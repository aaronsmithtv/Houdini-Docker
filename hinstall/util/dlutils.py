import hashlib
import logging
import os
import pathlib
import tarfile

import requests
from tqdm import tqdm

logger = logging.getLogger(__name__)


def extract_tar_gz_file(file_path: str) -> str:
    """
    Extracts a .tar.gz file and removes the original .tar.gz file
    """
    # Open the file for reading with gzip compression
    with tarfile.open(file_path, "r:gz") as tar:
        # Extract all files to the current directory
        tar.extractall(path=get_parent_path(file_path))
        extracted_name = tar.getnames()[0]

    # Remove the original .tar.gz file
    os.remove(file_path)
    return extracted_name


def get_parent_path(path: str):
    return str(pathlib.Path(path).parents[0])


def download_hou_file(dl_request: dict) -> None:
    """
    Download the Houdini version at the daily build request
    """
    write_path = get_hou_write_path(dl_request)
    response = requests.get(dl_request["download_url"], stream=True)
    if response.status_code == 200:
        logging.info(f"Downloading file to `{write_path}`")
        with open(write_path, "wb") as f:
            response.raw.decode_content = True
            total_size = int(response.headers.get("Content-Length", 0))
            block_size = 1024
            progress_bar = tqdm(
                total=total_size, unit="iB", unit_scale=True, desc="Downloading"
            )
            for chunk in response.iter_content(block_size):
                progress_bar.update(len(chunk))
                f.write(chunk)
        progress_bar.close()
    else:
        raise Exception("Could not download file at URL")


def verify_hou_checksum(dl_request: dict) -> None:
    """
    Verify the SideFX download hash against the file hash
    """
    write_path = get_hou_write_path(dl_request)
    file_hash = hashlib.md5()
    with open(write_path, "rb") as f:
        total_size = os.path.getsize(write_path)
        progress_bar = tqdm(
            total=total_size, unit="iB", unit_scale=True, desc="Checksum Matching"
        )
        for chunk in iter(lambda: f.read(4096), b""):
            file_hash.update(chunk)
            progress_bar.update(len(chunk))
        progress_bar.close()
    if file_hash.hexdigest() != dl_request["hash"]:
        raise Exception("Could not verify checksum")
    logging.info(f"Download and checksum verified successfully at `{write_path}`")


def extract_hou_tar(dl_request: dict) -> None:
    """
    Extracts the .tar.gz file downloaded from the SideFX API
    """
    write_path = get_hou_write_path(dl_request)
    extract_name = extract_tar_gz_file(file_path=write_path)
    extract_path = f"{get_parent_path(write_path)}//{extract_name}"
    new_path = f"{get_parent_path(write_path)}//build"
    os.rename(extract_path, new_path)
    logging.info(f"Extracted .tar.gz file from `{extract_path}` to `{new_path}`")


def get_hou_write_path(dl_request: dict) -> str:
    houdini_path = f"{get_parent_path(os.getcwd())}/houdini"
    write_path = f"{houdini_path}/{dl_request['filename']}"
    return write_path
