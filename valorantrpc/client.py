import base64
import json
import os
import pathlib
import platform

from .routes import Route

valorant_api = Route("GET", "https://valorant-api.com")


class LOCALVALORANTClient:
    def __init__(
        self,
        session,
        *,
        riot_clients_lockfile=pathlib.Path(os.getenv("LOCALAPPDATA"))
        / "Riot Games"
        / "Riot Client"
        / "Config"
        / "lockfile",
    ):
        self.session = session

        self.riot_clients_lockfile = riot_clients_lockfile.resolve(strict=True)

        (
            self.client_name,
            self.process_id,
            port,
            password,
            protocol,
        ) = self.riot_clients_lockfile.read_text().split(":")

        self._current_user = None

        self.local_api_client = Route(
            "GET", "{}://riot:{}@127.0.0.1:{}".format(protocol, password, port)
        )

    @property
    def user_platform(self):

        architecture, _ = platform.architecture()
        uname = platform.uname()

        return base64.b64encode(
            json.dumps(
                {
                    "platformType": "PC",
                    "platformOS": platform.system(),
                    "platformOSVersion": f"{platform.platform()}.1.256.{architecture}",
                    "platfromChipset": uname.processor,
                },
                indent=8,
            ).encode()
        ).decode()

    @property
    def current_version(self):
        version_data = valorant_api.act(self.session, endpoint="/v1/version").json()[
            "data"
        ]
        *_, version = version_data["version"].split(".")
        return f"{version_data['branch']}-shipping-{version_data['buildVersion']}-{version}"

    def iter_presences(self):

        for presence in self.local_api_client.act(
            self.session, endpoint="/chat/v4/presences"
        ).json()["presences"]:
            yield presence

    def fetch_sessions(self):
        return self.local_api_client.act(
            self.session, endpoint="/product-session/v1/external-sessions"
        ).json()

    def fetch_active_alias(self):

        if self._current_user is not None:
            return self._current_user

        response = {}

        while "game_name" not in response:
            response = self.local_api_client.act(
                self.session, endpoint="/player-account/aliases/v1/active"
            ).json()

        self._current_user = response
        return response

    def fetch_chat_session(self):
        return self.local_api_client.act(
            self.session, endpoint="/chat/v1/session"
        ).json()

    def fetch_all_friends(self):
        return self.local_api_client.act(
            self.session, endpoint="/chat/v4/friends"
        ).json()

    def fetch_player_settings(self):
        return self.local_api_client.act(
            self.session,
            endpoint="/player-preferences/v1/data-json/Ares.PlayerSettings",
        ).json()

    def fetch_friend_requests(self):
        return self.local_api_client.act(
            self.session, endpoint="/chat/v4/friendrequests"
        ).json()["requests"]

    def fetch_current_user_presence(self):

        current_user = self.fetch_active_alias()

        for _ in self.iter_presences():
            if (_["game_name"], _["game_tag"]) == (
                current_user["game_name"],
                current_user["tag_line"],
            ):
                return _
