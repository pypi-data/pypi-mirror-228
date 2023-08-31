import struct
from dataclasses import dataclass

from battlebit_community_server_api.model.PlayerLoadout import PlayerLoadout
from battlebit_community_server_api.model.PlayerSpawningPosition import PlayerSpawningPosition
from battlebit_community_server_api.model.PlayerStand import PlayerStand
from battlebit_community_server_api.model.PlayerWearings import PlayerWearings
from battlebit_community_server_api.model.Vector3 import Vector3


@dataclass
class PlayerSpawnArguments:
    position: PlayerSpawningPosition
    loadout: PlayerLoadout
    wearings: PlayerWearings
    vector_position: Vector3
    look_direction: Vector3
    stand: PlayerStand
    spawn_protection: float

    def to_bytes(self) -> bytes:
        out = self.position.as_bytes()
        out += self.loadout.as_bytes()
        out += self.wearings.as_bytes()
        out += self.vector_position.as_bytes()
        out += self.look_direction.as_bytes()
        out += self.stand.as_bytes()
        out += struct.pack("f", self.spawn_protection)

        return out
