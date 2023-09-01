import logging
from typing import Optional

from battlebit_community_server_api.helper.StructHelper import *
from battlebit_community_server_api.model import PlayerProgress
from battlebit_community_server_api.model.ChatChannel import ChatChannel
from battlebit_community_server_api.model.GameRole import GameRole
from battlebit_community_server_api.model.MapSize import MapSize
from battlebit_community_server_api.model.OpCodes import OpCodes
from battlebit_community_server_api.model.GameState import GameState
from battlebit_community_server_api.model.PlayerLoadout import read_from_bytes as build_player_loadout, PlayerLoadout
from battlebit_community_server_api.model.PlayerSpawnArguments import PlayerSpawnArguments
from battlebit_community_server_api.model.PlayerSpawningPosition import PlayerSpawningPosition
from battlebit_community_server_api.model.PlayerStand import PlayerStand
from battlebit_community_server_api.model.PlayerStats import PlayerStats
from battlebit_community_server_api.model.Role import Role
from battlebit_community_server_api.model.RoomSettings import from_bytes as room_settings_from_bytes
from battlebit_community_server_api.model.ServerInfo import ServerInfo
from battlebit_community_server_api.model.Squads import Squads
from battlebit_community_server_api.model.SteamId import SteamId
from battlebit_community_server_api.model.Team import Team
from battlebit_community_server_api.model.PlayerWearings import read_from_bytes as build_player_wearings, PlayerWearings
from battlebit_community_server_api.model.Vector3 import read_from_bytes as build_vector3, Vector3
from battlebit_community_server_api.model.Map import Map
from battlebit_community_server_api.model.Gamemode import Gamemode
from battlebit_community_server_api.model.IpAddress import IpAddress
from battlebit_community_server_api.model.Report import Report
from battlebit_community_server_api.model.ReportReason import ReportReason
from battlebit_community_server_api.model.PlayerBody import PlayerBody
from battlebit_community_server_api.model.ReasonOfDamage import ReasonOfDamage
from battlebit_community_server_api.model.KillReport import KillReport
from battlebit_community_server_api.model.RoundState import RoundState
from battlebit_community_server_api.model.LeaningSide import LeaningSide
from battlebit_community_server_api.model.LoadoutIndex import LoadoutIndex
from battlebit_community_server_api.model.PlayerState import PlayerState
from battlebit_community_server_api.model.MapDayNight import MapDayNight


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
    def parse_player_connected(message: bytes) -> tuple[SteamId, str, IpAddress, Team, Squads, Role]:
        """
        Parses the payload of PLAYER_CONNECTED and

        :return: SteamID, Username, IPAddress, Team, Squad, Role
        """
        steam_id, message = read_uint64(message)
        steam_id = SteamId(steam_id)
        user_name_length, message = read_uint16(message)
        user_name, message = read_string(message, user_name_length)
        ip, message = read_uint32(message)
        ip = IpAddress(ip)
        team, message = read_uint8(message)
        team = Team(team)
        squad, message = read_uint8(message)
        squad = Squads(squad)
        role, message = read_uint8(message)
        role = Role(role)
        return steam_id, user_name, ip, team, squad, role

    @staticmethod
    def parse_player_disconnected(message: bytes) -> SteamId:
        """ Returns SteamID of disconnected player """
        return SteamId(read_uint64(message)[0])

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
        map_rotation, gamemode_rotation = cls.parse_map_game_mode_rotation(message[:map_and_game_mode_rotation_size])
        message = message[map_and_game_mode_rotation_size:]

        # Round State
        round_state = cls._parse_round_settings(message[:cls.ROUND_SETTINGS_SIZE])
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
                          game_mode=Gamemode(game_mode_name),
                          map_name=Map(map_name),
                          map_size=MapSize(map_size),
                          is_day_mode=day_night_cycle == 0,
                          current_players=current_players,
                          queued_players=queued_players,
                          max_players=max_players,
                          loading_screen_text=loading_screen_text,
                          rules_text=server_rules_text,
                          round_state=round_state,
                          room_settings=room_settings,
                          gamemode_rotation=gamemode_rotation,
                          map_rotation=map_rotation)

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
    def parse_map_game_mode_rotation(data: bytes) -> tuple[list[Map], list[Gamemode]]:
        maps_in_rotation, data = read_uint32(data)
        maps = []
        for _ in range(maps_in_rotation):
            map_name_size, data = read_uint16(data)
            map_name, data = read_string(data, map_name_size)
            try:
                maps.append(Map(map_name))
            except ValueError:
                logging.warning(f"Unknown map name '{map_name}' found, skipping.")

        game_modes_in_rotation, data = read_uint32(data)
        game_modes = []
        for _ in range(game_modes_in_rotation):
            gamemode_name_size, data = read_uint16(data)
            gamemode_name, data = read_string(data, gamemode_name_size)
            try:
                game_modes.append(Gamemode(gamemode_name))
            except ValueError:
                logging.warning(f"Unknown gamemode name '{gamemode_name}' found, skipping.")

        return maps, game_modes

    @staticmethod
    def parse_notify_new_map_rotation(data: bytes) -> list[Map]:
        map_count, data = read_uint32(data)
        maps = []
        for _ in range(map_count):
            map_name_size, data = read_uint16(data)
            map_name, data = read_string(data, map_name_size)
            maps.append(Map(map_name))
        return maps

    @staticmethod
    def parse_notify_new_gamemode_rotation(data: bytes) -> list[Gamemode]:
        """ ToDo: Currently broken on server-side, implement when fixed. """
        raise NotImplementedError

    @staticmethod
    def parse_on_player_changed_role(data: bytes) -> tuple[SteamId, GameRole]:
        """ Returns SteamID and the players new game role """
        steam_id, data = read_uint64(data)
        steam_id = SteamId(steam_id)
        new_role, data = read_uint8(data)
        new_role = GameRole(new_role)
        return steam_id, new_role

    @staticmethod
    def parse_on_player_joined_a_squad(data: bytes) -> tuple[SteamId, Squads, bool]:
        """
        Parses the payload from ON_PLAYER_JOINED_A_SQUAD

        :return: SteamID, new Squad of the player and a bool that tells if the player is the new captain of that squad
        """
        steam_id, data = read_uint64(data)
        steam_id = SteamId(steam_id)
        new_squad, data = read_uint8(data)
        new_squad = Squads(new_squad)
        is_squad_captain, _ = read_bool(data)
        return steam_id, new_squad, is_squad_captain

    @staticmethod
    def parse_on_player_left_squad(data: bytes) -> SteamId:
        return SteamId(read_uint64(data)[0])

    @staticmethod
    def parse_on_player_changed_team(data: bytes) -> tuple[SteamId, Team]:
        steam_id, new_team = read_uint64(data)
        steam_id, new_team = SteamId(steam_id), Team(read_uint8(new_team)[0])
        return steam_id, new_team

    @staticmethod
    def parse_on_player_report(data: bytes) -> Report:
        # Untested, should work though
        reporter, data = read_uint64(data)
        reported, data = read_uint64(data)
        reason, data = read_uint8(data)
        if data:
            additional_info_size, data = read_uint16(data)
            additional_info, _ = read_string(data, additional_info_size)
        else:
            additional_info = None
        return Report(SteamId(reporter), SteamId(reported), ReportReason(reason), additional_info)

    @staticmethod
    def parse_on_player_killed_another_player(data: bytes) -> KillReport:
        killer, data = read_uint64(data)
        killer = SteamId(killer)
        killer_pos, data = build_vector3(data)
        victim, data = read_uint64(data)
        victim = SteamId(victim)
        victim_pos, data = build_vector3(data)
        tool_size, data = read_uint16(data)
        tool_name, data = read_string(data, tool_size)
        if not tool_name:
            tool_name = None
        body_part, data = read_uint8(data)
        body_part = PlayerBody(body_part)
        damage_reason, _ = read_uint8(data)
        damage_reason = ReasonOfDamage(damage_reason)

        return KillReport(killer, killer_pos, victim, victim_pos, tool_name, body_part, damage_reason)

    @classmethod
    def parse_save_player_stats(cls, data: bytes) -> tuple[SteamId, PlayerStats]:
        """ Returns SteamID and Stats of player """
        # Data is identical, so we can just use the parser for ON_PLAYERS_JOINING
        return cls.parse_on_player_joining(data)

    @classmethod
    def parse_on_player_given_up(cls, data: bytes) -> SteamId:
        """ Returns SteamID of player that gave up"""
        return SteamId(read_uint64(data)[0])

    @staticmethod
    def parse_on_player_spawn(data: bytes) -> tuple[SteamId, PlayerLoadout, PlayerWearings, Vector3]:
        """ Returns SteamID, Loadout, Wearings and spawn position of spawning player """
        steam_id, data = read_uint64(data)
        steam_id = SteamId(steam_id)
        player_loadout, data = build_player_loadout(data)
        player_wearings, data = build_player_wearings(data)
        spawn_pos, _ = build_vector3(data)
        return steam_id, player_loadout, player_wearings, spawn_pos

    @staticmethod
    def parse_on_player_die(data: bytes) -> SteamId:
        """ Returns the SteamID of the player that died """
        return SteamId(read_uint64(data)[0])

    @staticmethod
    def parse_on_player_revived_another(data: bytes) -> tuple[SteamId, SteamId]:
        """ Returns the SteamID of the reviver and the revived. First entry is the reviver. """
        reviving_player, data = read_uint64(data)
        reviving_player = SteamId(reviving_player)
        revived_player, _ = read_uint64(data)
        revived_player = SteamId(revived_player)
        return reviving_player, revived_player

    @classmethod
    def parse_new_round_state(cls, data: bytes) -> RoundState:
        return cls._parse_round_settings(data)

    @staticmethod
    def _parse_round_settings(round_settings_bytes: bytes) -> RoundState:
        state, round_settings_bytes = read_uint8(round_settings_bytes)
        state = GameState(state)
        team_a_tickets, round_settings_bytes = read_uint64(round_settings_bytes)
        team_b_tickets, round_settings_bytes = read_uint64(round_settings_bytes)
        max_tickets, round_settings_bytes = read_uint64(round_settings_bytes)
        players_to_start, round_settings_bytes = read_uint32(round_settings_bytes)
        seconds_left, round_settings_bytes = read_uint32(round_settings_bytes)
        return RoundState(state, team_a_tickets, team_b_tickets, max_tickets, players_to_start, seconds_left)

    @staticmethod
    def parse_game_tick(data: bytes) -> tuple[int, list[PlayerState]]:
        """ Returns amount of players ALIVE as well as the state of everyone alive """
        decompress_x, data = read_float32(data)
        decompress_y, data = read_float32(data)
        decompress_z, data = read_float32(data)

        offset_x, data = read_float32(data)
        offset_y, data = read_float32(data)
        offset_z, data = read_float32(data)

        player_count, data = read_uint8(data)
        player_states = []
        for player in range(player_count):
            steam_id, data = read_uint64(data)
            steam_id = SteamId(steam_id)
            com_pos_x, data = read_uint16(data)
            com_pos_y, data = read_uint16(data)
            com_pos_z, data = read_uint16(data)
            player_position = Vector3(
                (com_pos_x * decompress_x) - offset_x,
                (com_pos_y * decompress_y) - offset_y,
                (com_pos_z * decompress_z) - offset_z,
            )
            # FixMe: Unclear how player_health value is to be interpreted, leaving it out for now
            player_health, data = read_uint8(data)
            player_health = (player_health * 0.5) - 1.0
            player_standing, data = read_uint8(data)
            player_standing = PlayerStand(player_standing)
            leaning_side, data = read_uint8(data)
            leaning_side = LeaningSide(leaning_side)
            loadout_index, data = read_uint8(data)
            loadout_index = LoadoutIndex(loadout_index)
            in_seat, data = read_bool(data)
            is_bleeding, data = read_bool(data)
            ping, data = read_uint16(data)
            player_states.append(
                PlayerState(
                    steam_id, player_position, player_standing, leaning_side, loadout_index, in_seat, is_bleeding, ping
                )
            )

        return player_count, player_states

    @staticmethod
    def parse_on_squad_points_changed(data: bytes) -> tuple[Team, Squads, int]:
        """ Returns the squads current points """
        team, data = read_uint8(data)
        team = Team(team)
        squad, data = read_uint8(data)
        squad = Squads(squad)
        points, _ = read_uint32(data)
        return team, squad, points

    @staticmethod
    def parse_notify_new_round_id(data: bytes) -> tuple[int, int]:
        """ Returns Round-Index and SessionID """
        round_index, data = read_uint32(data)
        session_id, _ = read_uint64(data)
        return round_index, session_id

    @staticmethod
    def parse_log(data: bytes) -> str:
        """ Returns log message """
        log_msg_size, data = read_uint16(data)
        return read_string(data, log_msg_size)[0]

    @staticmethod
    def parse_on_squad_leader_changed(data: bytes) -> tuple[SteamId, Squads]:
        """ Returns SteamID of the player who is the new squad leader, and the squad (without team info) """
        steam_id, data = read_uint64(data)
        steam_id = SteamId(steam_id)
        squad, _ = read_uint8(data)
        squad = Squads(squad)
        return steam_id, squad

    @staticmethod
    def parse_update_connected_players(data: bytes) -> tuple[int, int, int]:
        """ Returns current players, players in queue and max players, in that order. """
        current_players, data = read_uint8(data)
        in_queue, data = read_uint8(data)
        max_players, data = read_uint8(data)  # Intentionally whacky, ask Oki
        max_players, data = read_uint8(data)
        return current_players, in_queue, max_players

    @staticmethod
    def parse_update_new_game_data(data: bytes) -> tuple[int, int, int, str, MapSize, str, MapDayNight]:
        """
        Returns (in that order):
        Current players, players in queue, max players, game mode name, map size, map name, day-night flag
        """
        # ToDo: Maybe make this into a dataclass later.
        current_players, data = read_uint8(data)
        in_queue, data = read_uint8(data)
        max_players, data = read_uint8(data)  # Intentionally whacky, ask Oki
        max_players, data = read_uint8(data)
        gamemode_name_len, data = read_uint16(data)
        gamemode_name, data = read_string(data, gamemode_name_len)
        map_size, data = read_uint8(data)
        map_size = MapSize(map_size)
        map_name_len, data = read_uint16(data)
        map_name, data = read_string(data, map_name_len)
        game_type, data = read_uint8(data)
        day_night, _ = read_uint8(data)
        day_night = MapDayNight(day_night)
        return current_players, in_queue, max_players, gamemode_name, map_size, map_name, day_night

    @staticmethod
    def parse_hail_message_client_info(client_info: bytes) -> tuple[SteamId, str, int, Team, Squads, Role, bool,
                                                                    Optional[PlayerLoadout], Optional[PlayerWearings],
                                                                    bytes]:
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
