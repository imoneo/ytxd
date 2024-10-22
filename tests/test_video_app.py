from typer.testing import CliRunner
from ytxd.main import app
import os
from . import cleanup
import ytxd.media_formats

runner = CliRunner()


YT_VIDEO_URL = "https://www.youtube.com/watch?v=OvlM5umIku8&list=PLhDz2jO-FE_dyCqK4PB17yNY3MLaQ7bz7&index=2"
YT_VIDEO_DEFAULT_VIDEO_NAME = "Click⧸Mouse Click Sound Effect (Copyright Free).mp4"
YT_PLAYLIST_URL = (
    "https://www.youtube.com/playlist?list=PLhDz2jO-FE_dyCqK4PB17yNY3MLaQ7bz7"
)
YT_PLAYLIST_DEFAULT_VIDEO_NAMES = (
    YT_VIDEO_DEFAULT_VIDEO_NAME,
    "Mouse Click Sound Effects (Copyright Free).mp4",
)

video_formats = [video_format.value for video_format in ytxd.media_formats.VideoFormat]


# $ ytxd video <url>
def test_download_video_cwd_default():
    result = runner.invoke(
        app,
        [
            "video",
            YT_VIDEO_URL,
        ],
    )
    assert result.exit_code == 0
    assert "Download completed" in result.stdout
    assert YT_VIDEO_DEFAULT_VIDEO_NAME in os.listdir()
    cleanup.remove_media_files_and_empty_directories()


# $ ytxd video --best <url>
def test_download_video_cwd_default_best():
    result = runner.invoke(
        app,
        [
            "video",
            "--best",
            YT_VIDEO_URL,
        ],
    )
    assert result.exit_code == 0
    assert "Download completed" in result.stdout
    assert YT_VIDEO_DEFAULT_VIDEO_NAME[:-3] + "mkv" in os.listdir()
    cleanup.remove_media_files_and_empty_directories()


# $ ytxd video --format <format> <url>
def test_download_video_specified_format():
    for format in video_formats:
        result = runner.invoke(app, ["video", "--format", format, YT_VIDEO_URL])
        assert result.exit_code == 0
        assert "Download completed" in result.stdout
        assert YT_VIDEO_DEFAULT_VIDEO_NAME[:-3] + format in os.listdir()
        cleanup.remove_media_files_and_empty_directories()


# $ ytxd video --path <downloads (new directory)> <url>
def test_download_video_relative_path_new_directory():
    new_dir_name = "downloads"
    path_to_new_dir = os.path.join(os.getcwd(), new_dir_name)
    result = runner.invoke(app, ["video", "--path", new_dir_name, YT_VIDEO_URL])
    assert result.exit_code == 0
    assert "Download completed" in result.stdout
    assert new_dir_name in os.listdir()
    assert os.path.isdir(path_to_new_dir)
    assert YT_VIDEO_DEFAULT_VIDEO_NAME in os.listdir(path_to_new_dir)
    cleanup.remove_media_files_and_empty_directories()


# $ytxd video --path < <new_name>.<extansion> > <url>
def test_download_video_specified_extansion():
    new_name_extansion = "effect.mkv"
    result = runner.invoke(app, ["video", "-o", new_name_extansion, YT_VIDEO_URL])
    assert result.exit_code == 0
    assert "Download completed" in result.stdout
    assert new_name_extansion in os.listdir()
    cleanup.remove_media_files_and_empty_directories()


# $ytxd video --path absolute_path_with_extansion> <url>
def test_download_video_absolute_path_extansion():
    new_name_extansion = "effect.mkv"
    new_dir_name = "absolute"
    cwd = os.getcwd()
    new_path = os.path.join(os.path.join(cwd, new_dir_name), new_name_extansion)
    result = runner.invoke(app, ["video", "--path", new_path, YT_VIDEO_URL])
    assert result.exit_code == 0
    assert "Download completed" in result.stdout
    assert new_dir_name in os.listdir()
    assert new_name_extansion in os.listdir(new_dir_name)
    cleanup.remove_media_files_and_empty_directories()


# $ ytxd video --resolution <resolution> <url>
def test_download_video_resolution():
    resolutions = [res.value for res in ytxd.media_formats.Resolution]
    for res in resolutions:
        result = runner.invoke(
            app,
            ["video", "--resolution", res, YT_VIDEO_URL],
        )
        assert result.exit_code == 0
        assert YT_VIDEO_DEFAULT_VIDEO_NAME in os.listdir()
        assert "Download completed" in result.stdout


# $ ytxd video <playlist url>
def test_download_video_playlist():
    result = runner.invoke(app, ["video", YT_PLAYLIST_URL])
    assert result.exit_code == 0
    assert "Download failed" not in result.stdout
    for name in YT_PLAYLIST_DEFAULT_VIDEO_NAMES:
        assert name in os.listdir()
    cleanup.remove_media_files_and_empty_directories()


# $ ytxd video -o <directory name> <playlist url>
def test_download_video_playlist_new_dir():
    new_dir_name = "effect"
    result = runner.invoke(app, ["video", "-o", new_dir_name, YT_PLAYLIST_URL])
    assert result.exit_code == 0
    assert new_dir_name in os.listdir()
    assert "Download failed" not in result.stdout
    for filename in YT_PLAYLIST_DEFAULT_VIDEO_NAMES:
        assert filename in os.listdir(new_dir_name)
    cleanup.remove_media_files_and_empty_directories()


# $ ytxd video --best -o <directory name> <url>
def test_download_video_playlist_new_dir_best():
    new_dir_name = "best"
    result = runner.invoke(
        app, ["video", "--best", "-o", new_dir_name, YT_PLAYLIST_URL]
    )
    assert result.exit_code == 0
    assert new_dir_name in os.listdir()
    assert "Download failed" not in result.stdout
    for filename in YT_PLAYLIST_DEFAULT_VIDEO_NAMES:
        assert filename[:-3] + "mkv" in os.listdir(new_dir_name)
    cleanup.remove_media_files_and_empty_directories()
