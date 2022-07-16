from ...states import idle
from ...utils import (
    get_competitive_rank_information,
    get_gamemode_information,
    get_map_information,
    get_party_information,
)


def set_presence(session, rpc_client, client_data):

    if client_data["isIdle"]:
        return idle.set_presence(session, rpc_client, client_data)

    state, party_size = get_party_information(client_data)
    gamemode_asset, gamemode = get_gamemode_information(client_data)

    if client_data["queueId"] == "competitive":
        small_image, small_text = get_competitive_rank_information(session, client_data)
    else:
        small_image, small_text = gamemode_asset, gamemode

    try:
        large_image, large_text = get_map_information(session, client_data)
    except ValueError:
        large_image, large_text = "game_icon", "VALORANT"

    return rpc_client.update(
        state=state,
        details=f"Agent Selection - {gamemode}",
        large_image=large_image,
        large_text=large_text,
        small_image=small_image,
        small_text=small_text,
        party_size=party_size,
        party_id=client_data["partyId"],
    )
