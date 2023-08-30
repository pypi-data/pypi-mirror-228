import os
import shutil
import time
from typing import Optional

import rich
import typer
from rich.table import Table
from rich.text import Text
from typing_extensions import Annotated

from radops import __version__, settings
from radops.data_lake import (
    File,
    add_from_url,
    add_local_file,
    get_local_path,
    get_unsynced_files,
    list_local_files,
)
from radops.data_lake.cloud_ops import (
    file_exists_in_s3,
    list_files_and_folders,
)

app = typer.Typer()

datalake_app = typer.Typer()
app.add_typer(datalake_app, name="datalake")

config_app = typer.Typer()
app.add_typer(config_app, name="config")


def _y_n_prompt_loop(prompt: str) -> None:
    while True:
        y_or_n = typer.prompt(prompt + " [y/n]").lower()
        if y_or_n == "y":
            return
        if y_or_n == "n":
            rich.print("Exiting")
            raise typer.Exit()
        else:
            rich.print("[red]Please respond with 'y' or 'n'")


def version_callback(value):
    if value:
        rich.print(__version__)
        raise typer.Exit()


@app.callback()
def common(
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    pass


@datalake_app.command(name="ls")
def ls(folder: Annotated[Optional[str], typer.Argument()] = ""):
    """list all files in the datalake"""
    local_files = list_local_files()

    def _style(c):
        return "b" if os.path.join(folder, c) in local_files else "i"

    files, folders = list_files_and_folders(folder)
    folders = [Text(f"{f}/", style="yellow") for f in folders]
    files = [Text(f, style=f"{_style(f)} green") for f in files]

    rich.print(*(folders + files), sep="\t")


@datalake_app.command(name="purge-local-storage")
def purge_local_storage():
    unsynced_files = get_unsynced_files()
    for uid in unsynced_files:
        os.remove(get_local_path(uid))

    rich.print(f"Removed files {unsynced_files} from local storage.")


@datalake_app.command(name="info")
def info(uid: str):
    """display the info and lineage of the specified file"""
    f = File(uid)
    if not f.exists_in_cloud():
        rich.print(f"[red]File {uid} does not exist in the data lake.")
    else:
        f.print_info()


@datalake_app.command(name="add")
def add(path_or_url: str, uid: str, move: bool = False, copy: bool = False):
    if move and copy:
        rich.print("[red]Cannot set both --move and --copy")
        raise typer.Exit()
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        if move or copy:
            rich.print(
                "[red]Cannot use '--move' or '--copy' when adding a file from a url."
            )
            raise typer.Exit()
        add_from_url(url=path_or_url, output_uid=uid)
    else:
        if not os.path.exists(path_or_url):
            rich.print(
                f"[red] File {path_or_url} does not exist. First argument to `datalake add` must be"
                " either a url (starting with 'http' or 'htttps') or a local file."
            )
            raise typer.Exit()
        if (not move) and (not copy):
            while True:
                resp = typer.prompt(
                    "Enter 'move' if local file should be moved to local storage or 'copy' if it should be copied"
                )
                if resp not in ["move", "copy"]:
                    rich.print("[yellow]Invalid response")
                else:
                    break
            copy = resp == "copy"

        add_local_file(path=path_or_url, output_uid=uid, copy=copy)


@datalake_app.command(name="delete")
def delete(uid: str):
    f = File(uid)
    downstream_uids = f.get_all_downstream()
    if len(downstream_uids) != 0:
        _y_n_prompt_loop(
            f"The file {uid} has the following downstream dependencies: {downstream_uids}. "
            "Deleting will delete all of these. Continue?"
        )

    deleted = f.delete(cascade=True)
    rich.print(f"Succesfully deleted file(s) {deleted}")


@datalake_app.command(name="local-path")
def local_path(uid: str):
    local_path = File(uid).storage_path
    if not file_exists_in_s3(uid):
        rich.print(f"[yellow]File {uid} is not in the datalake.")
    elif local_path.exists():
        rich.print(local_path)
    else:
        rich.print(
            f"[yellow]File {uid} has not been downloaded. You can do this by running[/yellow]: ",
            f"radops datalake download {uid}",
        )


@datalake_app.command(name="download")
def download(uid: str):
    f = File(uid)
    if not f.exists_in_cloud():
        rich.print(f"[yellow]File {uid} is not in the datalake.")
        raise typer.Exit()
    elif f.exists_locally():
        rich.print(f"[yellow]File {uid} already exists locally.")
        raise typer.Exit()
    return File(uid).download_from_cloud()


@config_app.command(name="view")
def view():
    """Displays current `radops` configuration"""
    table = Table("setting", "value")
    for k, v in settings.model_dump().items():
        table.add_row(k, str(v))
    rich.print(table)


@config_app.command(name="setup")
def setup():
    """Sets up `radops` configuration"""
    env_path = settings.model_config["env_file"]
    backup_path = None
    if os.path.exists(env_path):
        _y_n_prompt_loop(
            f"configuration file already exists at {settings.model_config['env_file']}, overwrite?"
        )
        backup_path = str(env_path) + time.strftime("%Y%m%d-%H%M%S")
        rich.print(f"Backing up existing config to {backup_path}")
        shutil.move(env_path, backup_path)

    try:
        settings_dict = {}
        settings_dict["email"] = typer.prompt("Your e-mail address")
        settings_dict["s3_endpoint_url"] = typer.prompt("S3 URL")
        settings_dict["aws_access_key_id"] = typer.prompt("Access key")
        settings_dict["aws_secret_access_key"] = typer.prompt(
            "Secret access key", hide_input=True
        )
    except Exception as e:
        if backup_path is not None:
            rich.print("[yellow]Restoring configuration")
            shutil.move(backup_path, env_path)

        if not isinstance(e, KeyboardInterrupt):
            raise e

    with open(env_path, "w") as f:
        for k, v in settings_dict.items():
            f.write(f"{k}={v}\n")


if __name__ == "__main__":
    app()
