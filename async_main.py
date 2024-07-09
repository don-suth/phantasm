from async_controller import MatrixController
from layers.connection_status_layer import ConnectionStatusLayer
from layers.clock_layer import ClockLayer
import asyncio
import websockets


async def main():
	controller = MatrixController()
	clock_layer = await controller.add_to_layers(ClockLayer)
	connection_status_layer = await controller.add_to_layers(ConnectionStatusLayer)
	contoller_run_task = asyncio.create_task(controller.run())
	async for websocket in websockets.client.connect("ws://localhost:8765"):
		try:
			# Connected
			await connection_status_layer.set_connected()
			async for message in websocket:
				# Process message
				pass
		except websockets.ConnectionClosed:
			# If the connection was closed unexpectedly: retry in 2 seconds
			await connection_status_layer.set_reconnecting()
			await asyncio.sleep(2)
			continue
		except websockets.WebSocketException:
			# All other connection problems: retry in 10 seconds
			await connection_status_layer.set_failed()
			await asyncio.sleep(10)
			await connection_status_layer.set_reconnecting()
			continue

asyncio.run(main())
