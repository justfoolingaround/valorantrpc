import os
import pathlib
import subprocess
import threading
import time

import click
import httpx
import rich
from black import err
from rich.traceback import install

from .cli.commands.utils.process import get_rcs_path, is_valorant_running
from .client import LOCALVALORANTClient
from .rpc import close_event, start_rpc_client
from .rpc.utils import forced_competitive_ranks

install(suppress=[click])

has_aborted = False


@click.command()
@click.option(
    "--run-valorant",
    is_flag=True,
    default=False,
    help="Wait until the VALORANT process starts and then start the RPC client.",
)
@click.option(
    "--lockfile",
    type=click.Path(exists=False, file_okay=False, dir_okay=False),
    default=None,
    help="Path to the default Riot Client's lockfile.",
)
@click.option(
    "--shortcut",
    is_flag=True,
    default=False,
    help="Create the RPC shortcut on your desktop, with the current set of options.",
)
@click.option(
    "--force-rank",
    type=click.IntRange(0, 24, clamp=True),
    default=None,
)
@click.option(
    "--force-leaderboard",
    type=int,
    default=None,
)
def run(run_valorant, lockfile, shortcut, force_rank, force_leaderboard):

    if force_leaderboard is not None:
        forced_competitive_ranks.update({"force_leaderboard": force_leaderboard})

    if force_rank is not None:
        forced_competitive_ranks.update({"force_rank": force_rank})

    console = rich.console.Console()

    running_state = is_valorant_running()
    valorant_process = None

    if not (run_valorant or running_state):
        raise RuntimeError(
            "Could not detect the VALORANT process, please make sure it is running or use `--run-valorant` to automatically start VALORANT."
        )

    if run_valorant:
        if not running_state:
            try:
                riot_client_services = get_rcs_path()
            except (FileNotFoundError, RuntimeError):
                raise RuntimeError(
                    "Could not find Riot Client's installation folder, is it installed?"
                )

            valorant_process = subprocess.Popen(
                [
                    riot_client_services.as_posix(),
                    "--launch-product=valorant",
                    "--launch-patchline=live",
                ]
            )

    http_client = httpx.Client(headers={"User-Agent": "VALORANT-RPC"}, verify=False)

    if lockfile is None:
        lockfile = (
            pathlib.Path(os.getenv("LOCALAPPDATA"))
            / "Riot Games"
            / "Riot Client"
            / "Config"
            / "lockfile"
        )
    else:
        lockfile = pathlib.Path(lockfile)

    while not lockfile.exists():
        console.print("[cyan]Waiting for Riot Client's lockfile to generate.[/cyan]")
        time.sleep(2.5)

    local_valorant_client = LOCALVALORANTClient(
        http_client, riot_clients_lockfile=lockfile
    )

    try:
        _ = local_valorant_client.fetch_active_alias()
    except httpx.HTTPError:
        raise RuntimeError(
            "Could not communicate with the local API, please try to restart RPC client or VALORANT."
        )

    if shortcut:
        import shlex
        import sys

        try:
            import winshell  # type: ignore
        except ImportError:
            raise RuntimeError(
                "Could not find the `winshell` module, please install it to create shortcuts."
            )

        desktop_shortcut = pathlib.Path(winshell.desktop()) / "VALORANT RPC.lnk"

        if desktop_shortcut.exists():
            desktop_shortcut.unlink()

        system_arguments = ["-m", "valorantrpc"] + sys.argv[1:]

        system_arguments.remove("--shortcut")

        winshell.CreateShortcut(
            desktop_shortcut.as_posix(),
            sys.executable,
            shlex.join(system_arguments),
            "",
            ("", 0),
            "VALORANT RPC Client",
        )

    def watch_for_deletion(lockfile, closing_event):

        main_thread = threading.main_thread()

        state = None

        while state is None or all(state):
            time.sleep(1)
            state = (
                lockfile.exists(),
                main_thread.is_alive(),
                not closing_event.is_set(),
            )

        lockfile, _, closing_event_state = state

        if lockfile ^ closing_event_state:
            error_message = "VALORANT has exited."
        else:
            if closing_event_state ^ has_aborted:
                error_message = "VALORANT has crashed."
            else:
                if has_aborted:
                    error_message = "The RPC client was signalled for closure."
                else:
                    error_message = (
                        "The RPC client suffered an exception during runtime."
                    )

        console.print(f"[red]{error_message}[/red]")

        return closing_event.set()

    thread = threading.Thread(
        target=watch_for_deletion, args=(lockfile, close_event)
    ).start()

    try:
        start_rpc_client(local_valorant_client, close_event=close_event)
    except RuntimeError:
        thread.join()
        raise

    if valorant_process is not None and valorant_process.poll() is None:
        console.print("[cyan]VALORANT child process is still running.[/cyan]")


def valorant_rpc(*args, **kwargs):
    global has_aborted

    try:
        return run(standalone_mode=False, *args, **kwargs)
    except click.Abort:
        has_aborted = True


if __name__ == "__main__":
    valorant_rpc()
