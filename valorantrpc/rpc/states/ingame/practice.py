from ...utils import (
    get_competitive_rank_information,
    get_party_information,
    parse_datetime,
)
from .. import idle


def set_presence(session, rpc_client, client_data):

    if client_data["isIdle"]:
        return idle.set_presence(session, rpc_client, client_data)

    start_time = parse_datetime(client_data["queueEntryTime"])

    state, party_size = get_party_information(client_data)

    if client_data["queueId"] == "competitive":
        large_image, large_text = get_competitive_rank_information(session, client_data)
    else:
        large_image, large_text = "mode_unrated", "Killing the training dummies"

    return rpc_client.update(
        state=state,
        details="In Range",
        small_image="splash_range",
        small_text="VALORANT",
        large_image=large_image,
        large_text=large_text,
        party_size=party_size,
        start=start_time,
        party_id=client_data["partyId"],
    )
