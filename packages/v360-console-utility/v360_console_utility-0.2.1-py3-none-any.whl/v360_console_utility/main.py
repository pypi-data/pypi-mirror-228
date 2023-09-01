import typer
from typing import Optional
from typing_extensions import Annotated
from tabulate import tabulate

from .config import settings
from .nas import read_assets
from .console import upload_inward as console_upload_inward

app = typer.Typer()

@app.callback()
def callback():
    """
    V360 Console Utility
    """
    # typer.echo(f"{settings.nas_ip}")
    typer.echo("Welcome to V360 Console Utility")


@app.command()
def upload_inward(date: Annotated[Optional[str], typer.Argument()] = None,
                  inward: Annotated[Optional[str], typer.Argument()] = None):
    """
    Upload inward
    """
    if inward is None:
        inward = typer.prompt("Enter inward number")

    if date is None:
        date = typer.prompt("Enter date")

    typer.echo(f"Getting asset details for inward {inward} on date {date}")
    try:
        assets = read_assets(date, inward)
        if (len(assets) == 0):
            typer.echo(
                f"No assets found at the location {settings.nas_prefix}/{date}/{inward}")
            raise typer.Exit()
    except Exception as e:
        typer.echo(f"Error : {e}")
        raise typer.Exit()

    # print
    typer.echo(tabulate(list(map(lambda asset: [asset], assets))))
    typer.echo(
        f"Total {len(assets)} assets are scanned for inward {inward} on date {date}")

    sync = typer.confirm(
        "Are you sure you want to sync the upload status of this Inward?")
    if not sync:
        typer.echo(f"Operation cancelled.")
        raise typer.Exit()

    try:
        console_upload_inward(inward, assets)
        typer.echo(f"Done")
    except Exception as e:
        typer.echo(f"Error : {e}")
        raise typer.Exit()


if __name__ == "__main__":
    app()

state = {}
