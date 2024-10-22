from typer.testing import CliRunner
from ytxd.main import app
import os
from . import cleanup
import ytxd.media_formats

runner = CliRunner()


YT_VIDEO_URL = "https://www.youtube.com/watch?v=OvlM5umIku8&list=PLhDz2jO-FE_dyCqK4PB17yNY3MLaQ7bz7&index=2"
YT_VIDEO_DEFAULT_AUDIO_NAME = "Click⧸Mouse Click Sound Effect (Copyright Free).mp3"
YT_PLAYLIST_URL = (
    "https://www.youtube.com/playlist?list=PLhDz2jO-FE_dyCqK4PB17yNY3MLaQ7bz7"
)
YT_PLAYLIST_DEFAULT_AUDIO_NAMES = (
    YT_VIDEO_DEFAULT_AUDIO_NAME,
    "Mouse Click Sound Effects (Copyright Free).mp3",
)

audio_formats = tuple(
    [audio_format.value for audio_format in ytxd.media_formats.AudioFormat]
)


# $ ytxd audio <url>
def test_download_audio_cwd_default():
    result = runner.invoke(
        app,
        [
            "audio",
            "--no-preview",
            YT_VIDEO_URL,
        ],
    )
    assert result.exit_code == 0
    assert "Download completed" in result.stdout
    assert YT_VIDEO_DEFAULT_AUDIO_NAME in os.listdir()
    cleanup.remove_media_files_and_empty_directories()


# $ ytxd audio --format <format> <url>
def test_download_audio_specified_format():
    for format in audio_formats:
        result = runner.invoke(
            app, ["audio", "--format", format, "--no-preview", YT_VIDEO_URL]
        )
        assert result.exit_code == 0
        assert "Download completed" in result.stdout
        assert YT_VIDEO_DEFAULT_AUDIO_NAME[:-3] + format in os.listdir()
        cleanup.remove_media_files_and_empty_directories()


# $ ytxd audio --path <downloads (new directory)> <url>
def test_download_audio_relative_path_new_directory():
    new_dir_name = "downloads"
    path_to_new_dir = os.path.join(os.getcwd(), new_dir_name)
    result = runner.invoke(
        app, ["audio", "--path", new_dir_name, "--no-preview", YT_VIDEO_URL]
    )
    assert result.exit_code == 0
    assert "Download completed" in result.stdout
    assert new_dir_name in os.listdir()
    assert os.path.isdir(path_to_new_dir)
    assert YT_VIDEO_DEFAULT_AUDIO_NAME in os.listdir(path_to_new_dir)
    cleanup.remove_media_files_and_empty_directories()


# $ytxd audio --path < <new_name>.<extansion> > <url>
def test_download_audio_specified_extansion():
    new_name_extansion = "effect.m4a"
    result = runner.invoke(
        app, ["audio", "-o", new_name_extansion, "--no-preview", YT_VIDEO_URL]
    )
    assert result.exit_code == 0
    assert "Download completed" in result.stdout
    assert new_name_extansion in os.listdir()
    cleanup.remove_media_files_and_empty_directories()


# $ytxd audio --path absolute_path_with_extansion> <url>
def test_download_audio_absolute_path_extansion():
    new_name_extansion = "effect.m4a"
    new_dir_name = "absolute"
    cwd = os.getcwd()
    new_path = os.path.join(os.path.join(cwd, new_dir_name), new_name_extansion)
    result = runner.invoke(
        app, ["audio", "--path", new_path, "--no-preview", YT_VIDEO_URL]
    )
    assert result.exit_code == 0
    assert "Download completed" in result.stdout
    assert new_dir_name in os.listdir()
    assert new_name_extansion in os.listdir(new_dir_name)
    cleanup.remove_media_files_and_empty_directories()


# $ ytxd audio <playlist url>
def test_download_audio_playlist():
    result = runner.invoke(app, ["audio", "--no-preview", YT_PLAYLIST_URL])
    assert result.exit_code == 0
    assert "Download failed" not in result.stdout
    for name in YT_PLAYLIST_DEFAULT_AUDIO_NAMES:
        assert name in os.listdir()
    cleanup.remove_media_files_and_empty_directories()


# $ ytxd audio -o <directory name> <playlist url>
def test_download_audio_playlist_new_dir():
    new_dir_name = "effect"
    result = runner.invoke(
        app, ["audio", "-o", new_dir_name, "--no-preview", YT_PLAYLIST_URL]
    )
    assert result.exit_code == 0
    assert new_dir_name in os.listdir()
    assert "Download failed" not in result.stdout
    for filename in YT_PLAYLIST_DEFAULT_AUDIO_NAMES:
        assert filename in os.listdir(new_dir_name)
    cleanup.remove_media_files_and_empty_directories()
