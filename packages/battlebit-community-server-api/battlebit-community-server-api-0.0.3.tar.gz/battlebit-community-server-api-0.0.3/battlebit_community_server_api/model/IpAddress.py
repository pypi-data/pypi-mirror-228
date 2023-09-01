class IpAddress:
    def __init__(self, uint32: int) -> None:
        self._uint32 = uint32

    def __str__(self) -> str:
        byte1 = (self._uint32 >> 24) & 0xFF
        byte2 = (self._uint32 >> 16) & 0xFF
        byte3 = (self._uint32 >> 8) & 0xFF
        byte4 = self._uint32 & 0xFF
        return f"{byte4}.{byte3}.{byte2}.{byte1}"

    def __int__(self) -> int:
        return self._uint32
