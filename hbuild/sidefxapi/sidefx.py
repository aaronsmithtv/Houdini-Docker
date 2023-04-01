import time
import json
import base64
import io
import html
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from typing import Optional, Any

# from hinstall.model.service import ApiService
from hbuild.sidefxapi.exception import APIError, AuthorizationError
from hbuild.sidefxapi.model.file import File, ResponseFile


class _Service:
    def __init__(
            self, endpoint_url, access_token, access_token_expiry_time,
            timeout):
        self.endpoint_url: str = endpoint_url
        self.access_token: str = access_token
        self.access_token_expiry_time: int = access_token_expiry_time
        self.timeout: int = timeout

    def __getattr__(self, attr_name):
        return _APIFunction(attr_name, self)


class _APIFunction:
    def __init__(self, function_name: str, apiservice: _Service):
        self.function_name = function_name
        self.service = apiservice
        logging.info(f"Function: `{self.function_name}`, Service: `{self.service}`")

    def __getattr__(self, attr_name):
        # This isn't actually an API function, but a family of them.  Append
        # the requested function name to our name.
        return _APIFunction(
            "%s.%s" % (self.function_name, attr_name), self.service)

    def __call__(self, *args, **kwargs):
        return call_api_with_access_token(
            self.service.endpoint_url, self.service.access_token,
            self.function_name, args, kwargs,
            timeout=self.service.timeout)


def get_access_token_and_expiry_time(
        access_token_url: str, client_id: str,
        client_secret_key: str, timeout: Optional[int] = None):
    """
    Given an API client (id and secret key) that is allowed to make API
    calls, return an access token that can be used to make calls.
    """
    # If they're trying to use the /token URL directly then assume this is a
    # client-credentials application.
    post_data = {}
    if (access_token_url.endswith("/token") or
            access_token_url.endswith("/token/")):
        post_data["grant_type"] = "client_credentials"

    auth_header = f"{client_id}:{client_secret_key}".encode()

    response = requests.post(
        access_token_url,
        headers={
            "Authorization": f"Basic {base64.b64encode(auth_header).decode('utf-8')}",
        },
        data=post_data,
        timeout=timeout)
    # logging.info(f"Raised response code `{response.status_code}`")
    if response.status_code != 200:
        raise AuthorizationError(
            response.status_code,
            "{0}: {1}".format(
                response.status_code,
                _extract_traceback_from_response(response)))

    response_json = response.json()
    access_token_expiry_time = time.time() - 2 + response_json["expires_in"]
    return response_json["access_token"], access_token_expiry_time


def call_api_with_access_token(
        endpoint_url: str, access_token: str, function_name: str,
        args: Any, kwargs: Any, timeout: Optional[int] = None):
    """
    Call into the API using an access token that was returned by
    get_access_token.
    """
    logging.info(f"kwargs items: {kwargs.items()}")
    file_data = {}
    for arg_name, arg_value in kwargs.items():
        if isinstance(arg_value, (bytearray, File)):
            if isinstance(arg_value, File):
                file_data[arg_name] = (
                    arg_value.filename, open(arg_value.filename, "rb"),
                    "application/octet-stream")
            else:
                file_data[arg_name] = (
                    "unnamed.bin", io.BytesIO(arg_value),
                    "application/octet-stream")
    for arg_name in file_data:
        del kwargs[arg_name]

    post_data = dict(json=json.dumps([function_name, args, kwargs]))
    logging.info(f"Post data: `{post_data}`")

    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, ],
        method_whitelist=["GET", "POST"],
        backoff_factor=1,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    logging.info(f"file data: `{file_data}`")
    response = http.post(
        endpoint_url,
        headers={"Authorization": "Bearer " + access_token},
        data=post_data,
        timeout=timeout,
        files=file_data,
        stream=True)
    # logging.info(f"Raised response code `{response.status_code}`")
    if response.status_code == 200:
        if response.headers.get("Content-Type") == "application/octet-stream":
            return ResponseFile(response)
        return response.json()

    raise APIError(
        response.status_code,
        _extract_traceback_from_response(response))


def _extract_traceback_from_response(response: requests.Response):
    """Helper function to extract a traceback from the web server response
    if an API call generated a server-side exception and the server is running
    in debug mode.  In production mode, the server will send back just the
    stack trace without the need to parse any html.
    """
    error_message = response.text
    if response.status_code != 500:
        return error_message

    traceback = ""
    for line in error_message.split("\n"):
        if traceback and line == "</textarea>":
            break
        if line == "Traceback:" or traceback:
            traceback += line + "\n"

    if traceback:
        traceback = error_message

    return html.unescape(traceback)


def service(
        client_id: str,
        client_secret_key: str,
        access_token_url: str = "https://www.sidefx.com/oauth2/application_token",
        endpoint_url: str = "https://www.sidefx.com/api/",
        access_token: Optional[str] = None,
        access_token_expiry_time: Optional[int] = None,
        timeout: Optional[int] = None) -> _Service:
    """
    Calls upon SideFX API endpoint to
    """
    if (access_token is None or
            access_token_expiry_time is None or
            access_token_expiry_time < time.time()):
        access_token, access_token_expiry_time = (
            get_access_token_and_expiry_time(
                access_token_url, client_id, client_secret_key,
                timeout=timeout))

    return _Service(
        endpoint_url, access_token, access_token_expiry_time, timeout=timeout)
