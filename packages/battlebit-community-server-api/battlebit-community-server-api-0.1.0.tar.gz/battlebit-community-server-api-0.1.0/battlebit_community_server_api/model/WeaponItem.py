from dataclasses import dataclass
from typing import Optional

from battlebit_community_server_api.helper.StructHelper import *
from battlebit_community_server_api.model.Attachment import Attachment, ALL_ATTACHMENTS
from battlebit_community_server_api.model.Weapon import Weapon, ALL_WEAPONS


@dataclass
class WeaponItem:
    base_weapon: Weapon
    main_sight: Optional[Attachment]
    top_sight: Optional[Attachment]
    canted_sight: Optional[Attachment]
    barrel: Optional[Attachment]
    side_rail: Optional[Attachment]
    under_rail: Optional[Attachment]
    bolt_action: Optional[Attachment]
    skin: Optional[int]
    magazine: Optional[int]

    def as_bytes(self) -> bytes:
        out = self.base_weapon.as_bytes()
        for attachment in [self.main_sight, self.top_sight, self.canted_sight, self.barrel, self.side_rail, self.under_rail, self.bolt_action]:
            if attachment:
                out += attachment.as_bytes()
            else:
                out += struct.pack("H", 4)
                out += "none".encode("utf-8")
        out += struct.pack("B", self.skin) if self.skin else struct.pack("B", 0)
        out += struct.pack("B", self.magazine) if self.magazine else struct.pack("B", 0)
        return out


def read_from_bytes(data: bytes) -> tuple[WeaponItem, bytes]:
    """ Reads from 0 until data is completed, returns remaining bytes """
    weapon_name_size, data = read_uint16(data)
    weapon_name, data = read_string(data, weapon_name_size)
    try:
        weapon = ALL_WEAPONS[weapon_name]
    except KeyError:
        weapon = ALL_WEAPONS["M4A1"]  # ToDo: Make configurable

    main_sight_size, data = read_uint16(data)
    main_sight_name, data = read_string(data, main_sight_size)
    try:
        main_sight = ALL_ATTACHMENTS[main_sight_name]
    except KeyError:
        main_sight = None

    top_sight_size, data = read_uint16(data)
    top_sight_name, data = read_string(data, top_sight_size)
    try:
        top_sight = ALL_ATTACHMENTS[top_sight_name]
    except KeyError:
        top_sight = None

    canted_sight_size, data = read_uint16(data)
    canted_sight_name, data = read_string(data, canted_sight_size)
    try:
        canted_sight = ALL_ATTACHMENTS[canted_sight_name]
    except KeyError:
        canted_sight = None

    barrel_size, data = read_uint16(data)
    barrel_name, data = read_string(data, barrel_size)
    try:
        barrel = ALL_ATTACHMENTS[barrel_name]
    except KeyError:
        barrel = None

    side_rail_size, data = read_uint16(data)
    side_rail_name, data = read_string(data, side_rail_size)
    try:
        side_rail = ALL_ATTACHMENTS[side_rail_name]
    except KeyError:
        side_rail = None

    under_rail_size, data = read_uint16(data)
    under_rail_name, data = read_string(data, under_rail_size)
    try:
        under_rail = ALL_ATTACHMENTS[under_rail_name]
    except KeyError:
        under_rail = None

    bolt_action_size, data = read_uint16(data)
    bolt_action_name, data = read_string(data, bolt_action_size)
    try:
        bolt_action = ALL_ATTACHMENTS[bolt_action_name]
    except KeyError:
        bolt_action = None

    skin_index, data = read_uint8(data)
    magazine_index, data = read_uint8(data)

    return WeaponItem(base_weapon=weapon,
                      main_sight=main_sight,
                      top_sight=top_sight,
                      canted_sight=canted_sight,
                      barrel=barrel,
                      side_rail=side_rail,
                      under_rail=under_rail,
                      bolt_action=bolt_action,
                      skin=skin_index,
                      magazine=magazine_index
                      ), data
