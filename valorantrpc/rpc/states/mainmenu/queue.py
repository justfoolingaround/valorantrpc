from ...utils import (
    get_competitive_rank_information,
    get_gamemode_information,
    get_map_information,
    get_party_information,
    parse_datetime,
)


def set_presence(session, rpc_client, client_data):

    start_time = parse_datetime(client_data["queueEntryTime"])

    state, party_size = get_party_information(client_data)
    gamemode_icon, gamemode = get_gamemode_information(client_data)

    try:
        map_name, map_asset = get_map_information(session, client_data)
    except ValueError:
        map_name, map_asset = gamemode_icon, f"Queuing: {gamemode}"

    small_image, small_text = "game_icon", "VALORANT"

    if client_data["queueId"] == "competitive":
        small_image, small_text = get_competitive_rank_information(session, client_data)

    large_image, large_text = map_asset, (
        map_name if map_name != "discovery" else "LFG"
    )

    return rpc_client.update(
        state=state,
        details=f"In Queue - {gamemode} // {map_name}",
        small_image=small_image,
        small_text=small_text,
        large_image=large_image,
        large_text=large_text,
        party_size=party_size,
        start=start_time,
        party_id=client_data["partyId"],
    )
