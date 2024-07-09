from async_controller import MatrixController
from layers.connection_status_layer import ConnectionStatusLayer
from layers.clock_layer import ClockLayer
import asyncio
import websockets
from websockets.client import connect as ws_connect


async def main():
	controller = MatrixController()
	controller.set_brightness(10)
	clock_layer = await controller.add_to_layers(ClockLayer)
	connection_status_layer = await controller.add_to_layers(ConnectionStatusLayer)
	contoller_run_task = asyncio.create_task(controller.run())
	async for websocket in ws_connect("ws://localhost:8765"):
		try:
			# Connected
			print("ws connected")
			await connection_status_layer.set_connected()
			async for message in websocket:
				# Process message
				print(message)
		except websockets.exceptions.ConnectionClosed:
			# If the connection was closed unexpectedly: retry in 2 seconds
			print("ws reconnecting")
			await connection_status_layer.set_reconnecting()
			await asyncio.sleep(2)
			continue
		except websockets.exceptions.WebSocketException:
			print("ws failed")
			# All other connection problems: retry in 10 seconds
			await connection_status_layer.set_failed()
			await asyncio.sleep(10)
			await connection_status_layer.set_reconnecting()
			continue

asyncio.run(main())
