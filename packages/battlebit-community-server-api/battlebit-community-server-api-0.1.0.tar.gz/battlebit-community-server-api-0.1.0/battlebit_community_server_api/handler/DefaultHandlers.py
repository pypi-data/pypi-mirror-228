import logging
import struct
from typing import Callable

from battlebit_community_server_api.command.Command import SetRoleTo, SetTeamTo
from battlebit_community_server_api.model.OpCodes import OpCodes
from battlebit_community_server_api.model.OutgoingGameServerMessage import OutgoingGameServerMessage
from battlebit_community_server_api.model.PlayerJoiningArguments import PlayerJoiningArguments
from battlebit_community_server_api.model.Squads import Squads
from battlebit_community_server_api.model.Team import Team
from battlebit_community_server_api.service.TcpParsingService import TcpParsingService


class DefaultHandlers:
    @classmethod
    def get_default_handler_by_op_code(cls, op_code: OpCodes) -> Callable:
        if op_code == OpCodes.NONE:
            return cls.no_response
        elif op_code == OpCodes.HAIL:
            return cls.hail_handler
        elif op_code == OpCodes.ACCEPTED:
            return cls.no_response
        elif op_code == OpCodes.DENIED:
            return cls.no_response
        elif op_code == OpCodes.EXECUTE_COMMAND:
            return cls.no_response
        elif op_code == OpCodes.SEND_PLAYER_STATS:
            return cls.no_response
        elif op_code == OpCodes.SPAWN_PLAYER:
            return cls.no_response
        elif op_code == OpCodes.SET_NEW_ROOM_SETTINGS:
            return cls.no_response
        elif op_code == OpCodes.RESPOND_PLAYER_MESSAGE:
            return cls.no_response
        elif op_code == OpCodes.SET_NEW_ROUND_STATE:
            return cls.no_response
        elif op_code == OpCodes.SET_PLAYER_WEAPON:
            return cls.no_response
        elif op_code == OpCodes.SET_PLAYER_GADGET:
            return cls.no_response
        elif op_code == OpCodes.PLAYER_CONNECTED:
            return cls.no_response
        elif op_code == OpCodes.PLAYER_DISCONNECTED:
            return cls.no_response
        elif op_code == OpCodes.ON_PLAYER_TYPED_MESSAGE:
            return cls.on_player_typed_message_handler
        elif op_code == OpCodes.ON_PLAYER_KILLED_ANOTHER_PLAYER:
            return cls.no_response
        elif op_code == OpCodes.ON_PLAYER_JOINING:
            return cls.on_player_joining_handler
        elif op_code == OpCodes.SAVE_PLAYER_STATS:
            return cls.no_response
        elif op_code == OpCodes.ON_PLAYER_ASKING_TO_CHANGE_ROLE:
            return cls.on_player_asking_to_change_role
        elif op_code == OpCodes.ON_PLAYER_CHANGED_ROLE:
            return cls.no_response
        elif op_code == OpCodes.ON_PLAYER_JOINED_A_SQUAD:
            return cls.no_response
        elif op_code == OpCodes.ON_PLAYER_LEFT_SQUAD:
            return cls.no_response
        elif op_code == OpCodes.ON_PLAYER_CHANGED_TEAM:
            return cls.no_response
        elif op_code == OpCodes.ON_PLAYER_REQUESTING_TO_SPAWN:
            return cls.on_player_requesting_to_spawn
        elif op_code == OpCodes.ON_PLAYER_REPORT:
            return cls.no_response
        elif op_code == OpCodes.ON_PLAYER_SPAWN:
            return cls.no_response
        elif op_code == OpCodes.ON_PLAYER_DIE:
            return cls.no_response
        elif op_code == OpCodes.NOTIFY_NEW_MAP_ROTATION:
            return cls.no_response
        elif op_code == OpCodes.NOTIFY_NEW_GAME_MODE_ROTATION:
            return cls.no_response
        elif op_code == OpCodes.NOTIFY_NEW_ROUND_STATE:
            return cls.no_response
        elif op_code == OpCodes.ON_PLAYER_ASKING_TO_CHANGE_TEAM:
            return cls.on_player_asking_to_change_team
        elif op_code == OpCodes.GAME_TICK:
            return cls.no_response
        elif op_code == OpCodes.ON_PLAYER_GIVEN_UP:
            return cls.no_response
        elif op_code == OpCodes.ON_PLAYER_REVIVED_ANOTHER:
            return cls.no_response
        elif op_code == OpCodes.ON_SQUAD_POINTS_CHANGED:
            return cls.no_response
        elif op_code == OpCodes.NOTIFY_NEW_ROUND_ID:
            return cls.no_response
        elif op_code == OpCodes.LOG:
            return cls.log
        elif op_code == OpCodes.ON_SQUAD_LEADER_CHANGED:
            return cls.no_response
        elif op_code == OpCodes.UPDATE_NEW_GAME_DATA:
            return cls.no_response
        elif op_code == OpCodes.UPDATE_CONNECTED_PLAYERS:
            return cls.no_response
        raise NotImplementedError(f"Could not find default handler for OP code {OpCodes(op_code).name}")

    @classmethod
    async def hail_handler(cls, data: bytes) -> bytes:
        logging.debug("Accepting HAIL...")
        return OutgoingGameServerMessage(op_code=OpCodes.ACCEPTED).serialize(without_packet_size=True)

    @classmethod
    async def on_player_joining_handler(cls, data: bytes) -> bytes:
        steam_id, player_stats = TcpParsingService.parse_on_player_joining(data)
        response = OutgoingGameServerMessage(op_code=OpCodes.SEND_PLAYER_STATS,
                                             value=steam_id.to_bytes()
                                             )
        response.add_bytes(PlayerJoiningArguments(player_stats, squad=Squads.NO_SQUAD, team=Team.NONE).to_bytes())
        return response.serialize()

    @classmethod
    async def on_player_typed_message_handler(cls, data: bytes) -> bytes:
        message_id, steam_id, channel, message = TcpParsingService.parse_on_player_typed_message(data)
        message_accepted = True
        response = OutgoingGameServerMessage(op_code=OpCodes.RESPOND_PLAYER_MESSAGE,
                                             value=struct.pack("H", message_id) + struct.pack("B", message_accepted))
        return response.serialize()

    @classmethod
    async def on_player_requesting_to_spawn(cls, data: bytes) -> bytes:
        steam_id, spawn_arguments, vehicle_id = TcpParsingService.parse_on_player_requesting_to_spawn(data)
        response = OutgoingGameServerMessage(op_code=OpCodes.SPAWN_PLAYER)
        response.add_bytes(steam_id.to_bytes())
        response.add_bytes(struct.pack("B", True))
        response.add_bytes(spawn_arguments.to_bytes())
        response.add_bytes(struct.pack("H", vehicle_id))
        return response.serialize()

    @classmethod
    async def on_player_asking_to_change_role(cls, data: bytes) -> bytes:
        steam_id, requested_role = TcpParsingService.parse_on_player_asking_to_change_role(data)
        response_command = SetRoleTo(steam_id, requested_role)
        response = OutgoingGameServerMessage(op_code=OpCodes.EXECUTE_COMMAND)
        response.add_bytes(struct.pack("H", len(response_command)))
        response.add_string(response_command.as_string())
        return response.serialize()

    @classmethod
    async def on_player_asking_to_change_team(cls, data: bytes) -> bytes:
        steam_id, requested_team = TcpParsingService.parse_on_player_asking_to_change_team(data)
        response_command = SetTeamTo(steam_id, requested_team)
        response = OutgoingGameServerMessage(op_code=OpCodes.EXECUTE_COMMAND)
        response.add_bytes(struct.pack("H", len(response_command)))
        response.add_string(response_command.as_string())
        return response.serialize()

    @classmethod
    async def no_response(cls, _: bytes) -> None:
        """ Specialized handler that signals that there is no need to respond """
        return

    @classmethod
    async def log(cls, data: bytes) -> None:
        logging.debug(TcpParsingService.parse_log(data))
        return

    @classmethod
    async def debug_log_bytes(cls, data: bytes) -> None:
        """ Debug handler to log certain OP codes """
        logging.debug(data)
        return
