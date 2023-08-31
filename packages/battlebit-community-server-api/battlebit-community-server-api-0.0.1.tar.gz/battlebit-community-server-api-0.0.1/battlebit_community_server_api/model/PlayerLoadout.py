import struct
from dataclasses import dataclass

from battlebit_community_server_api.helper.StructHelper import read_uint8
from battlebit_community_server_api.model.Gadget import read_from_bytes as build_gadget, Gadget
from battlebit_community_server_api.model.WeaponItem import read_from_bytes as build_weapon_item, WeaponItem


@dataclass
class PlayerLoadout:
    primary_weapon: WeaponItem
    secondary_weapon: WeaponItem

    first_aid: Gadget
    light_gadget: Gadget
    heavy_gadget: Gadget
    throwable: Gadget

    primary_extra_magazine: int
    secondary_extra_magazine: int
    first_aid_extra: int
    light_gadget_extra: int
    heavy_gadget_extra: int
    throwable_extra: int

    def as_bytes(self) -> bytes:
        out = self.primary_weapon.as_bytes()
        out += self.secondary_weapon.as_bytes()
        out += self.first_aid.as_bytes()
        out += self.light_gadget.as_bytes()
        out += self.heavy_gadget.as_bytes()
        out += self.throwable.as_bytes()
        out += struct.pack("B", self.primary_extra_magazine)
        out += struct.pack("B", self.secondary_extra_magazine)
        out += struct.pack("B", self.first_aid_extra)
        out += struct.pack("B", self.light_gadget_extra)
        out += struct.pack("B", self.heavy_gadget_extra)
        out += struct.pack("B", self.throwable_extra)
        return out


def read_from_bytes(data: bytes) -> tuple[PlayerLoadout, bytes]:
    """ Parses bytes and returns PlayerLoadout and remaining bytes """
    primary_weapon, data = build_weapon_item(data)
    secondary_weapon, data = build_weapon_item(data)
    first_aid, data = build_gadget(data)
    light_gadget, data = build_gadget(data)
    heavy_gadget, data = build_gadget(data)
    throwable, data = build_gadget(data)
    primary_mags, data = read_uint8(data)
    secondary_mags, data = read_uint8(data)
    first_aid_extra, data = read_uint8(data)
    light_gadget_extra, data = read_uint8(data)
    heavy_gadget_extra, data = read_uint8(data)
    throwable_extra, data = read_uint8(data)
    player_loadout = PlayerLoadout(primary_weapon=primary_weapon,
                                   secondary_weapon=secondary_weapon,
                                   first_aid=first_aid,
                                   light_gadget=light_gadget,
                                   heavy_gadget=heavy_gadget,
                                   throwable=throwable,
                                   primary_extra_magazine=primary_mags,
                                   secondary_extra_magazine=secondary_mags,
                                   first_aid_extra=first_aid_extra,
                                   light_gadget_extra=light_gadget_extra,
                                   heavy_gadget_extra=heavy_gadget_extra,
                                   throwable_extra=throwable_extra)
    return player_loadout, data
