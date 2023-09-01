from dataclasses import dataclass
from typing import Optional

from battlebit_community_server_api.model.PlayerBody import PlayerBody
from battlebit_community_server_api.model.ReasonOfDamage import ReasonOfDamage
from battlebit_community_server_api.model.SteamId import SteamId
from battlebit_community_server_api.model.Vector3 import Vector3


@dataclass
class KillReport:
    killer: SteamId
    killer_pos: Vector3
    victim: SteamId
    victim_pos: Vector3
    tool_name: Optional[str]
    body_part: PlayerBody
    damage_reason: ReasonOfDamage
