from dataclasses import dataclass

from battlebit_community_server_api.model.LeaningSide import LeaningSide
from battlebit_community_server_api.model.LoadoutIndex import LoadoutIndex
from battlebit_community_server_api.model.PlayerStand import PlayerStand
from battlebit_community_server_api.model.SteamId import SteamId
from battlebit_community_server_api.model.Vector3 import Vector3


@dataclass
class PlayerState:
    steam_id: SteamId
    position: Vector3
    standing: PlayerStand
    leaning_side: LeaningSide
    loadout_index: LoadoutIndex
    is_in_seat: bool
    is_bleeding: bool
    ping: int
