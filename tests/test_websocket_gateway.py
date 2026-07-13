import asyncio
import json

import pytest
from websockets.asyncio.server import ServerConnection, serve

from nyx_local.domain.gateway import ProtocolValidationError
from nyx_local.infrastructure.websocket_gateway import WebSocketGateway


def test_websocket_gateway_connects_sends_receives_and_closes() -> None:
    async def scenario() -> None:
        received: list[dict[str, object]] = []

        async def handler(connection: ServerConnection) -> None:
            raw_message = await connection.recv()
            assert isinstance(raw_message, str)
            received.append(json.loads(raw_message))
            await connection.send(json.dumps({"type": "test", "protocolVersion": "1.0"}))

        async with serve(handler, "127.0.0.1", 0) as server:
            port = server.sockets[0].getsockname()[1]
            transport = WebSocketGateway(f"ws://127.0.0.1:{port}")
            await transport.connect()
            await transport.send({"type": "client.test", "protocolVersion": "1.0"})
            response = await transport.receive()
            await transport.close()

        assert received == [{"type": "client.test", "protocolVersion": "1.0"}]
        assert response == {"type": "test", "protocolVersion": "1.0"}

    asyncio.run(scenario())


def test_websocket_gateway_rejects_non_object_json() -> None:
    async def scenario() -> None:
        async def handler(connection: ServerConnection) -> None:
            await connection.send("[]")

        async with serve(handler, "127.0.0.1", 0) as server:
            port = server.sockets[0].getsockname()[1]
            transport = WebSocketGateway(f"ws://127.0.0.1:{port}")
            await transport.connect()
            with pytest.raises(ProtocolValidationError, match="JSON object"):
                await transport.receive()
            await transport.close()

    asyncio.run(scenario())
