import os

import docker
import pytest

SIDEFX_CLIENT = os.environ.get("SIDEFX_CLIENT")
SIDEFX_SECRET = os.environ.get("SIDEFX_SECRET")

DOCKER_USER = os.environ.get("DOCKER_USER")
DOCKER_SECRET = os.environ.get("DOCKER_SECRET")
DOCKER_REPO = os.environ.get("DOCKER_REPO")

build_repo = f"{DOCKER_USER}/{DOCKER_REPO}"
build_tag = "latest"


def test_hython_environment():
    """
    Test Hython environment setup and license acquisition.
    """
    client = docker.from_env()
    client.images.pull(f"{build_repo}:{build_tag}")

    success_message = "hython success"

    command = f"/bin/sh -c \"hserver --clientid \"{SIDEFX_CLIENT}\" --clientsecret \"{SIDEFX_SECRET}\" --host \"https://www.sidefx.com/license/sesinetd\"; sleep 5; sesictrl login; sleep 5; echo \'print(\\\"{success_message}\\\")\' > test.py && hython test.py\""

    log = client.containers.run(
        image=f"{build_repo}:{build_tag}",
        command=command,
        environment={"SIDEFX_CLIENT": SIDEFX_CLIENT, "SIDEFX_SECRET": SIDEFX_SECRET},
    )

    log_output = log.decode("utf-8")

    assert success_message in log_output
    # OpenCL Exception test - use this to verify whether Houdini default OpenCL installation is functional
    # assert "OpenCL Exception" not in log_output
