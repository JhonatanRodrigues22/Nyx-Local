/** @jest-environment node */

import { NyxRuntime } from "@nyx-os/core";
import { createInMemoryEventBus, type NyxSystemEvents } from "@nyx-os/event-bus";
import { randomUUID } from "node:crypto";
import { spawn, type ChildProcessWithoutNullStreams } from "node:child_process";

async function waitFor(predicate: () => boolean, timeoutMs = 10_000): Promise<void> {
  const deadline = Date.now() + timeoutMs;
  while (!predicate()) {
    if (Date.now() >= deadline) {
      throw new Error("Cross-project integration condition timed out");
    }
    await new Promise((resolve) => setTimeout(resolve, 20));
  }
}

function waitForExit(child: ChildProcessWithoutNullStreams): Promise<number | null> {
  return new Promise((resolve) => child.once("exit", (code) => resolve(code)));
}

describe("Nyx OS and Nyx Local real integration", () => {
  jest.setTimeout(30_000);

  it("executes success and structured failure through the Python client", async () => {
    const projectPath = process.env.NYX_LOCAL_PROJECT_PATH;
    const python = process.env.NYX_LOCAL_PYTHON;
    if (!projectPath || !python) {
      throw new Error("Integration paths were not provided")
    }

    const token = randomUUID();
    process.env.NYX_LOCAL_GATEWAY_TOKEN = token;
    const events = createInMemoryEventBus<NyxSystemEvents>();
    let failedCommandMetadata: Record<string, unknown> | undefined;
    events.on("local.command.failed", (event) => {
      failedCommandMetadata = event.payload?.metadata;
    });
    const runtime = new NyxRuntime(undefined, {
      events,
      registerBaseAutomations: false,
      registerBaseCapabilities: false,
      registerBasePlugins: false,
      registerBaseServices: false,
      registerBaseTools: false,
      registerLocalGateway: true,
      localGatewayOptions: { port: 0 },
      localCommandTimeoutMs: 2_000
    });
    let child: ChildProcessWithoutNullStreams | null = null;

    try {
      await runtime.start();
      const gateway = runtime.getLocalGateway();
      if (!gateway) {
        throw new Error("Nyx OS did not create LocalGatewayServer")
      }
      const address = gateway.getAddress();
      child = spawn(python, ["scripts/integration_gateway_client.py"], {
        cwd: projectPath,
        env: {
          ...process.env,
          NYX_LOCAL_GATEWAY_TOKEN: token,
          NYX_LOCAL_GATEWAY_URL: `ws://${address.host}:${address.port}`,
          NYX_LOCAL_INSTANCE_ID: "nyx-local-integration"
        },
        stdio: "pipe"
      });

      await waitFor(() => runtime.getTools().isAvailable("local.echo"));
      const execution = await runtime.getTools().execute("local.echo", { message: "node-python" });
      expect(execution.result).toEqual({ message: "node-python" });

      let commandError: unknown;
      try {
        await runtime.getCapabilities().execute("local.echo", { message: 42 });
      } catch (error) {
        commandError = error;
      }

      expect(commandError).toMatchObject({
        code: "REMOTE_COMMAND_FAILED",
        retryable: false,
        details: {
          capabilityId: "local.echo",
          internalCode: "INVALID_SKILL_INPUT"
        }
      });
      expect(failedCommandMetadata).toMatchObject({
        requestId: expect.any(String),
        instanceId: "nyx-local-integration",
        capabilityId: "local.echo",
        errorCode: "REMOTE_COMMAND_FAILED"
      });

      const exitPromise = waitForExit(child);
      child.stdin.write("stop\n");
      child.stdin.end();
      await expect(exitPromise).resolves.toBe(0);
      await waitFor(() => !runtime.getTools().isAvailable("local.echo"));
    } finally {
      if (child && child.exitCode === null) {
        child.kill();
      }
      await runtime.stop();
      delete process.env.NYX_LOCAL_GATEWAY_TOKEN;
    }
  });
});
