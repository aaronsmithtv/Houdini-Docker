import json
import logging
import sys


def process_docker_message(raw_message) -> None:
	try:
		message_json = json.loads(raw_message)
		status = message_json.get("status", "")
		progress = message_json.get("progress", "")
		image_id = message_json.get("id", "")

		formatted_message = f"{status} - {progress} (Image ID: {image_id})"
		sys.stdout.write(f"\r{formatted_message}")
		sys.stdout.flush()
	except json.JSONDecodeError as e:
		logging.debug(f"Error `{e}` raised decoding JSON returned message")
