import asyncio
from asyncio import Queue
from typing import AsyncGenerator

from kelvin.app import KelvinClient, filters
from kelvin.sdk.datatype import KRNAssetMetric, Message, make_message


async def on_connect():
    print("Hello, it's connected")


async def on_data(msg: Message):
    print(f"Hello, got a message: {msg.resource} = {msg.payload.value}")


async def on_disconnect():
    print("Hello, it's disconnected")


async def on_parameter(msg: Message):
    print("Hello, it's parameter")
    print(msg)


async def handle_queue(queue: Queue[Message]):
    while True:
        msg = await queue.get()
        print("Received metric1: ", msg)


async def handle_stream(stream: AsyncGenerator[Message, None]):
    async for msg in stream:
        print("Received metric2: ", msg)


async def main():
    cli = KelvinClient()
    cli.on_connect = on_connect
    cli.on_data = on_data
    cli.on_disconnect = on_disconnect
    cli.on_app_parameter = on_parameter
    cli.on_asset_parameter = on_parameter

    queue1 = cli.filter(filters.resource_equal(KRNAssetMetric("asset1", "metric1")))
    asyncio.create_task(handle_queue(queue1))

    stream2 = cli.stream_filter(filters.resource_equal(KRNAssetMetric("asset1", "metric2")))
    asyncio.create_task(handle_stream(stream2))

    await cli.connect()

    while True:
        m = Message(**{"type": "data;icd=raw.float32", "payload": {"value": 123.5}})
        m.resource = KRNAssetMetric("asset-1", "x-both")
        # print("Sending message: ", m)
        # await cli.publish_message(m)
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
