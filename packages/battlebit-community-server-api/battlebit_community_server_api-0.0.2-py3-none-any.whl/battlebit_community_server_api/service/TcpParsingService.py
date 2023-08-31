import logging
from typing import Optional

from battlebit_community_server_api.helper.StructHelper import *
from battlebit_community_server_api.model import PlayerProgress
from battlebit_community_server_api.model.ChatChannel import ChatChannel
from battlebit_community_server_api.model.GameRole import GameRole
from battlebit_community_server_api.model.MapSize import MapSize
from battlebit_community_server_api.model.OpCodes import OpCodes
from battlebit_community_server_api.model.GameState import GameState
from battlebit_community_server_api.model.PlayerLoadout import read_from_bytes as build_player_loadout, \
    PlayerLoadout
from battlebit_community_server_api.model.PlayerSpawnArguments import PlayerSpawnArguments
from battlebit_community_server_api.model.PlayerSpawningPosition import PlayerSpawningPosition
from battlebit_community_server_api.model.PlayerStand import PlayerStand
from battlebit_community_server_api.model.PlayerStats import PlayerStats
from battlebit_community_server_api.model.Role import Role
from battlebit_community_server_api.model.RoomSettings import RoomSettings, from_bytes as room_settings_from_bytes
from battlebit_community_server_api.model.ServerInfo import ServerInfo
from battlebit_community_server_api.model.Squads import Squads
from battlebit_community_server_api.model.SteamId import SteamId
from battlebit_community_server_api.model.Team import Team
from battlebit_community_server_api.model.PlayerWearings import read_from_bytes as build_player_wearings, PlayerWearings
from battlebit_community_server_api.model.Vector3 import read_from_bytes as build_vector3


class TcpParsingService:
    """ The TcpParsingService parses TCP packages in their raw, bytes format and returns data objects. """
    ROUND_SETTINGS_SIZE: int = 33
    MAX_SQUADS_PER_TEAM: int = 64

    @staticmethod
    def split_data_into_individual_messages(data: bytes) -> tuple[tuple[OpCodes, bytes]]:
        """ Takes a bytestring of any length, splits it in individual messages and returns them with OpCodes """
        messages = []
        while len(data) > 0:
            packet_size, data = read_uint32(data)
            message = data[:packet_size]
            data = data[packet_size:]
            op_code_raw, message = read_uint8(message)
            messages.append((OpCodes(op_code_raw), message))
        return tuple(messages)

    @staticmethod
    def parse_on_player_connected(message: bytes) -> None:  # FixMe: UNTESTED
        steam_id = struct.unpack("Q", message[:8])[0]
        message = message[8:]
        user_name_size = struct.unpack("H", message[:2])[0]
        message = message[2:]
        if user_name_size != 0:  # ToDo: Parse this as soon as data comes available, set buffer position accordingly
            print("FOUND NEW DATASET, USERNAME SIZE != 0\n", message)
        ip_address = struct.unpack("I", message[:4])[0]
        message = message[4:]
        team = int(struct.unpack("B", message[:1])[0])
        message = message[1:]
        squad = int(struct.unpack("B", message[:1])[0])
        message = message[1:]
        role = int(struct.unpack("B", message[:1])[0])
        message = message[1:]

    @staticmethod
    def parse_on_player_typed_message(message: bytes) -> tuple[int, SteamId, ChatChannel, str]:
        """ Returns tuple with messageID, SteamID, ChatChannel and the message string """
        message_id, message = read_uint16(message)
        steam_id, message = read_uint64(message)
        channel, message = read_uint8(message)
        message_length, message = read_uint16(message)
        return message_id, SteamId(steam_id), ChatChannel(channel), message[:message_length].decode("utf-8")

    @staticmethod
    def parse_on_player_joining(message: bytes) -> tuple[SteamId, PlayerStats]:
        """ Returns a tuple with SteamID and PlayerStats """
        steam_id, message = read_uint64(message)
        steam_id = SteamId(steam_id)
        is_banned, message = read_uint8(message)
        is_banned = bool(is_banned)
        roles, message = read_uint64(message)

        progress, message = PlayerProgress.build_player_progress_from_bytes(message)

        tool_progress_size, message = read_uint16(message)
        tool_progress_raw = message[:tool_progress_size]
        message = message[tool_progress_size:]

        achievements_size, message = read_uint16(message)
        achievements_raw = message[:achievements_size]
        message = message[achievements_size:]

        selections_size, message = read_uint16(message)
        selections_raw = message[:selections_size]
        message = message[selections_size:]

        return steam_id, PlayerStats(is_banned=is_banned,
                                     roles=roles,
                                     progress=progress,
                                     tool_progress=tool_progress_raw,
                                     achievements=achievements_raw,
                                     selections=selections_raw)

    @classmethod
    def parse_hail_message(cls, message: bytes) -> ServerInfo:
        """ Parses HAIL """
        # ToDo: Parse Map/GameMode Rotation and Room Settings and add them to ServerInfo

        # Token
        token_size, message = read_uint16(message)
        token, message = read_string(message, token_size)

        # Version
        version_size, message = read_uint16(message)
        version, message = read_string(message, version_size)

        # Game Port
        game_port, message = read_uint16(message)

        # is port protected
        is_port_protected = struct.unpack("?", message[:1])[0]
        message = message[1:]

        # length of server name
        server_name_length, message = read_uint16(message)

        # Server Name
        server_name = message[:server_name_length].decode("utf-8")
        message = message[server_name_length:]

        # length of game mode name
        game_mode_name_length, message = read_uint16(message)

        # Game Mode Name
        game_mode_name = message[:game_mode_name_length].decode("utf-8")
        message = message[game_mode_name_length:]

        # length of map name
        map_name_length, message = read_uint16(message)

        # Map Name
        map_name = message[:map_name_length].decode("utf-8")
        message = message[map_name_length:]

        # Map Size
        map_size, message = read_uint8(message)

        # DayNight Cycle
        day_night_cycle, message = read_uint8(message)

        # Current Players
        current_players, message = read_uint8(message)

        # Queued Players
        queued_players, message = read_uint8(message)

        # Max Players
        max_players, message = read_uint8(message)

        # Loading screen text length
        loading_screen_text_length, message = read_uint16(message)

        # Loading screen text
        loading_screen_text = message[:loading_screen_text_length].decode("utf-8")
        message = message[loading_screen_text_length:]

        # Server Rules text size
        server_rules_text_length, message = read_uint16(message)

        # Server rules text
        server_rules_text = message[:server_rules_text_length].decode("utf-8")
        message = message[server_rules_text_length:]

        # Round Index
        round_index, message = read_uint32(message)

        # Session ID
        session_id, message = read_uint64(message)

        # Room Settings size
        room_settings_length, message = read_uint32(message)
        # Room Settings
        room_settings = room_settings_from_bytes(message)
        message = message[room_settings_length:]

        # Map & Game mode Rotation size
        map_and_game_mode_rotation_size, message = read_uint32(message)

        # Map & Game mode Rotation
        cls.parse_map_game_mode_rotation(message[:map_and_game_mode_rotation_size])
        message = message[map_and_game_mode_rotation_size:]

        # Round Settings
        round_settings = cls._parse_round_settings(message[:cls.ROUND_SETTINGS_SIZE])
        message = message[cls.ROUND_SETTINGS_SIZE:]

        # Clients
        client_count, message = read_uint8(message)
        clients = []
        for i in range(client_count):
            steam_id, user_name, ip_hash, team, squad, role, is_alive, loadout, wearings, message = \
                cls.parse_hail_message_client_info(message)
            clients.append((steam_id, user_name, ip_hash, team, squad, role, is_alive, loadout, wearings))

        logging.debug("Connected clients:")
        for client in clients:
            logging.debug(f"[{client[0]}] {client[1]}")

        # Squads
        squad_data_size, message = read_uint32(message)
        squad_points_team_us = []
        for _ in range(cls.MAX_SQUADS_PER_TEAM):
            points, message = read_uint32(message)
            squad_points_team_us.append(points)

        squad_points_team_ru = []
        for _ in range(cls.MAX_SQUADS_PER_TEAM):
            points, message = read_uint32(message)
            squad_points_team_ru.append(points)

        if message:
            logging.warning(f"Unparsed HAIL message remains: {message}. "
                            f"Probably an update that broke everything. Please fix.")

        return ServerInfo(name=server_name,
                          version=version,
                          port=game_port,
                          protected=is_port_protected,
                          game_mode=game_mode_name,
                          map_name=map_name,
                          map_size=MapSize(map_size),
                          is_day_mode=day_night_cycle == 0,
                          current_players=current_players,
                          queued_players=queued_players,
                          max_players=max_players,
                          loading_screen_text=loading_screen_text,
                          rules_text=server_rules_text,
                          game_state=GameState(round_settings[0]),
                          seconds_left_in_round=round_settings[-1],
                          room_settings=room_settings)


    @classmethod
    def parse_on_player_requesting_to_spawn(cls, message: bytes) -> tuple[SteamId, PlayerSpawnArguments, int]:
        """ Returns STEAM-ID, PlayerSpawnArguments and a Vehicle-ID """
        steam_id, message = read_uint64(message)
        steam_id = SteamId(steam_id)
        player_spawning_position, message = read_uint8(message)
        player_spawning_position = PlayerSpawningPosition(player_spawning_position)

        # LOADOUT
        player_loadout, message = build_player_loadout(message)

        # WEARINGS
        player_wearings, message = build_player_wearings(message)
        spawn_position, message = build_vector3(message)
        look_direction, message = build_vector3(message)
        stand, message = read_uint8(message)
        stand = PlayerStand(stand)
        spawn_protection, message = read_float32(message)

        # VEHICLE ID
        vehicle_id, message = read_uint16(message)

        return steam_id, PlayerSpawnArguments(
            position=player_spawning_position,
            loadout=player_loadout,
            wearings=player_wearings,
            vector_position=spawn_position,
            look_direction=look_direction,
            stand=stand,
            spawn_protection=spawn_protection
        ), vehicle_id

    @staticmethod
    def parse_on_player_asking_to_change_role(data: bytes) -> tuple[SteamId, GameRole]:
        steam_id, data = read_uint64(data)
        steam_id = SteamId(steam_id)
        requested_role, data = read_uint8(data)
        requested_role = GameRole(requested_role)
        return steam_id, requested_role

    @staticmethod
    def parse_on_player_asking_to_change_team(data: bytes) -> tuple[SteamId, Team]:
        steam_id, data = read_uint64(data)
        steam_id = SteamId(steam_id)
        requested_team, data = read_uint8(data)
        requested_team = Team(requested_team)
        return steam_id, requested_team

    @staticmethod
    def parse_map_game_mode_rotation(map_game_mode_rotation_bytes: bytes) -> None:
        # FixMe: Not clear how those values are to be understood
        map_rotation_size = struct.unpack("I", map_game_mode_rotation_bytes[:4])[0]  # Map Rotation
        game_mode_rotation_size = struct.unpack("I", map_game_mode_rotation_bytes[:4])[0]  # Game Mode Rotation

    @staticmethod
    def _parse_round_settings(round_settings_bytes: bytes) -> tuple[int, float, float, float, int, int]:
        state = struct.unpack('b', round_settings_bytes[0:1])[0]
        team_a_tickets = struct.unpack('d', round_settings_bytes[1:9])[0]
        team_b_tickets = struct.unpack('d', round_settings_bytes[9:17])[0]
        max_tickets = struct.unpack('d', round_settings_bytes[17:25])[0]
        players_to_start = struct.unpack('i', round_settings_bytes[25:29])[0]
        seconds_left = struct.unpack('i', round_settings_bytes[29:33])[0]
        return state, team_a_tickets, team_b_tickets, max_tickets, players_to_start, seconds_left

    @staticmethod
    def parse_hail_message_client_info(client_info: bytes) -> tuple[
        SteamId, str, int, Team, Squads, Role, bool, Optional[PlayerLoadout], Optional[PlayerWearings], bytes]:
        """
        Parses the guaranteed 24 bytes segments of client info, returned by the HAIL message.
        Then, if the player is alive, parses the PlayerLoadout and PlayerWearing.

        :return: Tuple containing: Steam-ID, Username, IP Hash, Team, Squad, Role, IsAliveStatus, PlayerLoadout,
                                   PlayerWearing and the remainder of buffer.
        :note: If the player is not alive, PlayerLoadout and PlayerWearing are None.
        """
        steam_id, client_info = read_uint64(client_info)
        steam_id = SteamId(steam_id)
        user_name_size, client_info = read_uint16(client_info)
        user_name, client_info = read_string(client_info, user_name_size)
        ip_hash, client_info = read_uint32(client_info)
        team, client_info = read_uint8(client_info)
        team = Team(team)
        squad, client_info = read_uint8(client_info)
        squad = Squads(squad)
        role, client_info = read_uint8(client_info)
        role = Role(role)
        is_alive, client_info = read_uint8(client_info)
        is_alive = bool(is_alive)
        if is_alive:
            _, client_info = read_uint32(client_info)  # Loadout size
            player_loadout, client_info = build_player_loadout(client_info)
            player_wearings, client_info = build_player_wearings(client_info)
        else:
            player_loadout = None
            player_wearings = None

        return steam_id, user_name, ip_hash, team, squad, role, is_alive, player_loadout, player_wearings, client_info
