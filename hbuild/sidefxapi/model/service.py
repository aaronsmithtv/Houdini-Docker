from typing import Optional

from pydantic import AnyUrl, BaseModel


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
    hash: str


class BuildDownloadModel(InstallBuild):
    date: str
    releases_list: str
    status: str
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
