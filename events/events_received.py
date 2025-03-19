from datetime import datetime
from pydantic import BaseModel
from pydantic_extra_types.color import Color as Colour


class LetMeInPayload(BaseModel):
	name: str
	entrance: str


class LetMeInEvent(BaseModel):
	time: datetime
	event: str = "LetMeIn"
	payload: LetMeInPayload


class FoodRunPayload(BaseModel):
	arrival_time: datetime
	entrance: str


class FoodRunEvent(BaseModel):
	time: datetime
	event: str = "FoodRun"
	payload: FoodRunPayload


class ClockSettingsUpdatePayload(BaseModel):
	brightness: int | None
	text_colour: Colour | None
	alternate_seconds_indicator: bool | None


class ClockSettingsUpdateEvent(BaseModel):
	time: datetime
	event: str = "ClockSettingsUpdate"
	payload: ClockSettingsUpdatePayload
