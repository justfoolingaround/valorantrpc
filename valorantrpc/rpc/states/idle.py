from ..utils import get_gamemode_information


def set_presence(session, rpc_client, client_data):

    _asset, gamemode = get_gamemode_information(client_data)

    return rpc_client.update(
        details=gamemode,
        state="Away",
        large_image="game_icon_yellow",
        large_text="VALORANT",
    )
