from async_controller import MatrixController
from layers.connection_status_layer import ConnectionStatusLayer
from layers.clock_layer import ClockLayer
from layers.text_layer import TextLayer
import asyncio
from websockets.client import connect
from websockets.exceptions import WebSocketException
import os


async def main():
	controller = MatrixController()
	controller.set_brightness(50)
	clock_layer = await controller.add_to_layers(ClockLayer)
	connection_status_layer = await controller.add_to_layers(ConnectionStatusLayer)
	text_layer = await controller.add_to_layers(TextLayer)
	contoller_run_task = asyncio.create_task(controller.run())
	async for websocket in connect("ws://localhost:8765"):
		try:
			# Connected
			print("ws connected")
			await connection_status_layer.set_connected()
			async for message in websocket:
				# Process message
				text_layer.add_message("WS", message)
		except WebSocketException:
			print("ws failed")
			# All other connection problems: retry in 10 seconds
			await connection_status_layer.set_failed()
			await asyncio.sleep(10)
		await connection_status_layer.set_reconnecting()
		await asyncio.sleep(2)


if __name__ == "__main__":
	asyncio.run(main())
