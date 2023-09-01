import logging
import struct


def read_uint8(buf: bytes) -> tuple[int, bytes]:
    """ Reads uint8, returns remaining buffer """
    uint8 = int(struct.unpack("B", buf[:1])[0])
    return uint8, buf[1:]


def write_uint8(d: int) -> bytes:
    """ Writes an integer to a single byte """
    if not 0 <= d <= 255:
        raise ValueError(f"Can not convert integer {d} to uint8!")
    return struct.pack("B", d)


def read_bool(buf: bytes) -> tuple[bool, bytes]:
    """ Reads uint8, converts result to boolean, returns remaining buffer """
    uint8 = int(struct.unpack("B", buf[:1])[0])
    return bool(uint8), buf[1:]


def write_bool(d: bool) -> bytes:
    """ Writes a boolean to a single byte """
    return struct.pack("B", d)


def read_uint16(buf: bytes) -> tuple[int, bytes]:
    """ Reads uint16, returns remaining buffer """
    uint16 = int(struct.unpack("H", buf[:2])[0])
    return uint16, buf[2:]


def read_uint32(buf: bytes) -> tuple[int, bytes]:
    """ Reads uint32, returns remaining buffer """
    uint32 = int(struct.unpack("I", buf[:4])[0])
    return uint32, buf[4:]


def read_uint64(buf: bytes) -> tuple[int, bytes]:
    """ Reads uint64, returns remaining buffer """
    uint64 = int(struct.unpack("Q", buf[:8])[0])
    return uint64, buf[8:]


def read_float32(buf: bytes) -> tuple[float, bytes]:
    f_32 = struct.unpack("f", buf[:4])[0]
    return f_32, buf[4:]


def write_float32(d: float) -> bytes:
    return struct.pack("f", d)


def read_string(buf: bytes, length: int) -> tuple[str, bytes]:
    """ Reads string of specified length (from 0), returns remaining buffer """
    return buf[:length].decode("utf-8"), buf[length:]


def write_string(string_to_write: str) -> bytes:
    """ writes string to bytes, including the 2-Byte length prefix """
    b = struct.pack("H", len(string_to_write))
    b += string_to_write.encode("utf-8")
    return b
