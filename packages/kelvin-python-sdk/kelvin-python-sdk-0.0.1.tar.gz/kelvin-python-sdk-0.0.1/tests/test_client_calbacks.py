import asyncio
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

from kelvin.app import KelvinClient


class MockStream:
    connected = False

    def __init__(self, config=None, data=[]) -> None:
        self.mock_data: list = data
        pass

    async def connect(self):
        if len(self.mock_data) > 0:
            self.connected = True
        else:
            raise ConnectionError()

    async def disconnect(self):
        self.connected = False

    async def read(self):
        await asyncio.sleep(0.1)
        try:
            return self.mock_data.pop(0)
        except IndexError:
            raise ConnectionError()

    async def write(self, msg) -> bool:
        return True


@pytest.mark.asyncio
@patch("kelvin.app.client.KelvinStream")
async def test_connect_disconnect(streamMock: MagicMock):
    mock = MagicMock(wraps=MockStream(data=[1]))
    streamMock.return_value = mock

    on_connect = AsyncMock()
    on_disconnect = AsyncMock()

    cli = KelvinClient()
    cli.on_connect = on_connect
    cli.on_disconnect = on_disconnect
    await cli.connect()
    await asyncio.sleep(0.1)
    await cli.disconnect()

    on_connect.assert_called_once()
    on_disconnect.assert_called_once()
