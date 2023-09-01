from enum import IntEnum


class Role(IntEnum):
    NONE = 0
    ADMIN = 1
    MODERATOR = 2
    SPECIAL = 4
    VIP = 8
