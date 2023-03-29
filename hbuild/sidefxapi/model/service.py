from pydantic import BaseModel


class ApiService(BaseModel):
	client_id: str
	client_secret: str
	access_token_url: str
	endpoint_url: str
