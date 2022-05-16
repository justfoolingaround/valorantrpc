import json
import os
import pathlib

import psutil

VALORANT_PROCESSES = ["VALORANT-Win64-Shipping.exe", "RiotClientServices.exe"]


def is_running(process_name):

    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return True

    return False


def is_valorant_running():
    return all(is_running(process) for process in VALORANT_PROCESSES)


def get_rcs_path():

    installation_info = (
        pathlib.Path(os.getenv("PROGRAMDATA", "."))
        / "Riot Games"
        / "RiotClientInstalls.json"
    ).resolve(strict=True)

    with open(installation_info, "r") as installation_info_file:
        installations = json.load(installation_info_file)

    riot_client = installations.get("rc_default")

    if riot_client is None:
        raise RuntimeError("Could not find default Riot Client installation.")

    return pathlib.Path(riot_client).resolve()
