from async_controller import MatrixController
from layers.connection_status_layer import ConnectionStatusLayer
import asyncio
import websockets


async def main():
	controller = MatrixController()
	connection_status_layer = await controller.add_to_layers(ConnectionStatusLayer)

	async for websocket in websockets.connect("localhost"):
		try:
			# Connected
			await connection_status_layer.set_connected()
			async for message in websocket:
				# Process message
				pass
		except websockets.ConnectionClosed:
			await connection_status_layer.set_reconnecting()
			await asyncio.sleep(2)
			continue



asyncio.run(main())