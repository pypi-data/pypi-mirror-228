from enum import IntEnum


class PlayerStand(IntEnum):
    STANDING = 0
    CROUCHING = 1
    PRONING = 2

    def as_bytes(self) -> bytes:
        return self.to_bytes(length=1, byteorder="little")
