import struct
from dataclasses import dataclass

from battlebit_community_server_api.helper.StructHelper import read_float32


@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def as_bytes(self) -> bytes:
        out = struct.pack("f", self.x)
        out += struct.pack("f", self.y)
        out += struct.pack("f", self.z)
        return out


def read_from_bytes(data: bytes) -> tuple[Vector3, bytes]:
    """ reads from zero, x => y => z, then returns Vector3 and remaining bytes """
    x, data = read_float32(data)
    y, data = read_float32(data)
    z, data = read_float32(data)
    return Vector3(x=x, y=y, z=z), data
