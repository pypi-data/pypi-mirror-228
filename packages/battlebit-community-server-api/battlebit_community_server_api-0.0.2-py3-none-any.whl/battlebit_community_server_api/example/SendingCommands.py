import logging

from battlebit_community_server_api.ApiServer import ApiServer, build_api_server
from battlebit_community_server_api.command.Command import SayToAllChat
from battlebit_community_server_api.handler.DefaultHandlers import DefaultHandlers
from battlebit_community_server_api.model.OpCodes import OpCodes
from battlebit_community_server_api.service.TcpParsingService import TcpParsingService

my_api_server: ApiServer = build_api_server("0.0.0.0", 30000, None)


async def my_custom_on_player_joining(data: bytes) -> bytes:
    """
    This function:

    1. Parses the data received by the "On Player Joining" event.
    2. Builds a command to greet the player in chat.
    3. Schedules the command to be executed.
    4. Executes the default handler for "On Player Joining" event.
    """
    steam_id, player_stats = TcpParsingService.parse_on_player_joining(data)
    my_new_command = SayToAllChat(f"Welcome user {steam_id}!")
    await my_api_server.add_command_to_queue(my_new_command)

    return await DefaultHandlers.get_default_handler_by_op_code(OpCodes.ON_PLAYER_JOINING)(data)


logging.basicConfig(level=logging.DEBUG)  # Optional: If you want to have an in-depth view into what's going on.
my_api_server.register_handler(OpCodes.ON_PLAYER_JOINING, my_custom_on_player_joining)

my_api_server.start()
