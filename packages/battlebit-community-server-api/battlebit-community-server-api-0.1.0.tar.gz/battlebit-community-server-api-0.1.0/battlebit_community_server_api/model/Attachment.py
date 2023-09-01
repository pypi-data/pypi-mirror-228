from dataclasses import dataclass

from battlebit_community_server_api.helper.StructHelper import write_string
from battlebit_community_server_api.model.AttachmentType import AttachmentType


@dataclass
class Attachment:
    name: str
    attachment_type: AttachmentType

    def as_bytes(self) -> bytes:
        return write_string(self.name)


# Barrels
BASIC = Attachment("Basic", AttachmentType.BARREL)
COMPENSATOR = Attachment("Compensator", AttachmentType.BARREL)
HEAVY = Attachment("Heavy", AttachmentType.BARREL)
LONG_BARREL = Attachment("Long_Barrel", AttachmentType.BARREL)
MUZZLE_BREAK = Attachment("Muzzle_Break", AttachmentType.BARREL)
RANGER = Attachment("Ranger", AttachmentType.BARREL)
SUPPRESSOR_LONG = Attachment("Suppressor_Long", AttachmentType.BARREL)
SUPPRESSOR_SHORT = Attachment("Suppressor_Short", AttachmentType.BARREL)
TACTICAL = Attachment("Tactical", AttachmentType.BARREL)
FLASH_HIDER = Attachment("Flash_Hider", AttachmentType.BARREL)
OSPREY_9 = Attachment("Osprey_9", AttachmentType.BARREL)
DGN_308 = Attachment("DGN-308", AttachmentType.BARREL)
VAMB_762 = Attachment("VAMB-762", AttachmentType.BARREL)
SDN_6762 = Attachment("SDN-6_762", AttachmentType.BARREL)
NT_4556 = Attachment("NT-4_556", AttachmentType.BARREL)

# Canted Sights
IRON_SIGHT = Attachment("Ironsight", AttachmentType.CANTED_SIGHT)
CANTED_RED_DOT = Attachment("Canted_Red_Dot", AttachmentType.CANTED_SIGHT)
FYOU_CANTED = Attachment("FYou_Canted", AttachmentType.CANTED_SIGHT)
HOLO_DOT = Attachment("Holo_Dot", AttachmentType.CANTED_SIGHT)

# Scope
_6X_SCOPE = Attachment("6x_Scope", AttachmentType.MAIN_SIGHT)
_8X_SCOPE = Attachment("8x_Scope", AttachmentType.MAIN_SIGHT)
_15X_SCOPE = Attachment("15x_Scope", AttachmentType.MAIN_SIGHT)
_20X_SCOPE = Attachment("20x_Scope", AttachmentType.MAIN_SIGHT)
PTR_40_HUNTER = Attachment("PTR-40_Hunter", AttachmentType.MAIN_SIGHT)
_1P78 = Attachment("1P78", AttachmentType.MAIN_SIGHT)
ACOG = Attachment("Acog", AttachmentType.MAIN_SIGHT)
M125 = Attachment("M_125", AttachmentType.MAIN_SIGHT)
PRISMA = Attachment("Prisma", AttachmentType.MAIN_SIGHT)
SLIP = Attachment("Slip", AttachmentType.MAIN_SIGHT)
PISTOL_DELTA_SIGHT = Attachment("Pistol_Delta_Sight", AttachmentType.MAIN_SIGHT)
PISTOL_RED_DOT = Attachment("Pistol_Red_Dot", AttachmentType.MAIN_SIGHT)
AIM_COMP = Attachment("Aim_Comp", AttachmentType.MAIN_SIGHT)
HOLOGRAPHIC = Attachment("Holographic", AttachmentType.MAIN_SIGHT)
KOBRA = Attachment("Kobra", AttachmentType.MAIN_SIGHT)
OKP7 = Attachment("OKP7", AttachmentType.MAIN_SIGHT)
PKAS = Attachment("PK-AS", AttachmentType.MAIN_SIGHT)
RED_DOT = Attachment("Red_Dot", AttachmentType.MAIN_SIGHT)
REFLEX = Attachment("Reflex", AttachmentType.MAIN_SIGHT)
STRIKEFIRE = Attachment("Strikefire", AttachmentType.MAIN_SIGHT)
RAZOR = Attachment("Razor", AttachmentType.MAIN_SIGHT)
FLIR = Attachment("Flir", AttachmentType.MAIN_SIGHT)
ECHO = Attachment("Echo", AttachmentType.MAIN_SIGHT)
TRI4X32 = Attachment("TRI4X32", AttachmentType.MAIN_SIGHT)
FYOU_SIGHT = Attachment("FYou_Sight", AttachmentType.MAIN_SIGHT)
HOLO_PK120 = Attachment("Holo_PK-120", AttachmentType.MAIN_SIGHT)
PISTOL_8X_SCOPE = Attachment("Pistol_8x_Scope", AttachmentType.MAIN_SIGHT)
BURRIS_AR332 = Attachment("BurrisAR332", AttachmentType.MAIN_SIGHT)
HS401G5 = Attachment("HS401G5", AttachmentType.MAIN_SIGHT)

# Top Scope
DELTA_SIGHT_TOP = Attachment("Delta_Sight_Top", AttachmentType.TOP_SIGHT)
RED_DOT_TOP = Attachment("Red_Dot_Top", AttachmentType.TOP_SIGHT)
C_Red_DOT_TOP = Attachment("C_Red_Dot_Top", AttachmentType.TOP_SIGHT)
FYOU_TOP = Attachment("FYou_Top", AttachmentType.TOP_SIGHT)

# Under Rails
ANGLED_GRIP = Attachment("Angled_Grip", AttachmentType.UNDER_RAIL)
BIPOD = Attachment("Bipod", AttachmentType.UNDER_RAIL)
VERTICAL_GRIP = Attachment("Vertical_Grip", AttachmentType.UNDER_RAIL)
STUBBY_GRIP = Attachment("Stubby_Grip", AttachmentType.UNDER_RAIL)
STABIL_GRIP = Attachment("Stabil_Grip", AttachmentType.UNDER_RAIL)
VERTICAL_SKELETON_GRIP = Attachment("Vertical_Skeleton_Grip", AttachmentType.UNDER_RAIL)
FABDTFG = Attachment("FAB-DTFG", AttachmentType.UNDER_RAIL)
MAGPUL_ANGLED = Attachment("Magpul_Angled", AttachmentType.UNDER_RAIL)
BCMGUN_FIGHTER = Attachment("BCM-Gun_Fighter", AttachmentType.UNDER_RAIL)
SHIFT_SHORT_ANGLED_GRIP = Attachment("Shift_Short_Angled_Grip", AttachmentType.UNDER_RAIL)
SE5_GRIP = Attachment("SE-5_Grip", AttachmentType.UNDER_RAIL)
RK6_FORE_GRIP = Attachment("RK-6_Foregrip", AttachmentType.UNDER_RAIL)
HERA_CQR_FRONT = Attachment("HeraCQR_Front", AttachmentType.UNDER_RAIL)
B25URK = Attachment("B-25URK", AttachmentType.UNDER_RAIL)
VTAC_UVG_TACTICAL_GRIP = Attachment("VTAC_UVG_TacticalGrip", AttachmentType.UNDER_RAIL)

# Side Rails
FLASHLIGHT = Attachment("Flashlight", AttachmentType.SIDE_RAIL)
RANGEFINDER = Attachment("Rangefinder", AttachmentType.SIDE_RAIL)
RED_LASER = Attachment("Redlaser", AttachmentType.SIDE_RAIL)
TACTICAL_FLASHLIGHT = Attachment("Tactical_Flashlight", AttachmentType.SIDE_RAIL)
GREEN_LASER = Attachment("Greenlaser", AttachmentType.SIDE_RAIL)
SEARCH_LIGHT = Attachment("Searchlight", AttachmentType.SIDE_RAIL)

# Bolts
BOLT_ACTION_A = Attachment("BOLT_Action_A", AttachmentType.BOLT)
BOLT_ACTION_B = Attachment("BOLT_Action_B", AttachmentType.BOLT)
BOLT_ACTION_C = Attachment("BOLT_Action_C", AttachmentType.BOLT)
BOLT_ACTION_D = Attachment("BOLT_Action_D", AttachmentType.BOLT)
BOLT_ACTION_E = Attachment("BOLT_Action_E", AttachmentType.BOLT)

ALL_ATTACHMENTS = {a.name: a for a in [BASIC, COMPENSATOR, HEAVY, LONG_BARREL, MUZZLE_BREAK, RANGER, SUPPRESSOR_LONG,
                                       SUPPRESSOR_SHORT, TACTICAL, FLASH_HIDER, OSPREY_9, DGN_308, VAMB_762, SDN_6762,
                                       NT_4556, IRON_SIGHT, CANTED_RED_DOT, FYOU_CANTED, HOLO_DOT, _6X_SCOPE,
                                       _8X_SCOPE, _15X_SCOPE, _20X_SCOPE, PTR_40_HUNTER, _1P78, ACOG, M125, PRISMA,
                                       SLIP, PISTOL_DELTA_SIGHT, PISTOL_RED_DOT, AIM_COMP, HOLOGRAPHIC, KOBRA, OKP7,
                                       PKAS, RED_DOT, REFLEX, STRIKEFIRE, RAZOR, FLIR, ECHO, TRI4X32, FYOU_SIGHT,
                                       HOLO_PK120, PISTOL_8X_SCOPE, BURRIS_AR332, HS401G5, DELTA_SIGHT_TOP,
                                       RED_DOT_TOP, C_Red_DOT_TOP, FYOU_TOP, ANGLED_GRIP, BIPOD, VERTICAL_GRIP,
                                       STUBBY_GRIP, STABIL_GRIP, VERTICAL_SKELETON_GRIP, FABDTFG, MAGPUL_ANGLED,
                                       BCMGUN_FIGHTER, SHIFT_SHORT_ANGLED_GRIP, SE5_GRIP, RK6_FORE_GRIP,
                                       HERA_CQR_FRONT, B25URK, VTAC_UVG_TACTICAL_GRIP, FLASHLIGHT, RANGEFINDER,
                                       RED_LASER, TACTICAL_FLASHLIGHT, GREEN_LASER, SEARCH_LIGHT, BOLT_ACTION_A,
                                       BOLT_ACTION_B, BOLT_ACTION_C, BOLT_ACTION_D, BOLT_ACTION_E]}
