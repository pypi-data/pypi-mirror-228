from dataclasses import dataclass


@dataclass
class SteamId:
    steam_id: int

    def to_bytes(self) -> bytes:
        return int(self.steam_id).to_bytes(length=8, byteorder="little")

    def __str__(self) -> str:
        return f"{self.steam_id}"

    def __repr__(self) -> str:
        return f"{self.steam_id}"
