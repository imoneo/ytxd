import yt_dlp
from pathlib import Path
from rich import print

from . import url
from .media_formats import AudioFormat, VideoFormat, Resolution, resolution_mapping

ALLOWED_VIDEO_FORMATS = [video_format.value for video_format in VideoFormat]
ALLOWED_AUDIO_FORMAT = [audio_format.value for audio_format in AudioFormat]


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


def video(
    url_adress: str,
    path: Path = Path.cwd(),
    file_format: str = VideoFormat.mp4,
    resolution: str = resolution_mapping(Resolution.p1080),
    best: bool = False,
) -> None:
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
    except Exception as e:
        print(f"Download error: {e}")


def audio(
    url_adress: str, path: Path = Path.cwd(), audio_format: str = AudioFormat.mp3
) -> None:
    """
    Download audio track from *url_adress* leading to single video or playlist.
    If *path* parameter contains suffix with valid file format, this format will overide *file_format* parameter.
    """
    is_playlist = url.is_youtube_playlist(url_adress)
    url_adress = url_adress if is_playlist else url.remove_playlist_context(url_adress)

    (output_path, audio_format) = define_path_and_file_format_audio(
        path, audio_format, is_playlist
    )  # type: ignore

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

    except Exception as e:
        print(f"Error: {e}")
