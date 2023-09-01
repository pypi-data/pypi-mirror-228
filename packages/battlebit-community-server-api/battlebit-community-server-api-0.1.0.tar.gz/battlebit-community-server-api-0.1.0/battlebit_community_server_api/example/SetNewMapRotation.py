import asyncio
import logging
import time
from threading import Thread

from battlebit_community_server_api.ApiServer import ApiServer, build_api_server
from battlebit_community_server_api.command.Command import SetMapRotation
from battlebit_community_server_api.model.Map import Map

event_loop = asyncio.new_event_loop()
my_api_server: ApiServer = build_api_server("0.0.0.0", 30000, event_loop)

# Construct new map rotation
new_map_rotation = [
    Map.DUSTY_DEW,
    Map.MULTU_ISLANDS,
    Map.OIL_DUNES,
    Map.SANDY_SUNSET
]


# Prepare command
my_command = SetMapRotation(new_map_rotation)


logging.basicConfig(level=logging.DEBUG)  # Optional: If you want to have an in-depth view into what's going on.

# Adding Command to the queue from outside the main loop (triggered by surrounding code)
# required the API to be run in a Thread, so it doesn't block.
api_thread = Thread(target=my_api_server.start, daemon=False)
api_thread.start()
SLEEP_TIME = 3
for i in range(SLEEP_TIME):
    logging.debug(f"Sleeping: {SLEEP_TIME - i}")
    time.sleep(1)

logging.debug(f"Adding SetMapRotation command to queue")

# It is PARAMOUNT that all methods on the API server are called threadsafe. Otherwise, you might
# run into race conditions or locks. Use asyncio.run_coroutine_threadsafe whenever possible !
asyncio.run_coroutine_threadsafe(
    my_api_server.add_command_to_queue(my_command),
    event_loop
)
