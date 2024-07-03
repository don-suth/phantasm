from controller import MatrixController
from text_effect import TextEffect
import asyncio
from websockets import serve


async def main():
	controller = MatrixController()
	text_layer = await controller.add_to_layers(TextEffect)
	
	async def append_message(websocket):
		async for message in websocket:
			await text_layer.add_message("Donald", message)
	
	async with serve(append_message, "localhost", 8765):
		await controller.run()

asyncio.run(main())