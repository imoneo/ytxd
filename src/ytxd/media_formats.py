from enum import Enum


class Resolution(str, Enum):
    p360 = "360p"
    p480 = "480p"
    p720 = "720p"
    p1080 = "1080p"
    k2 = "2k"
    k4 = "4k"
    best = "best"


class VideoFormat(str, Enum):
    mp4 = "mp4"
    mkv = "mkv"
    # avi = "avi"
    # flv = "flv"


class AudioFormat(str, Enum):
    mp3 = "mp3"
    flac = "flac"
    wav = "wav"
    m4a = "m4a"


# Conversion function
def resolution_mapping(resolution: Resolution) -> str:
    """
    Map *resolution* string from Resolution enum to strings recognised by **yt-dlp**.
    """
    resolution_mapping = {
        Resolution.p360: "bestvideo[height<=360]+bestaudio/best",
        Resolution.p480: "bestvideo[height<=480]+bestaudio/best",
        Resolution.p720: "bestvideo[height<=720]+bestaudio/best",
        Resolution.p1080: "bestvideo[height<=1080]+bestaudio/best",
        Resolution.k2: "bestvideo[height<=1440]+bestaudio/best",  # 2K is 1440p
        Resolution.k4: "bestvideo[height<=2160]+bestaudio/best",  # 4K is 2160p
    }

    return resolution_mapping.get(resolution, "bestvideo+bestaudio/best")
