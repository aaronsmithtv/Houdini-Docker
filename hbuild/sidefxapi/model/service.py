from pydantic import BaseModel, Field, AnyUrl, validator
from datetime import datetime
from enum import Enum
from typing import Optional
import re


class HashModel(BaseModel):
    hash: str

    @validator('hash')
    def validate_md5_hash(cls, hash_str):
        if re.match(r"^[a-fA-F0-9]{32}$", hash_str):
            return hash_str
        raise ValueError("Invalid MD5 hash format")


class Platform(Enum):
    WINDOWS = "win64"
    MACOS = "macos"
    MACOS_ARM = "macosx_arm64"
    LINUX = "linux"


class PlatformModel(BaseModel):
    platform: str

    @validator('platform')
    def validate_platform(cls, platform_str):
        for plat in Platform:
            if platform_str.startswith(plat.value):
                return platform_str
        raise ValueError(
            "Platform should start with: " + ', '.join(
                [p.value for p in Platform]))


class DateModel(BaseModel):
    date: str

    @validator('date')
    def validate_date_format(cls, date_str):
        try:
            datetime.strptime(date_str, '%Y/%m/%d')
            return date_str
        except ValueError:
            raise ValueError("Incorrect date format, should be 'YYYY/MM/DD'")


class ApiService(BaseModel):
    client_id: str = Field(..., description="SideFX Application Client ID")
    client_secret: str = Field(..., description="SideFX Application Client Secret")
    access_token_url: AnyUrl = Field(..., description="The URL for retrieving the access token")
    endpoint_url: AnyUrl = Field(..., description="The base URL for the API endpoint")


class ProductModel(BaseModel):
    product: str
    platform: str


class ProductBuild(ProductModel):
    version: Optional[str]
    build: Optional[str]


class DailyBuild(ProductBuild):
    date: str
    release: str
    status: str

    class Config:
        schema_extra = {
            "example": {
                "build": "382",
                "date": "2018/10/26",
                "platform": "linux_x86_64_gcc6.3",
                "product": "houdini",
                "release": "devel",
                "status": "good",
                "version": "17.0",
            }
        }


class InstallBuild(BaseModel):
    download_url: AnyUrl
    filename: str
    hash: HashModel


class BuildDownloadModel(InstallBuild):
    date: Optional[str]
    releases_list: Optional[str]
    status: Optional[str]
    size: int

    class Config:
        schema_extra = {
            "example": {
                "date": "2018/10/26",
                "download_url": "https://example.cloudfront.net/download",
                "filename": "houdini-17.0.352-win64-vc141.exe",
                "hash": "001e6e62aed5a3e5c10d3f2019bf41b5",
                "releases_list": "gold",
                "status": "good",
                "size": 1114902200,
            }
        }
