import struct
from dataclasses import dataclass

from battlebit_community_server_api.model import Role
from battlebit_community_server_api.model.PlayerProgress import PlayerProgress


@dataclass
class PlayerStats:
    is_banned: bool
    roles: Role
    progress: PlayerProgress
    tool_progress: bytes
    achievements: bytes
    selections: bytes

    def to_bytes(self) -> bytes:
        out = struct.pack("B", self.is_banned)
        out += struct.pack("Q", self.roles)
        out += self.progress.to_bytes()
        out += struct.pack("H", len(self.tool_progress))
        out += self.tool_progress
        out += struct.pack("H", len(self.achievements))
        out += self.achievements
        out += struct.pack("H", len(self.selections))
        out += self.selections
        return out
