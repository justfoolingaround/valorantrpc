from ...utils import (
    get_party_information,
    get_gamemode_information,
    get_competitive_rank_information,
)

from ...states import idle


def set_presence(session, rpc_client, client_data):

    if client_data["isIdle"]:
        return idle.set_presence(session, rpc_client, client_data)

    state, party_size = get_party_information(client_data)
    gamemode_asset, gamemode = get_gamemode_information(client_data)

    if client_data["queueId"] == "competitive":
        small_image, small_text = get_competitive_rank_information(session, client_data)
    else:
        small_image, small_text = gamemode_asset, gamemode

    return rpc_client.update(
        state=state,
        details=f"Agent Selection - {gamemode}",
        large_image="game_icon",
        large_text="VALORANT",
        small_image=small_image,
        small_text=small_text,
        party_size=party_size,
        party_id=client_data["partyId"],
    )
