from datetime import datetime
from pydantic import BaseModel


class AuthenticationPayload(BaseModel):
	token: str = "Hello!"


class AuthenticationEvent(BaseModel):
	time: datetime
	event: str = "Authenticate"
	payload: AuthenticationPayload



