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
from ritual_events.from_phantasm import AuthenticateEvent
from ritual_events.to_phantasm import (
	LetMeInEvent,
	FoodRunEvent,
	UpdateClockSettingsEvent,
	validate_to_phantasm_json,
)
from pydantic import ValidationError
import os
import json


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
			authentication = AuthenticateEvent(
				token="Hello!"
			).model_dump_json()
			await websocket.send(authentication)
			async for message in websocket:
				# Process message
				# await text_layer.add_message("WS", message)
				event = validate_to_phantasm_json(message)
				match event:
					case LetMeInEvent(name=name, entrance=entrance):
						await controller.add_to_layers(
							SmashCutTextTransition,
							from_layer=None,
							to_layer=AlertLayer(
								matrix=controller.matrix,
								message=name,
								location=entrance
							)
						)
					case FoodRunEvent(entrance=entrance, arrival_time=arrival_time):
						await controller.add_to_layers(
							SmashCutTextTransition,
							from_layer=None,
							to_layer=AlertLayer(
								matrix=controller.matrix,
								message=f"Food run arriving at {arrival_time}",
								location=entrance
							)
						)
					case UpdateClockSettingsEvent(new_brightness=brightness, new_text_colour=new_colour, alternate_seconds=seconds):
						clock_layer.set_colour(*(new_colour.as_rgb_tuple(alpha=False)))
						clock_layer.set_seconds(seconds)
						controller.set_brightness(brightness)
					case _:
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
