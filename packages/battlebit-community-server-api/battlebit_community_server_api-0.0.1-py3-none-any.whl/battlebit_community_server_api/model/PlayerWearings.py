from dataclasses import dataclass

from battlebit_community_server_api.helper.StructHelper import *


@dataclass
class PlayerWearings:
    head: str
    chest: str
    belt: str
    backpack: str
    eye: str
    face: str
    hair: str
    skin: str
    uniform: str
    camo: str

    def as_bytes(self) -> bytes:
        out = write_string(self.head)
        out += write_string(self.chest)
        out += write_string(self.belt)
        out += write_string(self.backpack)
        out += write_string(self.eye)
        out += write_string(self.face)
        out += write_string(self.hair)
        out += write_string(self.skin)
        out += write_string(self.uniform)
        out += write_string(self.camo)
        return out


def read_from_bytes(data: bytes) -> tuple[PlayerWearings, bytes]:
    head_size, data = read_uint16(data)
    head, data = read_string(data, head_size)

    chest_size, data = read_uint16(data)
    chest, data = read_string(data, chest_size)

    belt_size, data = read_uint16(data)
    belt, data = read_string(data, belt_size)

    backpack_size, data = read_uint16(data)
    backpack, data = read_string(data, backpack_size)

    eye_size, data = read_uint16(data)
    eye, data = read_string(data, eye_size)

    face_size, data = read_uint16(data)
    face, data = read_string(data, face_size)

    hair_size, data = read_uint16(data)
    hair, data = read_string(data, hair_size)

    skin_size, data = read_uint16(data)
    skin, data = read_string(data, skin_size)

    uniform_size, data = read_uint16(data)
    uniform, data = read_string(data, uniform_size)

    camo_size, data = read_uint16(data)
    camo, data = read_string(data, camo_size)

    return PlayerWearings(head=head,
                          chest=chest,
                          belt=belt,
                          backpack=backpack,
                          eye=eye,
                          face=face,
                          hair=hair,
                          skin=skin,
                          uniform=uniform,
                          camo=camo), data
