from pathlib import Path
import typer
from typing_extensions import Annotated
from rich import print, rule

from . import download, dependencies
from .media_formats import Resolution, VideoFormat, AudioFormat, resolution_mapping

app = typer.Typer(rich_markup_mode="rich", no_args_is_help=True)


def success() -> None:
    """Success print statement."""
    print(rule.Rule("Download [green]completed[/green]", style="green"))


def fail() -> None:
    """Download failed print statement."""
    print(rule.Rule("Download [red]failed[/red]", style="red"))


@app.command(
    help="Download [italic yellow]video[/italic yellow] from given [green bold]URL[/green bold]. [underline]Downloading from multiple URLs is allowed.[/underline]"
)
def video(
    url: Annotated[list[str], typer.Argument(help="Video URL")],
    path: Annotated[
        Path,
        typer.Option(
            "-o",
            "--path",
            help="Path to the downloaded video or playlist. If not declared, save to the current working directory.",
        ),
    ] = Path.cwd(),
    resolution: Annotated[
        Resolution,
        typer.Option(
            "--resolution",
            "--res",
            help="Video [bold green]resolution[/bold green]. If not available, the next closest resolution is used.",
        ),
    ] = Resolution.p1080,
    file_format: Annotated[
        VideoFormat,
        typer.Option(
            "--format",
            "--extension",
            "--ext",
            help="Video file [bold green]format[/bold green]. If not available, another format will be downloaded.",
        ),
    ] = VideoFormat.mp4,
    best: Annotated[
        bool,
        typer.Option(
            "--best",
            help="Download the [bold yellow]best[/bold yellow] audio and video quality available. [bold underline red]Ignores other options.[/bold underline red]",
        ),
    ] = False,
    no_preview: Annotated[
        bool,
        typer.Option("--no-preview", help="Do not open file explorer for preview."),
    ] = False,
):
    if not dependencies.check():
        fail()
        return
    for u in url:
        if not download.video(
            u, path, file_format, resolution_mapping(resolution), best
        ):
            fail()
            return
    if not no_preview:
        locate = not path.is_dir()
        typer.launch(str(path), locate=locate)
    success()


@app.command(
    help="Download [underline]only[/underline] [italic yellow]audio[/italic yellow] from the given [green bold]URL[/green bold]. [underline]Downloading from multiple URLs is allowed.[/underline]"
)
def audio(
    url: Annotated[
        list[str],
        typer.Argument(
            help="Download and extract audio from the given URL. Playlist [bold green]URLs[/bold green] are allowed."
        ),
    ],
    path: Annotated[
        Path,
        typer.Option(
            "-o",
            "--path",
            help="Path to save the downloaded audio file or playlist. If not provided, saves to the current working directory.",
        ),
    ] = Path.cwd(),
    file_format: Annotated[
        AudioFormat,
        typer.Option(
            "--format", "--extension", "--ext", help="Specify the audio file format."
        ),
    ] = AudioFormat.mp3,
    no_preview: Annotated[
        bool,
        typer.Option("--no-preview", help="Do not open file explorer for preview."),
    ] = False,
):
    if not dependencies.check():
        fail()
        return
    for u in url:
        if not download.audio(u, path, file_format):
            fail()
            return
    if not no_preview:
        locate = not path.is_dir()
        typer.launch(str(path), locate=locate)
    success()


@app.command(help="Retrieve information about video or videos from url.")
def info(
    url: Annotated[list[str], typer.Argument(help="Url to video or playlist.")],
    path: Annotated[
        Path, typer.Option("-o", "--path", help="Specify where to save informations.")
    ] = Path.cwd(),
    no_preview: Annotated[
        bool,
        typer.Option("--no-preview", help="Do not open file explorer for preview."),
    ] = False,
):
    if not dependencies.check():
        fail()
        return

    for u in url:
        if not download.info(u, path):
            fail()
            return

    if not no_preview:
        locate = not path.is_dir()
        typer.launch(str(path), locate=locate)
    success()
