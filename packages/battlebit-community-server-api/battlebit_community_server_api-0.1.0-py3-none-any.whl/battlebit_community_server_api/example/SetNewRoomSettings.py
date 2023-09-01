import asyncio
import logging
import time
from threading import Thread

from battlebit_community_server_api.ApiServer import ApiServer, build_api_server
from battlebit_community_server_api.model.OpCodes import OpCodes
from battlebit_community_server_api.model.OutgoingGameServerMessage import OutgoingGameServerMessage
from battlebit_community_server_api.model.RoomSettings import RoomSettings

event_loop = asyncio.new_event_loop()
my_api_server: ApiServer = build_api_server("0.0.0.0", 30000, event_loop)

# Construct new room settings
new_room_settings = RoomSettings(
    damage_multiplier=1.0,
    friendly_fire_enabled=False,
    hide_map_votes=True,
    only_winner_team_can_vote=True,
    player_collision_enabled=True,

    medic_limit_per_squad=5,
    engineer_limit_per_squad=6,
    support_limit_per_squad=7,
    recon_limit_per_squad=2,

    can_vote_for_day=True,
    can_vote_for_night=True,

    tank_spawn_delay_multiplier=1.0,
    transport_spawn_delay_multiplier=1.0,
    sea_vehicle_spawn_delay_multiplier=1.0,
    apc_spawn_delay_multiplier=1.0,
    helicopter_spawn_delay_multiplier=1.0,

    unlock_all_attachments=True,
    teamless_mode_enabled=False,
    squad_required_to_change_role=False
)

# Prepare an outgoing server message to be added to the queue
my_outgoing_game_server_message = OutgoingGameServerMessage(
    op_code=OpCodes.SET_NEW_ROOM_SETTINGS,
    value=new_room_settings.to_bytes()
)


logging.basicConfig(level=logging.DEBUG)  # Optional: If you want to have an in-depth view into what's going on.

# Adding OutgoingGameServerMessages to the queue from outside the main loop (triggered by surrounding code)
# required the API to be run in a Thread, so it doesn't block.
api_thread = Thread(target=my_api_server.start, daemon=False)
api_thread.start()
SLEEP_TIME = 3
for i in range(SLEEP_TIME):
    logging.debug(f"Sleeping: {SLEEP_TIME - i}")
    time.sleep(1)

logging.debug(f"Adding new room settings message to queue")

# It is PARAMOUNT that all methods on the API server are called threadsafe. Otherwise, you might
# run into race conditions or locks. Use asyncio.run_coroutine_threadsafe whenever possible !
asyncio.run_coroutine_threadsafe(
    my_api_server.add_outgoing_game_server_message_to_queue(my_outgoing_game_server_message),
    event_loop
)
