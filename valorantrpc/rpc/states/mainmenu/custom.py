from ...utils import (
    get_party_information,
    get_map_information,
)

from ...states import idle


custom_game_states = {
    "TeamOne": "Defending",
    "TeamTwo": "Attacking",
    "TeamSpectate": "Spectating",
    "TeamOneCoaches": "Coaching defenders",
    "TeamTwoCoaches": "Coaching attackers",
}


def set_presence(session, rpc_client, client_data):

    if client_data["isIdle"]:
        return idle.set_presence(session, rpc_client, client_data)

    state, party_size = get_party_information(client_data)
    gamemap, gamemap_asset = get_map_information(session, client_data)

    team = client_data["customGameTeam"]

    small_text = custom_game_states.get(team, "Playing customs")

    if team in ["TeamOne", "Red"]:
        small_image = "team_defender"
    else:
        small_image = "team_attacker"

    return rpc_client.update(
        state=state,
        details="CUSTOM",
        large_image=gamemap_asset,
        large_text=gamemap,
        small_image=small_image,
        small_text=small_text,
        party_size=party_size,
        party_id=client_data["partyId"],
    )
