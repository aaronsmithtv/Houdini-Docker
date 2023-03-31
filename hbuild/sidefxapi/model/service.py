from pydantic import BaseModel, Field, UrlStr
from datetime import date
from enum import Enum

class ApiService(BaseModel):
    client_id: str = Field(..., description="SideFX Application Client ID")
    client_secret: str = Field(..., description="SideFX Application Client Secret")
    access_token_url: UrlStr = Field(..., description="The URL for retrieving the access token")
    endpoint_url: UrlStr = Field(..., description="The base URL for the API endpoint")

class Platform(Enum):
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"

class DailyBuild(BaseModel):
    build: str
    date: str
    platform: Platform
    product: str
    release: str
    status: str
    version: str

class DownloadBuild(BaseModel):
    date: str
    download_url: UrlStr
    filename: str
    hash: str
    releases_list: str
    status: str
    size: int
