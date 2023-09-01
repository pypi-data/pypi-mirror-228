from dataclasses import dataclass
from typing import Optional

from battlebit_community_server_api.helper.StructHelper import *


@dataclass
class Gadget:
    name: str

    def as_bytes(self) -> bytes:
        return write_string(self.name)


def read_from_bytes(data: bytes) -> tuple[Optional[Gadget], bytes]:
    """ Reads from 0 until data is completed, returns remaining bytes """
    gadget_size, data = read_uint16(data)
    gadget_name, data = read_string(data, gadget_size)
    try:
        gadget = ALL_GADGETS[gadget_name]
    except KeyError:
        gadget = None
    return gadget, data


BANDAGE = Gadget("Bandage")
BINOCULARS = Gadget("Binoculars")
RANGE_FINDER = Gadget("Range Finder")
REPAIR_TOOL = Gadget("Repair Tool")
C4 = Gadget("C4")
CLAYMORE = Gadget("Claymore")
M320_SMOKE_GRENADE_LAUNCHER = Gadget("M320 Smoke Grenade Launcher")
SMALL_AMMO_KIT = Gadget("Small Ammo Kit")
ANTI_PERSONNEL_MINE = Gadget("Anti Personnel Mine")
ANTI_VEHICLE_MINE = Gadget("Anti Vehicle Mine")
MEDIC_KIT = Gadget("Medic Kit")
RPG7_HEAT_EXPLOSIVE = Gadget("Rpg7 Heat Explosive")
RIOT_SHIELD = Gadget("Riot Shield")
FRAG_GRENADE = Gadget("Frag Grenade")
IMPACT_GRENADE = Gadget("Impact Grenade")
ANTI_VEHICLE_GRENADE = Gadget("Anti Vehicle Grenade")
SMOKE_GRENADE_BLUE = Gadget("Smoke Grenade Blue")
SMOKE_GRENADE_GREEN = Gadget("Smoke Grenade Green")
SMOKE_GRENADE_RED = Gadget("Smoke Grenade Red")
SMOKE_GRENADE_WHITE = Gadget("Smoke Grenade White")
FLARE = Gadget("Flare")
SLEDGE_HAMMER = Gadget("Sledge Hammer")
ADVANCED_BINOCULARS = Gadget("Advanced Binoculars")
MDX201 = Gadget("Mdx 201")
BINO_SOFLAM = Gadget("Bino Soflam")
HEAVY_AMMO_KIT = Gadget("Heavy Ammo Kit")
RPG7_PGO7_TANDEM = Gadget("Rpg7 Pgo7 Tandem")
RPG7_PGO7_HEAT_EXPLOSIVE = Gadget("Rpg7 Pgo7 Heat Explosive")
RPG7_PGO7_FRAGMENTATION = Gadget("Rpg7 Pgo7 Fragmentation")
RPG7_FRAGMENTATION = Gadget("Rpg7 Fragmentation")
GRAPPLING_HOOK = Gadget("Grappling Hook")
AIR_DRONE = Gadget("Air Drone")
FLASHBANG = Gadget("Flashbang")
PICKAXE = Gadget("Pickaxe")
SUICIDE_C4 = Gadget("SuicideC4")
SLEDGE_HAMMER_SKIN_A = Gadget("Sledge Hammer SkinA")
SLEDGE_HAMMER_SKIN_B = Gadget("Sledge Hammer SkinB")
SLEDGE_HAMMER_SKIN_C = Gadget("Sledge Hammer SkinC")
PICKAXE_IRON_PICKAXE = Gadget("Pickaxe IronPickaxe")

ALL_GADGETS = {g.name: g for g in [
    BANDAGE,
    BINOCULARS,
    RANGE_FINDER,
    REPAIR_TOOL,
    C4,
    CLAYMORE,
    M320_SMOKE_GRENADE_LAUNCHER,
    SMALL_AMMO_KIT,
    ANTI_PERSONNEL_MINE,
    ANTI_VEHICLE_MINE,
    MEDIC_KIT,
    RPG7_HEAT_EXPLOSIVE,
    RIOT_SHIELD,
    FRAG_GRENADE,
    IMPACT_GRENADE,
    ANTI_VEHICLE_GRENADE,
    SMOKE_GRENADE_BLUE,
    SMOKE_GRENADE_GREEN,
    SMOKE_GRENADE_RED,
    SMOKE_GRENADE_WHITE,
    FLARE,
    SLEDGE_HAMMER,
    ADVANCED_BINOCULARS,
    MDX201,
    BINO_SOFLAM,
    HEAVY_AMMO_KIT,
    RPG7_PGO7_TANDEM,
    RPG7_PGO7_HEAT_EXPLOSIVE,
    RPG7_PGO7_FRAGMENTATION,
    RPG7_FRAGMENTATION,
    GRAPPLING_HOOK,
    AIR_DRONE,
    FLASHBANG,
    PICKAXE,
    SUICIDE_C4,
    SLEDGE_HAMMER_SKIN_A,
    SLEDGE_HAMMER_SKIN_B,
    SLEDGE_HAMMER_SKIN_C,
    PICKAXE_IRON_PICKAXE
]}
