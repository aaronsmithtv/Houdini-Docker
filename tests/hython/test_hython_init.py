import pytest
import docker
import os

SIDEFX_CLIENT = os.environ.get('SIDEFX_CLIENT')
SIDEFX_SECRET = os.environ.get('SIDEFX_SECRET')

DOCKER_USER = os.environ.get('DOCKER_USER')
DOCKER_SECRET = os.environ.get('DOCKER_SECRET')
DOCKER_REPO = os.environ.get('DOCKER_REPO')

build_repo = f"{DOCKER_USER}/{DOCKER_REPO}"
build_tag = "latest"


@pytest.fixture(scope="module")
def docker_client():
    return docker.from_env()


def test_hython_environment(docker_client):
    """
    Test Hython environment setup and license acquisition.
    """
    success_message = "Hython test successful"

    command = f"""
    /bin/sh -c "
    hserver --clientid '{SIDEFX_CLIENT}' --clientsecret '{SIDEFX_SECRET}' --host 'https://www.sidefx.com/license/sesinetd' &&
    sesictrl login &&
    echo 'print(\"{success_message}\")' | hython"
    """

    log = docker_client.containers.run(
        image=f"{build_repo}:{build_tag}",
        command=command,
        environment={
            "SIDEFX_CLIENT": SIDEFX_CLIENT,
            "SIDEFX_SECRET": SIDEFX_SECRET
        }
    )

    log_output = log.decode('utf-8')
    # print(log_output)

    assert success_message in log_output
    # assert "OpenCL Exception" not in log_output
