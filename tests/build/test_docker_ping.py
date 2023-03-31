import pytest
import docker
import os

DOCKER_USER = os.environ.get('DOCKER_USER')
DOCKER_SECRET = os.environ.get('DOCKER_SECRET')
DOCKER_REPO = os.environ.get('DOCKER_REPO')

build_repo = f"{DOCKER_USER}/{DOCKER_REPO}"
build_tag = "latest"


def test_docker_ping_success():
    """
    Ensure that $PATH is configured correctly, and assert that a License key
    can be acquired by a license server.
    """
    client = docker.from_env()
    client.images.pull(f"{build_repo}:{build_tag}")

    log = client.containers.run(
        image=f"{build_repo}:{build_tag}",
        command='/bin/sh -c "sesinetd; sleep 5; sesictrl ping"'
    )

    assert "Successfully pinged" in log.decode('utf-8')
