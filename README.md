# **Y**ou**T**ube **X** **D**ownload (**_YTXD_**)

An easy to use wrapper around [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) CLI.

_**YTXD**_ is a command line tool that allows You to download from YouTube (or X, etc ...). The main purpose of _**YTXD**_ is to provide easy to use interface for downloading video or audio scores.

## Usage

### direct commands

```bash
# download video to current working directory
$ ytxd video <video-url>

# download audio score of video to current working directory
$ ytxd audio <video-url>

# download video or audio to path with given extansion and filename, path can be relative
$ ytxd video -o Videos/clip.mkv <video-url>

# download best quality avaiable
$ ytxd video --best <video-url>

# specify path, resolution and video format
$ ytxd video --resolution 720p --format flac --path ~/Downloads <video-url>
```

## Installation

**_ytxd_** is avaiable on _PyPI_:

```bash
pip install ytxd
```

Once installed, `ytxd` will be exposed as a command-line tool:

```bash
ytxd --help
```

_**ytxd**_ requires [`ffmpeg`](https://www.ffmpeg.org/) to run. `Ffmpeg` installation site [https://www.ffmpeg.org/download.html](https://www.ffmpeg.org/download.html) and/or commands:

```bash
# ubuntu / debian
$ sudo apt-get update && sudo apt-get install ffmpeg
```

```PowerShell
# windows 10/11
> winget install ffmpeg
```

### Recomendation

I suggest to use **_ytxd_** via [`uv`](https://docs.astral.sh/uv/), an extremely fast Python package and project manager, written in Rust..
After following guide and installing `uv` from [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/), **_ytxd_** can be used by typing command:

```bash
uvx ytxd --help
```
