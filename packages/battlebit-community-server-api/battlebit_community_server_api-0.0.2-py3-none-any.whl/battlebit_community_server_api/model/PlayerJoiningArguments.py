import struct
from dataclasses import dataclass

from battlebit_community_server_api.model.PlayerStats import PlayerStats
from battlebit_community_server_api.model.Squads import Squads
from battlebit_community_server_api.model.Team import Team


@dataclass
class PlayerJoiningArguments:
    player_stats: PlayerStats
    team: Team
    squad: Squads

    def to_bytes(self) -> bytes:
        out = self.player_stats.to_bytes()
        out += struct.pack("B", self.team.value)
        out += struct.pack("B", self.squad.value)
        return out
