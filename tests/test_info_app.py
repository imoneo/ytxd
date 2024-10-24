from typer.testing import CliRunner
from ytxd.main import app
import os
from . import cleanup

YT_VIDEO_URL = "https://www.youtube.com/watch?v=RvW6eunLqwM"
JSON_FILENAME = "pink-noise-sfx-no-copyright.json"

runner = CliRunner()


# $ ytxd info <url>
def test_download_info_cwd():
    result = runner.invoke(app, ["info", "--no-preview", YT_VIDEO_URL])
    assert result.exit_code == 0
    assert JSON_FILENAME in os.listdir()
    assert "Download completed" in result.stdout
    cleanup.remove_media_files_and_empty_directories()


# $ ytxd info <relative path> <url>
def test_download_info_relative_path():
    new_dir_name = "newdir"
    os.makedirs(new_dir_name)
    assert new_dir_name in os.listdir()

    result = runner.invoke(
        app, ["info", "--no-preview", "--path", new_dir_name, YT_VIDEO_URL]
    )
    assert result.exit_code == 0
    assert JSON_FILENAME in os.listdir(new_dir_name)
    assert "Download completed" in result.stdout


# $ ytxd info --path <downloads> <url>
def test_download_info_relative_new_dir_path():
    new_name = "downloads"
    result = runner.invoke(
        app, ["info", "--no-preview", "--path", new_name, YT_VIDEO_URL]
    )
    assert result.exit_code == 0
    assert f"{new_name}.json" in os.listdir()
    assert "Download completed" in result.stdout
    cleanup.remove_media_files_and_empty_directories()


# $ ytxd info --path <absolute path with suffix> <url>
def test_download_info_absolute_path_suffix():
    name_with_suffix = "suffix.txt"
    abs_path = os.path.join(os.getcwd(), name_with_suffix)
    result = runner.invoke(
        app,
        ["info", "--no-preview", "--path", abs_path, YT_VIDEO_URL],
    )
    assert result.exit_code == 0
    assert f"{name_with_suffix[:-3]}json" in os.listdir()
    assert "Download completed" in result.stdout
    cleanup.remove_media_files_and_empty_directories()
