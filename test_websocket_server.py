from websockets.server import serve
import asyncio


async def echo(websocket):
	print("Someone connected")
	# Close the connection in 10 seconds
	async def auto_close():
		await asyncio.sleep(10)
		await websocket.close()
	close_task = asyncio.create_task(auto_close())
	async for message in websocket:
		print(message)
		await websocket.send(message)


async def main():
	async with serve(echo, "localhost", 8765):
		await asyncio.Future()

asyncio.run(main())
