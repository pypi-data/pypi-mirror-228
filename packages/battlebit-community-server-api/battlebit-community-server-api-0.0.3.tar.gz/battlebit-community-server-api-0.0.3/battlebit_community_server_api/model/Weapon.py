from dataclasses import dataclass

from battlebit_community_server_api.helper.StructHelper import write_string
from battlebit_community_server_api.model.WeaponType import WeaponType


@dataclass
class Weapon:
    name: str
    weapon_type: WeaponType

    def as_bytes(self) -> bytes:
        return write_string(self.name)


ACR = Weapon("ACR", WeaponType.RIFLE)
AK15 = Weapon("AK15", WeaponType.RIFLE)
AK74 = Weapon("AK74", WeaponType.RIFLE)
G36C = Weapon("G36C", WeaponType.RIFLE)
HONEY_BADGER = Weapon("Honey Badger", WeaponType.PERSONAL_DEFENSE_WEAPON)
KRISS_VECTOR = Weapon("Kriss Vector", WeaponType.SUB_MACHINE_GUN)
L86A1 = Weapon("L86A1", WeaponType.LIGHT_SUPPORT_GUN)
L96 = Weapon("L96", WeaponType.SNIPER_RIFLE)
M4A1 = Weapon("M4A1", WeaponType.RIFLE)
M9 = Weapon("M9", WeaponType.PISTOL)
M110 = Weapon("M110", WeaponType.DMR)
M249 = Weapon("M249", WeaponType.LIGHT_MACHINE_GUN)
MK14EBR = Weapon("MK14 EBR", WeaponType.DMR)
MK20 = Weapon("MK20", WeaponType.DMR)
MP7 = Weapon("MP7", WeaponType.SUB_MACHINE_GUN)
PP2000 = Weapon("PP2000", WeaponType.SUB_MACHINE_GUN)
SCAR_H = Weapon("SCAR-H", WeaponType.RIFLE)
SSG69 = Weapon("SSG 69", WeaponType.SNIPER_RIFLE)
SV98 = Weapon("SV-98", WeaponType.SNIPER_RIFLE)
UMP45 = Weapon("UMP-45", WeaponType.SUB_MACHINE_GUN)
UNICA = Weapon("Unica", WeaponType.HEAVY_PISTOL)
USP = Weapon("USP", WeaponType.PISTOL)
AS_VAL = Weapon("As Val", WeaponType.CARBINE)
AUG_A3 = Weapon("AUG A3", WeaponType.RIFLE)
DESERT_EAGLE = Weapon("Desert Eagle", WeaponType.HEAVY_PISTOL)
FAL = Weapon("FAL", WeaponType.RIFLE)
GLOCK_18 = Weapon("Glock 18", WeaponType.AUTO_PISTOL)
M200 = Weapon("M200", WeaponType.SNIPER_RIFLE)
MP443 = Weapon("MP 443", WeaponType.PISTOL)
FAMAS = Weapon("FAMAS", WeaponType.RIFLE)
MP5 = Weapon("MP5", WeaponType.SUB_MACHINE_GUN)
P90 = Weapon("P90", WeaponType.PERSONAL_DEFENSE_WEAPON)
MSR = Weapon("MSR", WeaponType.SNIPER_RIFLE)
PP19 = Weapon("PP19", WeaponType.SUB_MACHINE_GUN)
SVD = Weapon("SVD", WeaponType.DMR)
REM_700 = Weapon("Rem700", WeaponType.SNIPER_RIFLE)
SG550 = Weapon("SG550", WeaponType.RIFLE)
GROZA = Weapon("Groza", WeaponType.PERSONAL_DEFENSE_WEAPON)
HK419 = Weapon("HK419", WeaponType.RIFLE)
SCORPION_EVO = Weapon("ScorpionEVO", WeaponType.CARBINE)
RSH_12 = Weapon("Rsh12", WeaponType.HEAVY_PISTOL)
MG36 = Weapon("MG36", WeaponType.LIGHT_SUPPORT_GUN)
AK5C = Weapon("AK5C", WeaponType.RIFLE)
ULTIMAX_100 = Weapon("Ultimax100", WeaponType.LIGHT_MACHINE_GUN)

ALL_WEAPONS = {w.name: w for w in [ACR, AK15, AK74, G36C, HONEY_BADGER, KRISS_VECTOR, L86A1, L96, M4A1, M9, M110, M249,
                                   MK14EBR, MK20, MP7, PP2000, SCAR_H, SSG69, SV98, UMP45, UNICA, USP, AS_VAL, AUG_A3,
                                   DESERT_EAGLE, FAL, GLOCK_18, M200, MP443, FAMAS, MP5, P90, MSR, PP19, SVD, REM_700,
                                   SG550, GROZA, HK419, SCORPION_EVO, RSH_12, MG36, AK5C, ULTIMAX_100]}
