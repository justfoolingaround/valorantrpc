from ...utils import (
    get_party_information,
    get_gamemode_information,
    get_competitive_rank_information,
    parse_datetime,
)


def set_presence(session, rpc_client, client_data):

    start_time = parse_datetime(client_data["queueEntryTime"])

    state, party_size = get_party_information(client_data)
    gamemode_asset, gamemode = get_gamemode_information(client_data)

    if client_data["queueId"] == "competitive":
        large_image, large_text = get_competitive_rank_information(session, client_data)
    else:
        large_image, large_text = gamemode_asset, gamemode

    return rpc_client.update(
        state=state,
        details=f"In Queue - {gamemode}",
        small_image="game_icon",
        small_text="VALORANT",
        large_image=large_image,
        large_text=large_text,
        party_size=party_size,
        start=start_time,
        party_id=client_data["partyId"],
    )
