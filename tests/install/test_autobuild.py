from unittest.mock import MagicMock

from docker.errors import NotFound

import hbuild.autobuild as autobuild


def test_image_tag_exists():
    docker_client = MagicMock()
    repo = "example/repo"
    tag = "test-tag"

    # Scenario 1: Image tag exists
    docker_client.images.pull.return_value = "some-image-id"
    result = autobuild.image_tag_exists(docker_client, tag, repo)
    assert result is False
    docker_client.images.pull.assert_called_once_with(repository=repo, tag=tag)

    # Reset the MagicMock
    docker_client.reset_mock()

    # Scenario 2: Image tag does not exist
    docker_client.images.pull.side_effect = NotFound("Not found")
    result = autobuild.image_tag_exists(docker_client, tag, repo)
    assert result is True
    docker_client.images.pull.assert_called_once_with(repository=repo, tag=tag)
