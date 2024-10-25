import json
import yt_dlp
from pathlib import Path
from rich import print
from slugify import slugify

from . import url
from .media_formats import AudioFormat, VideoFormat, Resolution, resolution_mapping

import logging

ALLOWED_VIDEO_FORMATS = tuple([video_format.value for video_format in VideoFormat])
ALLOWED_AUDIO_FORMAT = tuple([audio_format.value for audio_format in AudioFormat])


def define_path_and_file_format_video(
    path: Path, file_format: str, is_playlist: bool
) -> tuple[Path, str] | tuple[None, None]:
    """
    Returns valid path to **soon** downloaded video file, if it is possible
    defines **new file format** from provided path, otherwise *file_format* parameter value is set.
    """
    try:
        if is_playlist:
            changed_file_format = "mp4"
            changed_path = path.with_suffix("") / f"%(title)s.%(ext)s"  # noqa: F541
            return (changed_path, changed_file_format)

        if path.suffix:
            if path.suffix[1:] in ALLOWED_VIDEO_FORMATS:
                changed_file_format = path.suffix[1:]
            else:
                changed_file_format = "mp4"
            return (path, changed_file_format)

        else:
            changed_path = path / f"%(title)s.%(ext)s"  # noqa: F541
            return (changed_path, file_format)

    except Exception as e:
        print(f"An exception occured: {e}")
        logging.error(
            f"define_path_and_file_format_video(); path: {path}, file_format: {file_format}, is_playlist: {is_playlist}"
        )
        return (None, None)


def define_path_and_file_format_audio(path: Path, file_format: str, is_playlist: bool):
    """
    Returns valid path to **soon** downloaded audio file, if it is possible
    defines **new file format** from provided path, otherwise *file_format* parameter value is set.
    """
    try:
        if is_playlist:
            changed_file_format = "mp3"
            changed_path = path.with_suffix("") / f"%(title)s"  # noqa: F541
            return (changed_path, changed_file_format)

        if path.suffix:
            if path.suffix[1:] in ALLOWED_AUDIO_FORMAT:
                changed_file_format = path.suffix[1:]
            else:
                changed_file_format = "mp3"
            changed_path = path.with_suffix("")
            return (changed_path, changed_file_format)
        else:
            changed_path = path / f"%(title)s"  # noqa: F541
            return (changed_path, file_format)

    except Exception as e:
        print(f"An exception occured: {e}")
        logging.error(
            f"define_path_and_file_format_audio(); path: {path}, file_format: {file_format}, is_playlist: {is_playlist}"
        )
        return (None, None)


def video(
    url_adress: str,
    path: Path = Path.cwd(),
    file_format: str = VideoFormat.mp4,
    resolution: str = resolution_mapping(Resolution.p1080),
    best: bool = False,
) -> bool:
    """
    Download video or playlist from *url_adress* to *path*.
    If path contains suffix with avaiable video format, this format will overide *file_format* parameter.
    *Best* set true will download best quality avaiable file with .mkv extansion.
    """
    is_playlist = url.is_youtube_playlist(url_adress)
    url_adress = url_adress if is_playlist else url.remove_playlist_context(url_adress)

    (output_path, file_format) = define_path_and_file_format_video(
        path, file_format, is_playlist
    )  # type: ignore
    if (output_path, file_format) == (None, None):
        return False

    ydl_opts = (
        {
            "format": "bestvideo+bestaudio",  # download the beat audio and video, and merge them afterwards if necessary
            "outtmpl": str(output_path),
            "merge_output_format": VideoFormat.mkv,  # mkv as a format of choice, because of wide codecs support and open-source nature
        }
        if best
        else {
            "format": resolution,
            "outtmpl": str(output_path),
            "merge_output_format": file_format,
        }
    )
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # info_dict = ydl.extract_info(url_adress, download=True)  # Extract and download
            ydl.extract_info(url_adress, download=True)
        return True
    except Exception as e:
        print(f"Download error: {e}")
        logging.error("video()")
        return False


def audio(
    url_adress: str, path: Path = Path.cwd(), audio_format: str = AudioFormat.mp3
) -> bool:
    """
    Download audio track from *url_adress* leading to single video or playlist.
    If *path* parameter contains suffix with valid file format, this format will overide *file_format* parameter.
    """
    is_playlist = url.is_youtube_playlist(url_adress)
    url_adress = url_adress if is_playlist else url.remove_playlist_context(url_adress)

    (output_path, audio_format) = define_path_and_file_format_audio(
        path, audio_format, is_playlist
    )  # type: ignore

    if (output_path, audio_format) == (None, None):
        return False
    ydl_opts = {
        "format": "bestaudio/best",  # Download the best available audio
        "outtmpl": str(output_path),
        "postprocessors": [
            {  # Convert to the specified audio format
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                "preferredquality": "best",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url_adress, download=True)
        return True

    except Exception as e:
        print(f"Error: {e}")
        logging.error("audio()")
        return False


def define_path_informations(path: Path, filename: str) -> Path | None:
    """Create a path for json file with name that is valid."""
    try:
        json_file_name = f"{slugify(filename)}.json"
        path = path.expanduser()  # expand '~' if necessary

        if path.is_absolute():
            if path.suffix == "" and not path.is_dir():
                path.mkdir(parents=True, exist_ok=False)
                return path / json_file_name
            if path.suffix != "" and not path.exists():
                parent_dir = path.parent
                parent_dir.mkdir(
                    parents=True,
                    exist_ok=True,
                )
                return path.with_suffix(".json")

        # path is relative, dir does not exist
        if path.suffix == "" and not path.is_dir():
            new_dir_path = Path.cwd() / path
            new_dir_path.mkdir(parents=True, exist_ok=False)
            output_path = new_dir_path / json_file_name
            return output_path

        if path.suffix != "":
            return path.with_suffix(".json")

        return path / json_file_name
    except Exception as e:
        print(f"An exception occured: {e}")
        logging.error(f"define_path_informations(); path: {path}, filename: {filename}")


def info(url_adress: str, path: Path = Path.cwd()) -> bool:
    """Retrieve information about video from *url_adress* into json file."""
    try:
        ydl_opts = {}
        info_dict = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extracting video information
            info_dict = ydl.extract_info(url_adress, download=False)

        if info_dict is None:
            raise ValueError("Failed to retrieve video information: info_dict is None")
        output_path = define_path_informations(path, info_dict["title"])
        with open(str(output_path), "w") as file:
            json.dump(info_dict, file)
        return True
    except Exception as e:
        print(f"An error occured: {e}")
        logging.error(f"info(); url_adress: {url_adress} ,path: {path}")
        return False
