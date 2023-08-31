import asyncio
import logging
from asyncio import AbstractEventLoop
from typing import Callable

from battlebit_community_server_api.command.Command import Command
from battlebit_community_server_api.model.OpCodes import OpCodes
from battlebit_community_server_api.service.GameServerCommunicationService import GameServerCommunicationService


class ApiServer:
    def __init__(self, game_server_communication_service: GameServerCommunicationService) -> None:
        self._game_server_communication_service = game_server_communication_service
        # ToDo: This is new in Python 3.10, add a switch for it, if that's the only breaking change to 3.7
        self._main_loop = None

    def start(self) -> None:
        if not self._main_loop:
            self._main_loop = asyncio.new_event_loop()
        self._main_loop.run_until_complete(self._game_server_communication_service.start())

    def register_handler(self, op_code: OpCodes, handler: Callable) -> None:
        self._game_server_communication_service.register_handler(op_code, handler)

    async def add_command_to_queue(self, command: Command) -> None:
        await self._game_server_communication_service.add_command_to_queue(command)

    @property
    def loop(self) -> AbstractEventLoop:
        return self._main_loop

    @loop.setter
    def loop(self, new_loop: AbstractEventLoop) -> None:
        self._main_loop = new_loop


def build_api_server(host: str, port: int) -> ApiServer:
    return ApiServer(
        GameServerCommunicationService(
            host, port
        )
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    api_server = build_api_server("0.0.0.0", 30000)
    logging.debug("Starting BattleBit Community Server Python API")
    api_server.start()
