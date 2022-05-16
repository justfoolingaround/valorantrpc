import functools
import time
from datetime import datetime

party_sizes = {
    1: "Solo",
    2: "Duo",
    3: "Trio",
}

forced_competitive_ranks = {}

game_modes = {
    "newmap": ("New Map", False),
    "competitive": ("Competitive", False),
    "unrated": ("Unrated", True),
    "spikerush": ("Spike Rush", True),
    "deathmatch": ("Deathmatch", True),
    "ggteam": ("Escalation", True),
    "onefa": ("Replication", True),
    "snowball": ("Snowball Fight", False),
}


RANK_UNKNOWN = (
    "https://media.valorant-api.com/competitivetiers/e4e9a692-288f-63ca-7835-16fbf6234fda/0/largeicon.png",
    "Unknown",
)


@functools.lru_cache()
def ranks(session):
    return session.get("https://valorant-api.com/v1/competitivetiers").json()["data"]


@functools.lru_cache()
def maps(session):
    return session.get("https://valorant-api.com/v1/maps").json()["data"]


@functools.lru_cache()
def agents(session):
    return session.get("https://valorant-api.com/v1/agents").json()["data"]


def get_party_information(data):

    party_size = data["partySize"]
    party = (party_size, data["maxPartySize"])
    party_state = ["Closed Party", "Open Party"][data["partyAccessibility"] == "OPEN"]

    return f"{party_sizes.get(party_size, 'In a party')} ({party_state})", party


def get_competitive_rank_information(
    session,
    data,
):
    if "force_rank" in forced_competitive_ranks:
        data.update({"competitiveTier": forced_competitive_ranks["force_rank"]})

    leaderboard_position = forced_competitive_ranks.get(
        "force_leaderboard", data["leaderboardPosition"]
    )

    for _ in ranks(session)[-1]["tiers"]:
        if data["competitiveTier"] == _["tier"]:
            return (
                _["largeIcon"],
                _["tierName"]
                + (
                    " // {}".format(leaderboard_position)
                    if leaderboard_position
                    else ""
                ),
            )

    return RANK_UNKNOWN


def get_map_information(session, data):

    game_map = data["matchMap"]

    if not game_map:
        raise ValueError("No map selected")

    for _ in maps(session):
        if game_map == _["mapUrl"]:
            return "{displayName} ({coordinates})".format_map(_), _["splash"]

    raise ValueError("Invalid data")


def get_gamemode_information(data):
    game_mode, has_icon = game_modes.get(data["queueId"], ("Custom", False))
    return f"mode_{data['queueId']}" if has_icon else "discovery", game_mode


def parse_datetime(datetime_string):
    return time.mktime(
        (datetime.strptime(datetime_string, "%Y.%m.%d-%H.%M.%S") + (datetime.now() - datetime.utcnow())).timetuple()
    )
