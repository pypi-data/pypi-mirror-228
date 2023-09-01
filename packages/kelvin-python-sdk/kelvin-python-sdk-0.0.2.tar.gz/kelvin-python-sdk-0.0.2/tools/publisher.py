import asyncio
from asyncio import StreamReader, StreamWriter

from kelvin.sdk.datatype import Float32, KRNAssetMetric, KRNWorkload, Message

MESSAGES = {"asset1": ["metric1", "metric2", "metric3"]}


async def handle_read(reader: StreamReader):
    while True:
        data = await reader.readline()
        if not len(data):
            break
        try:
            msg = Message.parse_raw(data)
            print("Got message", msg)
        except Exception as e:
            print("Error parsing message", e)


async def handle_write(writer: StreamWriter):
    value = 0
    while not writer.is_closing():
        print("Publishing messages", value)
        for asset, metrics in MESSAGES.items():
            for metric in metrics:
                msg = Float32(
                    resource=KRNAssetMetric(asset, metric),
                    source=KRNWorkload("mynode", "mypublisher"),
                    payload={"value": value},
                )
                writer.write(msg.encode() + b"\n")

            try:
                await writer.drain()
            except ConnectionResetError:
                pass

        value += 1
        await asyncio.sleep(1)


async def handle_client(reader: StreamReader, writer: StreamWriter):
    print("New client")
    tasks = {
        asyncio.create_task(handle_read(reader)),
        asyncio.create_task(handle_write(writer)),
    }

    await asyncio.gather(*tasks)
    print("Connection lost")


async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8888)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving on {addrs}")

    async with server:
        await server.serve_forever()


asyncio.run(main())
