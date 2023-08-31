import struct
from typing import Optional

from battlebit_community_server_api.model.OpCodes import OpCodes


class OutgoingGameServerMessage:
    """ Abstraction for building outgoing messages to the game server """
    def __init__(self, op_code: OpCodes, value: Optional[bytes] = None) -> None:
        self._op_code = op_code
        self._value: bytes = value if value else bytes()

    def add_bytes(self, new_bytes: bytes) -> None:
        self._value += new_bytes

    def add_string(self, string: str) -> None:
        self._value += string.encode("utf-8")

    def serialize(self, without_packet_size: bool = False) -> bytes:
        serialized_message = struct.pack("B", self._op_code)
        serialized_message += self._value
        if without_packet_size:
            return serialized_message
        return struct.pack("I", len(serialized_message)) + serialized_message
