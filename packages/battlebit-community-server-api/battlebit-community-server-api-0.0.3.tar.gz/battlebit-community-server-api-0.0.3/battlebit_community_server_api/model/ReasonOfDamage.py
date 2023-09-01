from enum import IntEnum


class ReasonOfDamage(IntEnum):
    SERVER = 0
    WEAPON = 1
    BLEEDING = 2
    FALL = 3
    HELICOPTER_BLADE = 4
    VEHICLE_EXPLOSION = 5
    EXPLOSION = 6
    VEHICLE_RUNOVER = 7
    BUILDING_COLLAPSING = 8
    SLEDGEHAMMER = 9
    TREE_FALL = 10
    COUNT_AS_KILL = 11
    SUICIDE = 12
    HELICOPTER_CRASH = 13
    BARBED_WIRE = 14
