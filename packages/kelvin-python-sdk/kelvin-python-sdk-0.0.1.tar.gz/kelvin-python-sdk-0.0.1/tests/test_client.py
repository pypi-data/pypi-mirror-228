import asyncio
from asyncio import StreamReader, StreamWriter
from time import sleep
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from kelvin.app.client import KelvinClient
from kelvin.app.stream import KelvinStream, KelvinStreamConfig, StreamInterface
from kelvin.sdk.datatype import KRN, Message, make_message
from kelvin.sdk.datatype.krn import KRN
from kelvin.sdk.datatype.primitives import StringParameter

pytest_plugins = ("pytest_asyncio",)


### Setup server
async def made_server(reader: StreamReader, writer: StreamWriter):
    print("Made server")
    while not writer.is_closing():
        data = await reader.readline()
        if data:
            writer.write(data)
            await writer.drain()
        await asyncio.sleep(0.05)


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def start_server(event_loop):
    print("Setting up server")
    server = await asyncio.start_server(made_server, "127.0.0.1", 8888)
    asyncio.get_event_loop().create_task(server.serve_forever())
    yield server
    server.close()
    await server.wait_closed()


### Stream Tests


@pytest.mark.asyncio
async def test_connect():
    stream = KelvinStream()
    await stream.connect()
    await stream.disconnect()


@pytest.mark.asyncio
async def test_rw():
    stream = KelvinStream()
    await stream.connect()
    msg = make_message("raw.float32", "metric1", value=1.0)
    await stream.write(msg)
    msg2 = await stream.read()
    await stream.disconnect()
    assert msg.value == msg2.value


### Client Tests
@pytest.mark.asyncio
async def test_client_connect():
    client = KelvinClient()
    await client.connect()
    await client.disconnect()


@pytest.mark.asyncio
async def test_client_ctx():
    async with KelvinClient() as client:
        assert client


def test_build_parameter_map():
    client = KelvinClient()
    client._build_parameter_map(False, {})
    assert client._asset_parameters == {}
    assert client._app_parameters == {}

    param = StringParameter()
    param.resource = KRN("param", "a.b.c")
    m = {"a": {"b": {"c": param}}}
    client._build_parameter_map(True, param)
    assert client._asset_parameters == m


def test_build_parameter_multimap():
    # This test is for a map containing multiple branches from the same root
    client = KelvinClient()
    client._build_parameter_map(False, {})
    assert client._asset_parameters == {}
    assert client._app_parameters == {}
    p1 = StringParameter()
    p1.resource = KRN("param", "a.b.c")
    p2 = StringParameter()
    p2.resource = KRN("param", "a.d")
    p3 = StringParameter()
    p3.resource = KRN("param", "a.b.f")
    m = {"a": {"b": {"c": p1, "f": p3}, "d": p2}}
    client._build_parameter_map(True, p1)
    client._build_parameter_map(True, p2)
    client._build_parameter_map(True, p3)
    assert client._asset_parameters == m
