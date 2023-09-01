from dataclasses import dataclass

from battlebit_community_server_api.model.MapSize import MapSize
from battlebit_community_server_api.model.RoomSettings import RoomSettings
from battlebit_community_server_api.model.Gamemode import Gamemode
from battlebit_community_server_api.model.Map import Map
from battlebit_community_server_api.model.RoundState import RoundState


@dataclass
class ServerInfo:
    name: str
    version: str
    port: int
    protected: bool
    game_mode: Gamemode
    map_name: Map
    map_size: MapSize
    is_day_mode: bool
    current_players: int
    queued_players: int
    max_players: int
    loading_screen_text: str
    rules_text: str
    round_state: RoundState
    room_settings: RoomSettings
    gamemode_rotation: list[Gamemode]
    map_rotation: list[Map]

    def generate_log(self) -> str:
        return f"Server: {self.name}\n" \
               f"Version: {self.version}\n" \
               f"Port: {self.port} ({'' if self.protected else 'un'}protected)\n" \
               f"Game Mode: {self.game_mode.value}\n" \
               f"Map: {self.map_name.value} (Size: {MapSize(self.map_size).name.replace('_', ' ').strip()})\n" \
               f"Day Mode: {'Yes' if self.is_day_mode == 0 else 'No'}\n" \
               f"Players (current/in queue/max): {self.current_players}/{self.queued_players}/{self.max_players}\n" \
               f"Loading Screen Text: {self.loading_screen_text}\n" \
               f"Rules: {self.rules_text}\n"
