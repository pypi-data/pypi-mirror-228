import logging

from battlebit_community_server_api.ApiServer import ApiServer, build_api_server
from battlebit_community_server_api.model.OpCodes import OpCodes
from battlebit_community_server_api.model.OutgoingGameServerMessage import OutgoingGameServerMessage
from battlebit_community_server_api.model.PlayerJoiningArguments import PlayerJoiningArguments
from battlebit_community_server_api.model.Squads import Squads
from battlebit_community_server_api.model.Team import Team
from battlebit_community_server_api.service.TcpParsingService import TcpParsingService

my_api_server: ApiServer = build_api_server("0.0.0.0", 30000, None)


async def my_custom_on_player_joining(data: bytes) -> bytes:
    """
    This function:

    1. parses the data received by the "On Player Joining" event.
    2. Sets the players rank to 150.
    3. Builds the appropriate response message.
    4. Returns the response as bytes.
    """
    steam_id, player_stats = TcpParsingService.parse_on_player_joining(data)
    player_stats.progress.rank = 150
    response = OutgoingGameServerMessage(op_code=OpCodes.SEND_PLAYER_STATS, value=steam_id.to_bytes())
    response.add_bytes(PlayerJoiningArguments(player_stats, squad=Squads.NO_SQUAD, team=Team.NONE).to_bytes())
    return response.serialize()


logging.basicConfig(level=logging.DEBUG)  # Optional: If you want to have an in-depth view into what's going on.
my_api_server.register_handler(OpCodes.ON_PLAYER_JOINING, my_custom_on_player_joining)

my_api_server.start()
