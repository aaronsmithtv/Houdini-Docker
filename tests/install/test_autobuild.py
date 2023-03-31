import unittest
from unittest.mock import MagicMock
from docker.errors import NotFound
import hbuild.autobuild as autobuild
import hbuild.sidefxapi.sidefx as sidefx


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


def test_get_latest_build():
    # Create a mock SideFX API service
    mock_service = MagicMock(spec=sidefx._Service)

    mock_download = MagicMock()
    mock_service.download = mock_download

    mock_download.get_daily_builds_list.return_value = [
        {
            'product': 'houdini',
            'version': '20.0.0',
            'build': '1234',
            'platform': 'linux',
        }
    ]

    mock_download.get_daily_build_download.return_value = {
        'download_url': 'https://example.com/houdini-20.0.0-1234.tar.gz',
        'filename': 'houdini-20.0.0-1234.tar.gz',
        'hash': '123456abcdef',
    }

    # Mock the sidefx.service() call to return the mock_service
    with unittest.mock.patch.object(
            sidefx, 'service', return_value=mock_service):
        latest_build = autobuild.get_latest_build()

    # Verify the results
    assert latest_build == {
        'download_url': 'https://example.com/houdini-20.0.0-1234.tar.gz',
        'filename': 'houdini-20.0.0-1234.tar.gz',
        'hash': '123456abcdef',
        'version': '20.0.0',
        'build': '1234',
    }

    # Verify that the mocked methods were called with the correct arguments
    mock_download.get_daily_builds_list.assert_called_once_with(
        product=autobuild.dl_product,
        platform=autobuild.dl_platform,
        only_production=True,
    )
    mock_download.get_daily_build_download.assert_called_once_with(
        product='houdini',
        version='20.0.0',
        build='1234',
        platform='linux',
    )
