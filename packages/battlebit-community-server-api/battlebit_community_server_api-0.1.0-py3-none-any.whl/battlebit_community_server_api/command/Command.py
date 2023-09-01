import logging
from dataclasses import dataclass
from typing import Optional

from battlebit_community_server_api.model.GameRole import GameRole
from battlebit_community_server_api.model.SteamId import SteamId
from battlebit_community_server_api.model.Team import Team
from battlebit_community_server_api.model.Squads import Squads
from battlebit_community_server_api.model.Map import Map
from battlebit_community_server_api.model.Gamemode import Gamemode


@dataclass
class Command:
    command_string: str
    arguments: list[str]

    def __len__(self) -> int:
        return len(self.as_string())

    def as_string(self) -> str:
        return f"{self.command_string} {' '.join(self.arguments).rstrip(' ')}".rstrip(' ')


class ForceStartGame(Command):
    def __init__(self) -> None:
        self.command_string = "forcestart"
        self.arguments = []


class ForceEndGame(Command):
    def __init__(self) -> None:
        self.command_string = "endgame"
        self.arguments = []


class SayToAllChat(Command):
    def __init__(self, message: str) -> None:
        self.command_string = "say"
        self.arguments = message.split(" ")


class SayToChat(Command):
    def __init__(self, message: str, target_steam_id: SteamId) -> None:
        self.command_string = "sayto"
        self.arguments = [str(target_steam_id.steam_id)]
        self.arguments += message.split(" ")


class SetRoleTo(Command):
    def __init__(self, steam_id: SteamId, role: GameRole) -> None:
        self.command_string = "setrole"
        self.arguments = [str(steam_id), str(role.value)]


class SetTeamTo(Command):
    def __init__(self, steam_id: SteamId, team: Team) -> None:
        self.command_string = "changeteam"
        self.arguments = [str(steam_id), "a" if team == Team.US else "b"]


class SetNewPassword(Command):
    def __init__(self, new_password: str) -> None:
        self.command_string = "setpass"
        self.arguments = [new_password]


class SetPingLimit(Command):
    def __init__(self, new_ping_limit: int) -> None:
        self.command_string = "setmaxping"
        self.arguments = [str(new_ping_limit)]


class AnnounceShort(Command):
    def __init__(self, announcement_text: str) -> None:
        self.command_string = "an"
        self.arguments = [announcement_text]


class AnnounceLong(Command):
    def __init__(self, announcement_text: str) -> None:
        self.command_string = "ann"
        self.arguments = [announcement_text]


class UILogOnServer(Command):
    def __init__(self, log_message: str, message_lifetime_seconds: float) -> None:
        self.command_string = "serverlog"
        self.arguments = [log_message, str(message_lifetime_seconds)]


class SetLoadingScreenText(Command):
    def __init__(self, new_loading_screen_text: str) -> None:
        self.command_string = "setloadingscreentext"
        self.arguments = [new_loading_screen_text]


class SetRulesScreenText(Command):
    def __init__(self, new_rules_screen_text: str) -> None:
        self.command_string = "setrulesscreentext"
        self.arguments = [new_rules_screen_text]


class StopServer(Command):
    def __init__(self) -> None:
        self.command_string = "stop"
        self.arguments = []


class CloseServer(Command):
    def __init__(self) -> None:
        self.command_string = "notifyend"
        self.arguments = []


class KickAllPlayers(Command):
    def __init__(self) -> None:
        self.command_string = "kick all"
        self.arguments = []


class KickPlayer(Command):
    def __init__(self, steam_id: SteamId, reason_for_kick: Optional[str] = "") -> None:
        self.command_string = "kick"
        self.arguments = [str(steam_id.steam_id), reason_for_kick]


class KillPlayer(Command):
    def __init__(self, steam_id: SteamId) -> None:
        self.command_string = "kill"
        self.arguments = [str(steam_id.steam_id)]


class SwapTeam(Command):
    def __init__(self, steam_id: SteamId) -> None:
        self.command_string = "changeteam"
        self.arguments = [str(steam_id.steam_id)]


class KickFromSquad(Command):
    def __init__(self, steam_id: SteamId) -> None:
        self.command_string = "squadkick"
        self.arguments = [str(steam_id.steam_id)]


class JoinSquad(Command):
    def __init__(self, steam_id: SteamId, squad: Squads) -> None:
        self.command_string = "setsquad"
        self.arguments = [str(steam_id.steam_id), squad.value]


class DisbandPlayerSquad(Command):
    def __init__(self, steam_id: SteamId) -> None:
        self.command_string = "squaddisband"
        self.arguments = [str(steam_id.steam_id)]


class PromoteSquadLeader(Command):
    def __init__(self, steam_id: SteamId) -> None:
        self.command_string = "squadpromote"
        self.arguments = [str(steam_id.steam_id)]


class WarnPlayer(Command):
    def __init__(self, steam_id: SteamId, warn_message: str) -> None:
        self.command_string = "warn"
        self.arguments = [str(steam_id.steam_id), warn_message]


class MessageToPlayer(Command):
    def __init__(self, steam_id: SteamId, message: str, fade_out_time_seconds: Optional[float] = None) -> None:
        if not fade_out_time_seconds:
            self.command_string = "msg"
            self.arguments = [str(steam_id.steam_id), message]
        else:
            self.command_string = "msgf"
            self.arguments = [str(steam_id.steam_id), str(fade_out_time_seconds), message]


class SetPlayerHp(Command):
    def __init__(self, steam_id: SteamId, hit_points: float) -> None:
        self.command_string = "sethp"
        self.arguments = [str(steam_id.steam_id), str(hit_points)]


class DamagePlayer(Command):
    def __init__(self, steam_id: SteamId, damage_amount: float) -> None:
        self.command_string = "givedamage"
        self.arguments = [str(steam_id.steam_id), str(damage_amount)]


class HealPlayer(Command):
    def __init__(self, steam_id: SteamId, heal_amount: float) -> None:
        self.command_string = "heal"
        self.arguments = [str(steam_id.steam_id), str(heal_amount)]


class SetSquadPoints(Command):
    def __init__(self, team: Team, squad: Squads, points: int) -> None:
        self.command_string = "setsquadpoints"
        self.arguments = [str(team.value), str(squad.value), str(points)]


class SetMapRotation(Command):
    def __init__(self, maps: list[Map]) -> None:
        if len(maps) > 8:
            logging.warning("Can not set more than 8 maps, trimming tail...")
            maps = maps[:8]
        self.command_string = "setmaprotation"
        self.arguments = [",".join(maps)]


class SetGamemodeRotation(Command):
    def __init__(self, gamemodes: list[Gamemode]) -> None:
        if len(gamemodes) > 8:
            logging.warning("Can not set more than 8 gamemodes, trimming tail...")
            gamemodes = gamemodes[:8]
        self.command_string = "setgamemoderotation"
        self.arguments = [",".join(gamemodes)]
