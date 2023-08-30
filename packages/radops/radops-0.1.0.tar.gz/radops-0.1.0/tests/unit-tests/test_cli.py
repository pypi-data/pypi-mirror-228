from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from radops.cli import app

runner = CliRunner()


@pytest.fixture
def mock_list_files():
    with patch(
        "radops.cli.list_files_and_folders"
    ) as mock_list_files_and_folders:
        with patch("radops.cli.list_local_files") as mock_list_local_files:
            yield mock_list_local_files, mock_list_files_and_folders


@pytest.fixture
def mock_file_exists_in_cloud():
    with patch("radops.cli.File.exists_in_cloud") as mock_exists_in_cloud:
        yield mock_exists_in_cloud


@pytest.fixture
def mock_download():
    with patch("radops.cli.File.exists_locally") as mock_exists_locally:
        with patch(
            "radops.cli.File.download_from_cloud"
        ) as mock_download_from_cloud:
            # mock_exists_locally.return_value = False/
            # mock_download_from_cloud.return_value = Mock()
            yield mock_exists_locally, mock_download_from_cloud


def test_ls(mock_list_files):
    # Set up mock responses
    mock_list_files[0].return_value = ["file1"]
    mock_list_files[1].return_value = [["file1", "file2"], []]

    result = runner.invoke(app, ["datalake", "ls"])
    assert result.exit_code == 0

    assert "file1" in result.stdout
    assert "file2" in result.stdout


def test_info(mock_file_exists_in_cloud):
    # Set up mock responses
    mock_file_exists_in_cloud.return_value = False

    with patch("radops.cli.File.print_info") as print_info:
        assert not print_info.called
        result = runner.invoke(app, ["datalake", "info", "file_uid"])
        assert result.exit_code == 0
        assert "does not exist" in result.stdout
        assert not print_info.called

    mock_file_exists_in_cloud.return_value = True

    with patch("radops.cli.File.print_info") as print_info:
        assert not print_info.called
        result = runner.invoke(app, ["datalake", "info", "file_uid"])
        assert result.exit_code == 0
        assert print_info.called


def test_download(mock_download, mock_file_exists_in_cloud):
    mock_exists_locally, mock_download_from_cloud = mock_download

    mock_file_exists_in_cloud.return_value = False
    assert not mock_download_from_cloud.called
    result = runner.invoke(app, ["datalake", "download", "file_uid"])
    assert result.exit_code == 0
    assert "is not in the datalake" in result.stdout
    assert not mock_download_from_cloud.called

    mock_file_exists_in_cloud.return_value = True
    mock_exists_locally.return_value = True
    result = runner.invoke(app, ["datalake", "download", "file_uid"])
    assert result.exit_code == 0
    assert "already exists locally" in result.stdout
    assert not mock_download_from_cloud.called

    mock_exists_locally.return_value = False
    result = runner.invoke(app, ["datalake", "download", "file_uid"])
    assert result.exit_code == 0
    assert mock_download_from_cloud.called
