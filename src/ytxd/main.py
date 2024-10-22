from pathlib import Path
import typer
from typing_extensions import Annotated
from rich import print, rule

from . import download, dependencies
from .media_formats import Resolution, VideoFormat, AudioFormat, resolution_mapping

app = typer.Typer(rich_markup_mode="rich", no_args_is_help=True)


def success():
    print(rule.Rule("Download [green]completed[/green]", style="green"))


def fail():
    print(rule.Rule("Download [red]failed[/red]", style="red"))


@app.command(
    help="Download [italic yellow]video[/italic yellow] from given [green bold]URL[/green bold]. [underline]Downloading from multiple urls is allowed.[/underline]"
)
def video(
    url: Annotated[list[str], typer.Argument(help="video url")],
    path: Annotated[
        Path,
        typer.Option(
            "-o",
            "--path",
            help="path to downloaded video or playlist, if not declared save to current working directory",
        ),
    ] = Path.cwd(),
    resolution: Annotated[
        Resolution,
        typer.Option(
            "--resolution",
            "--res",
            help="video [bold green]resolution[/bold green], if not avaiable the next close to decalred",
        ),
    ] = Resolution.p1080,
    file_format: Annotated[
        VideoFormat,
        typer.Option(
            "--format",
            "--extension",
            "--ext",
            help="video file [bold green]format[/bold green] if avaiable, otherwise download other",
        ),
    ] = VideoFormat.mp4,
    best: Annotated[
        bool,
        typer.Option(
            "--best",
            help="the [bold yellow]best[/bold yellow] audio and video quality avaiable, [bold underline red]ignore other options[/bold underline red]",
        ),
    ] = False,
):
    if dependencies.check():
        for u in url:
            download.video(u, path, file_format, resolution_mapping(resolution), best)
        # if best:
        #     for u in url:
        #         download.video_best(u, path, "mkv")
        # else:
        #     for u in url:
        #         download.video(
        #             u, path, file_format, resolution=resolution_mapping(resolution)
        #         )
        if path.is_dir():
            typer.launch(str(path), locate=False)
        else:
            typer.launch(str(path), locate=True)
        success()
    else:
        fail()


@app.command(
    help="Download [underline]only[/underline] [italic yellow]audio[/italic yellow] from given [green bold]URL[/green bold]. [underline]Downloading from multiple urls is allowed.[/underline]"
)
def audio(
    url: Annotated[
        list[str],
        typer.Argument(
            help="Download and extract audio from given url. Playlist [bold green]urls[/bold green] allowed."
        ),
    ],
    path: Annotated[
        Path,
        typer.Option(
            "-o",
            "--path",
            help="path to downloaded audio file or playlist, if not declared save to current working directory",
        ),
    ] = Path.cwd(),
    file_format: Annotated[
        AudioFormat,
        typer.Option(
            "--format", "--extansion", "--ext", help="Specify audio file format"
        ),
    ] = AudioFormat.mp3,
):
    if dependencies.check():
        for u in url:
            download.audio(u, path, file_format)
        if path.is_dir():
            typer.launch(str(path), locate=False)
        else:
            typer.launch(str(path), locate=True)
        success()
    else:
        fail()


# if __name__ == "__main__":
#     app()
