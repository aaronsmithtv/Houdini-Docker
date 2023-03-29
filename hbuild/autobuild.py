import docker
from docker.errors import NotFound

import os
import logging

import hbuild.sidefxapi.sidefx as sidefx
import hbuild.util.logutils as logutils


logging.basicConfig(level=logging.INFO)

dl_eula_date = "2021-10-13"
dl_product = 'houdini'
dl_platform = 'linux'

DOCKER_USER = os.environ.get('DOCKER_USER')
DOCKER_SECRET = os.environ.get('DOCKER_SECRET')

SIDEFX_CLIENT = os.environ.get('SIDEFX_CLIENT')
SIDEFX_SECRET = os.environ.get('SIDEFX_SECRET')

install_dir = "../hinstall"
build_repo = f"{DOCKER_USER}/hbuild"


def image_tag_exists(docker_client: docker.DockerClient, tag: str, repo: str) -> bool:
	try:
		server_image = docker_client.images.pull(repository=repo, tag=tag)
	except NotFound as e:
		logging.debug(f"Error `{e}` raised pulling server image")
		server_image = None
	if server_image:
		logging.info(f"Upload not needed, image tag `{tag}` already exists")
		return False
	logging.info(f"Tag does not exist in repository, beginning download/push process...")
	return True


def get_latest_build() -> dict:
	logging.info(f"Starting Houdini download client service")
	# Set up the SideFX API service
	service = sidefx.service(
		access_token_url="https://www.sidefx.com/oauth2/application_token",
		client_id=SIDEFX_CLIENT,
		client_secret_key=SIDEFX_SECRET,
		endpoint_url="https://www.sidefx.com/api/",
	)

	# Retrieve the daily builds list for the specified product, version, and platform
	latest_build = service.download.get_daily_builds_list(
		product=dl_product,
		platform=dl_platform,
		only_production=True)[0]

	# Retrieve the latest daily build available
	srv_build = service.download.get_daily_build_download(
		product=latest_build['product'],
		version=latest_build['version'],
		build=latest_build['build'],
		platform=dl_platform)

	build = {
		'download_url': srv_build['download_url'],
		'filename': srv_build['filename'],
		'hash': srv_build['hash'],
		'version': latest_build['version'],
		'build': latest_build['build'],
	}

	return build


if __name__ == "__main__":
	client = docker.from_env()

	dl_build = get_latest_build()

	build_tag = f"{dl_build['version']}.{dl_build['build']}-base"
	logging.info(f'Latest build found: `{build_tag}`')

	tag_status = image_tag_exists(
		docker_client=client,
		tag=build_tag,
		repo=build_repo
	)

	if tag_status:
		build_args = {
			'DL_URL': dl_build['download_url'],
			'DL_NAME': dl_build['filename'],
			'DL_HASH': dl_build['hash'],
			'EULA_DATE': dl_eula_date,
		}

		dockerfile_dir = os.path.join(os.path.dirname(__file__), "..", "hinstall")

		logging.info("Building Docker image...")
		image, logs = client.images.build(
			path=os.path.abspath(dockerfile_dir),
			rm=True,
			nocache=True,
			tag=f"{build_repo}:{build_tag}",
			buildargs=build_args,
			encoding="gzip",
		)

		logging.info(f"Built Docker image `{image.short_id}`, pushing to Docker hub...")
		client.login(username=DOCKER_USER, password=DOCKER_SECRET)

		for line in client.images.push(repository=build_repo, tag=build_tag, stream=True):
			logutils.process_docker_message(line)
		logging.info(f"Successfully pushed Docker image `{build_tag}` in `{build_repo}`.")

		docker.from_env().images.get(f"{build_repo}:{build_tag}").tag(f"{build_repo}:latest")

		for line in client.images.push(repository=build_repo, tag='latest', stream=True):
			logutils.process_docker_message(line)
		logging.info(f"Successfully pushed Docker image `latest` in `{build_repo}`.")

	logging.info(f"Finished HouDocker process, exiting...")
