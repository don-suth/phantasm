from async_controller import MatrixController
from layers.connection_status_layer import ConnectionStatusLayer
from layers.clock_layer import ClockLayer
import asyncio
import websockets
import os

async def main():
	controller = MatrixController()
	controller.set_brightness(10)
	clock_layer = await controller.add_to_layers(ClockLayer)
	connection_status_layer = await controller.add_to_layers(ConnectionStatusLayer)
	contoller_run_task = asyncio.create_task(controller.run())
	async for websocket in websockets.connect("ws://localhost:8765"):
		try:
			# Connected
			print("ws connected")
			await connection_status_layer.set_connected()
			async for message in websocket:
				# Process message
				print(message)
		except websockets.exceptions.WebSocketException:
			print("ws failed")
			# All other connection problems: retry in 10 seconds
			await connection_status_layer.set_failed()
			await asyncio.sleep(10)
		await connection_status_layer.set_reconnecting()
		await asyncio.sleep(2)


if __name__ == "__main__":
	base_dir = os.path.dirname(os.path.abspath(__file__))
	activate_this = os.path.join(base_dir, "venv/bin/activate_this.py")
	with open(activate_this) as exec_file:
		exec(exec_file.read(), {'__file__': exec_file})
	asyncio.run(main())
