import base64
import json
import time
import html

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from typing import Optional, Any

# from hinstall.model.service import ApiService
from hbuild.sidefxapi.model.file import ResponseFile
from hbuild.sidefxapi.model.service import ProductBuild, ProductModel, BuildDownloadModel
from hbuild.sidefxapi.exception import APIError, AuthorizationError


class WebHoudini:
	def __init__(self, sesi_secret: str, sesi_id: str):
		self.session = get_session()
		self.endpoint_url = "https://www.sidefx.com/api/"
		self.access_token, self.expiry_time = get_access_token_and_expiry_time(
			client_secret_key=sesi_secret,
			client_id=sesi_id
		)

	def get_latest_builds(
			self, build: ProductModel,
			only_production: Optional[bool] = True) -> list[ProductBuild]:
		api_command = "download.get_daily_builds_list"

		build = dict(build)
		build.update({'only_production': only_production})

		post_data = dict(json=json.dumps([api_command, [], build]))
		resp_builds = self.get_session_response(post_data)

		builds = [ProductBuild.parse_obj(resp_build) for resp_build in resp_builds]

		return builds

	def get_build_download(self, build: ProductBuild) -> BuildDownloadModel:
		api_command = "download.get_daily_build_download"

		build = dict(build)
		post_data = dict(json=json.dumps([api_command, [], build]))
		resp_build = self.get_session_response(post_data)

		return BuildDownloadModel.parse_obj(resp_build)

	def get_session_response(
			self, post_data: dict[str, Any],
			timeout: Optional[int] = None) -> Any:
		response = self.session.post(
			self.endpoint_url,
			headers={"Authorization": "Bearer " + self.access_token},
			data=post_data,
			timeout=timeout)
		# logging.info(f"Raised response code `{response.status_code}`")
		if response.status_code == 200:
			if response.headers.get("Content-Type") == "application/octet-stream":
				return ResponseFile(response)
			return response.json()

		raise APIError(
			response.status_code,
			_extract_traceback_from_response(response))


def get_session():
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
	return http


def get_access_token_and_expiry_time(
		client_id: str,
		client_secret_key: str,
		access_token_url: str = "https://www.sidefx.com/oauth2/application_token",
		timeout: Optional[int] = None):
	"""
	Given an API client (id and secret key) that is allowed to make API
	calls, return an access token that can be used to make calls.
	"""
	# If they're trying to use the /token URL directly then assume this is a
	# client-credentials application.
	post_data = {}
	if access_token_url.endswith("/token") or access_token_url.endswith("/token/"):
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


def without_keys(d, keys):
	return {k: d[k] for k in d.keys() - keys}
