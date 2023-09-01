import asyncio
import datetime
import logging
import struct
from typing import Callable, Optional, Union

from battlebit_community_server_api.command.Command import Command
from battlebit_community_server_api.handler.DefaultHandlers import DefaultHandlers
from battlebit_community_server_api.helper.StructHelper import read_uint8
from battlebit_community_server_api.model.OutgoingGameServerMessage import OutgoingGameServerMessage
from battlebit_community_server_api.service.TcpParsingService import TcpParsingService
from battlebit_community_server_api.model.OpCodes import OpCodes


class GameServerCommunicationService:
    """
    The GameServerCommunicationService is responsible for establishing and maintaining the TCP socket connection
    to the GameServer. It also forwards raw data messages in both directions.
    """
    PACKET_SIZE = 1024 * 1024 * 4  # 4MB
    KEEP_ALIVE_FREQUENCY = 15  # Seconds
    KEEP_ALIVE_MESSAGE = b"\x00\x00\x00\x00"
    TIMEOUT_AFTER = 60  # Seconds

    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._socket_server: Optional[asyncio.Server] = None
        self._handler_register: dict[OpCodes, Callable] = {}
        self._queue = set()
        self._writer: Optional[asyncio.StreamWriter] = None
        self._reader: Optional[asyncio.StreamReader] = None

    async def start(self) -> None:
        self._socket_server = await asyncio.start_server(self._handle_incoming_connection, self._host, self._port,
                                                         limit=self.PACKET_SIZE, start_serving=False)
        await self._socket_server.serve_forever()

    async def _handle_incoming_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        logging.debug(f"New connection from: {writer.get_extra_info('peername')}")
        self._writer, self._reader = writer, reader
        await self._handle_incoming_data()
        logging.debug(f"Connection with {writer.get_extra_info('peername')} has been closed!")

    async def _handle_incoming_data(self) -> None:
        # ToDo: Handle OSError
        last_packet_sent = datetime.datetime.now()
        last_packet_received = datetime.datetime.now()
        while True:
            # Setting current timestamp
            now = datetime.datetime.now()
            # Wait for new packet
            try:
                data = await self._reader.read(self.PACKET_SIZE)
            except ConnectionResetError:
                logging.error("ConnectionReset!!")
                self._writer, self._reader = None, None
                return
            # Special case: Receiving HAIL
            if read_uint8(data)[0] == OpCodes.HAIL:
                logging.debug("Received HAIL...")
                try:
                    self._writer.write(await self._handler_register[OpCodes.HAIL](data))
                except KeyError:
                    self._writer.write(await DefaultHandlers.get_default_handler_by_op_code(OpCodes.HAIL)(data))
                await self._writer.drain()
                continue
            # Unpack received data in messages
            messages = TcpParsingService.split_data_into_individual_messages(data)
            # Handling possible timeout scenario
            if not messages and last_packet_received + datetime.timedelta(seconds=self.TIMEOUT_AFTER) < now:
                logging.error("Gameserver closed the connection")
                return
            last_packet_received = now  # Updating timestamp
            # Triggering handlers for messages
            for message in messages:
                op_code, bytes_ = message
                # Logging
                if op_code not in (OpCodes.GAME_TICK, OpCodes.NOTIFY_NEW_ROUND_STATE):
                    logging.debug(f"Received {op_code.name} message...")
                # Check for custom handlers
                if op_code in self._handler_register.keys():
                    handler_result = await self._handler_register[op_code](bytes_)
                # Execute default handler if no custom handler present
                else:
                    try:
                        handler_result = await DefaultHandlers.get_default_handler_by_op_code(op_code)(bytes_)
                    except NotImplementedError as err:
                        logging.error(err)
                        continue

                # If handler returned any result
                if handler_result:
                    last_packet_sent = now
                    self._writer.write(handler_result)
                    await self._writer.drain()

            # Checking if keepalive message is needed, and send one if it is.
            if last_packet_sent + datetime.timedelta(seconds=self.KEEP_ALIVE_FREQUENCY) < datetime.datetime.now():
                last_packet_sent = now
                self._writer.write(self.KEEP_ALIVE_MESSAGE)
                await self._writer.drain()

    async def _execute_command_or_outgoing_game_server_message(self, command_or_msg: Union[Command, OutgoingGameServerMessage]) -> None:
        if hasattr(command_or_msg, "command_string"):  # FixMe: isinstance() seems to not be working
            command = command_or_msg
            logging.debug(f"Executing command: {command}")
            if not self._writer:
                # ToDo: Shit way of doing this
                await asyncio.sleep(1)
                await self._execute_command_or_outgoing_game_server_message(command)
            else:
                message = OutgoingGameServerMessage(op_code=OpCodes.EXECUTE_COMMAND)
                message.add_bytes(struct.pack("H", len(command)))
                message.add_string(command.as_string())
                self._writer.write(message.serialize())
                await self._writer.drain()
        elif hasattr(command_or_msg, "serialize"):
            msg = command_or_msg
            logging.debug(f"Executing outgoing game server message: {msg}")
            if not self._writer:
                # ToDo: Shit way of doing this
                await asyncio.sleep(1)
                await self._execute_command_or_outgoing_game_server_message(msg)
            else:
                self._writer.write(msg.serialize())
                await self._writer.drain()
        else:
            logging.warning(f"Unknown type queued for execution: {type(command_or_msg)}")

    def register_handler(self, op_code: OpCodes, handler: Callable) -> None:
        self._handler_register[op_code] = handler

    async def add_command_to_queue(self, command: Command) -> None:
        task = asyncio.create_task(self._execute_command_or_outgoing_game_server_message(command))
        self._queue.add(task)
        task.add_done_callback(self._queue.discard)

    async def add_outgoing_game_server_message_to_queue(self, msg: OutgoingGameServerMessage) -> None:
        task = asyncio.create_task(self._execute_command_or_outgoing_game_server_message(msg))
        self._queue.add(task)
        task.add_done_callback(self._queue.discard)
