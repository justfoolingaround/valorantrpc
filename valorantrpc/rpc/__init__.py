import base64
import json
import threading
import time

import pypresence

from .states import pregame
from .states.ingame import playing, practice
from .states.mainmenu import custom, default, queue

PRESENCE_CLIENT_ID = 811469787657928704

rpc_client = pypresence.Presence(PRESENCE_CLIENT_ID)

rpc_client.connect()

close_event = threading.Event()


def start_rpc_client(
    client, refresh=3.0, *, close_event: threading.Event = close_event
):

    while not close_event.isSet():

        raw = client.fetch_current_user_presence()

        if raw is None:
            continue

        presence = json.loads(base64.b64decode(raw["private"]))

        loop_state = presence["sessionLoopState"]
        party_state = presence["partyState"]
        provisioning_flow = presence["provisioningFlow"]

        rpc_callback = None

        if loop_state == "MENUS":
            if party_state == "DEFAULT":
                rpc_callback = default.set_presence
            else:
                if party_state == "MATCHMAKING":
                    rpc_callback = queue.set_presence
                else:
                    rpc_callback = custom.set_presence
        else:
            if loop_state == "INGAME":
                if provisioning_flow == "ShootingRange":
                    rpc_callback = practice.set_presence
                else:
                    rpc_callback = playing.set_presence
            else:
                rpc_callback = pregame.set_presence

        rpc_callback(client.session, rpc_client, presence)

        time.sleep(refresh)
