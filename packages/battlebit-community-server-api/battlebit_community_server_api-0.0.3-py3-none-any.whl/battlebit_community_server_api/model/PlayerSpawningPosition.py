from enum import IntEnum


class PlayerSpawningPosition(IntEnum):
    SPAWN_AT_POINT = 0
    SPAWN_AT_RALLY = 1
    SPAWN_AT_FRIEND = 2
    SPAWN_AT_VEHICLE = 3
    NONE = 4

    def as_bytes(self) -> bytes:
        return self.to_bytes(length=1, byteorder="little")
