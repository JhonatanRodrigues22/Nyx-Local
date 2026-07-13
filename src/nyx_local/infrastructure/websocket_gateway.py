from __future__ import annotations

import json
from math import isfinite
from typing import TypeGuard, cast

from websockets.asyncio.client import ClientConnection, connect

from nyx_local.domain.gateway import GatewayTransport, ProtocolValidationError
from nyx_local.domain.skills import JsonValue


class WebSocketGateway(GatewayTransport):
    """Concrete WebSocket transport for the Nyx OS local gateway."""

    def __init__(self, url: str, *, max_payload_bytes: int = 64 * 1024) -> None:
        self._url = url
        self._max_payload_bytes = max_payload_bytes
        self._connection: ClientConnection | None = None

    async def connect(self) -> None:
        await self.close()
        self._connection = await connect(
            self._url,
            max_size=self._max_payload_bytes,
            open_timeout=10,
        )

    async def send(self, payload: dict[str, JsonValue]) -> None:
        connection = self._require_connection()
        await connection.send(json.dumps(payload, separators=(",", ":")))

    async def receive(self) -> dict[str, JsonValue]:
        connection = self._require_connection()
        raw_message = await connection.recv()
        if not isinstance(raw_message, str):
            raise ProtocolValidationError("binary WebSocket messages are not supported")

        decoded = cast(object, json.loads(raw_message))
        if not isinstance(decoded, dict) or not all(isinstance(key, str) for key in decoded):
            raise ProtocolValidationError("gateway message must be a JSON object")
        if not _is_json_value(decoded):
            raise ProtocolValidationError("gateway message contains a non-JSON value")
        return cast(dict[str, JsonValue], decoded)

    async def close(self) -> None:
        connection = self._connection
        self._connection = None
        if connection is not None:
            await connection.close()

    def _require_connection(self) -> ClientConnection:
        if self._connection is None:
            raise ConnectionError("WebSocket gateway is not connected")
        return self._connection


def _is_json_value(value: object) -> TypeGuard[JsonValue]:
    if isinstance(value, float):
        return isfinite(value)
    if value is None or isinstance(value, str | int | bool):
        return True
    if isinstance(value, list):
        return all(_is_json_value(item) for item in value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and _is_json_value(item) for key, item in value.items())
    return False
