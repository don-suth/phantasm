from async_controller import MatrixController
from datetime import datetime
from layers.connection_status_layer import ConnectionStatusLayer
from layers.clock_layer import ClockLayer
from layers.text_layer import TextLayer
from layers.smash_cut_to_text_transition import SmashCutTextTransition
from layers.alert_layer import AlertLayer
import asyncio
from websockets.client import connect
from websockets.exceptions import WebSocketException
from ritual_events.from_phantasm import AuthenticateAction, AuthenticateData
import os


async def main():
	controller = MatrixController()
	controller.set_brightness(50)
	clock_layer = await controller.add_to_layers(ClockLayer)
	connection_status_layer = await controller.add_to_layers(ConnectionStatusLayer)
	contoller_run_task = asyncio.create_task(controller.run())
	async for websocket in connect("wss://telepathy.unigames.asn.au:443"):
		try:
			# Connected
			print("ws connected")
			await connection_status_layer.set_connected()
			authentication = AuthenticateAction(
				data=AuthenticateData(
					token="Hello!"
				),
				time=datetime.now()
			).model_dump_json()
			await websocket.send(authentication)
			await asyncio.sleep(4)
			await controller.add_to_layers(
				SmashCutTextTransition,
				from_layer=None,
				to_layer=AlertLayer(matrix=controller.matrix, message="Donald Sutherland", location="Tav")
			)
			async for message in websocket:
				# Process message
				# await text_layer.add_message("WS", message)
				pass
		except WebSocketException:
			print("ws failed")
			# All other connection problems: retry in 10 seconds
			await connection_status_layer.set_failed()
			await asyncio.sleep(10)
		await connection_status_layer.set_reconnecting()
		await asyncio.sleep(2)


if __name__ == "__main__":
	asyncio.run(main())
