import logging
from datetime import datetime

from battlebit_community_server_api.ApiServer import ApiServer, build_api_server
from battlebit_community_server_api.command.Command import SayToAllChat, ForceStartGame, SayToChat
from battlebit_community_server_api.handler.DefaultHandlers import DefaultHandlers
from battlebit_community_server_api.model.OpCodes import OpCodes
from battlebit_community_server_api.service.TcpParsingService import TcpParsingService

my_api_server: ApiServer = build_api_server("0.0.0.0", 30000, None)


async def chat_messages_handler(data: bytes) -> bytes:
    """
    This function:

    1. Parses the data received by the "On Player Typed Message" event.
    2. Builds a new message depending on what the content of the original was.
    3. Sends the new message to chat.
    4. Executes the default handler for "On Player Typed Message" event.
    """
    message_id, steam_id, channel, message = TcpParsingService.parse_on_player_typed_message(data)
    if message.startswith("!"):
        message = message.lstrip("!").lower()
        if message == "time":
            response_to_chat = SayToAllChat(f"Current time: {datetime.now().strftime('%H:%M:%S')}")
        elif message == "steamid":
            response_to_chat = SayToChat(f"Your STEAM-ID: {steam_id}", steam_id)
        elif message == "forcestart":
            response_to_chat = SayToAllChat(f"Force starting round")
            await my_api_server.add_command_to_queue(ForceStartGame())
        else:
            response_to_chat = SayToAllChat(f"Sorry, I couldn't recognize your command :(")

        await my_api_server.add_command_to_queue(response_to_chat)

    return await DefaultHandlers.get_default_handler_by_op_code(OpCodes.ON_PLAYER_TYPED_MESSAGE)(data)


logging.basicConfig(level=logging.DEBUG)  # Optional: If you want to have an in-depth view into what's going on.
my_api_server.register_handler(OpCodes.ON_PLAYER_TYPED_MESSAGE, chat_messages_handler)

my_api_server.start()
