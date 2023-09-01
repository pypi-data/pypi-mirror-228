from enum import StrEnum


class Gamemode(StrEnum):
    CONQUEST = "CONQ"
    INFANTRY_CONQUEST = "INFCONQ"
    DOMINATION = "DOMI"
    RUSH = "RUSH"
    CAPTURE_THE_FLAG = "CTF"
    FRONTLINE = "FRONTLINE"
    TEAM_DEATHMATCH = "TDM"
    ELIMINATION = "ELI"
