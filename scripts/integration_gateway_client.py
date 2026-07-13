"""Controlled resident client used only by the Node-to-Python integration check."""

import asyncio
import sys

from nyx_local.core.bootstrap import Bootstrap
from nyx_local.core.settings import Settings
from nyx_local.services.gateway_service import GatewayService


async def run() -> None:
    bootstrap = Bootstrap()
    bootstrap.initialize(Settings.from_env(require_gateway_token=True))
    if bootstrap.registry is None:
        raise RuntimeError("Bootstrap did not initialize the registry")
    service = bootstrap.registry.get("gateway_service")
    if not isinstance(service, GatewayService):
        raise RuntimeError("Bootstrap did not register GatewayService")

    service_task = asyncio.create_task(service.run())
    try:
        await asyncio.to_thread(sys.stdin.readline)
    finally:
        await service.shutdown()
        await service_task
        bootstrap.shutdown()


if __name__ == "__main__":
    asyncio.run(run())
