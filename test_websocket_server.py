from websockets.server import serve
import asyncio


async def echo(websocket):
	print("Someone connected")
	async for message in websocket:
		print(message)
		await websocket.send(message)


async def main():
	async with serve(echo, "localhost", 8765):
		await asyncio.Future()

asyncio.run(main())
