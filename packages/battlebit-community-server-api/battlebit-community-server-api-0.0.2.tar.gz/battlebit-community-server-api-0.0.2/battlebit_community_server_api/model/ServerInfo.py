from dataclasses import dataclass

from battlebit_community_server_api.model.GameState import GameState
from battlebit_community_server_api.model.MapSize import MapSize
from battlebit_community_server_api.model.RoomSettings import RoomSettings


@dataclass
class ServerInfo:
    name: str
    version: str
    port: int
    protected: bool
    game_mode: str
    map_name: str
    map_size: MapSize
    is_day_mode: bool
    current_players: int
    queued_players: int
    max_players: int
    loading_screen_text: str
    rules_text: str
    game_state: GameState
    seconds_left_in_round: int
    room_settings: RoomSettings

    def generate_log(self) -> str:
        return f"Server: {self.name}\n" \
               f"Version: {self.version}\n" \
               f"Port: {self.port} ({'' if self.protected else 'un'}protected)\n" \
               f"Game Mode: {self.game_mode}\n" \
               f"Map: {self.map_name} (Size: {MapSize(self.map_size).name.replace('_', ' ').strip()})\n" \
               f"Day Mode: {'Yes' if self.is_day_mode == 0 else 'No'}\n" \
               f"Players (current/in queue/max): {self.current_players}/{self.queued_players}/{self.max_players}\n" \
               f"Loading Screen Text: {self.loading_screen_text}\n" \
               f"Rules: {self.rules_text}\n" \
               f"Game State: {GameState(self.game_state).name.replace('_', ' ')}\n" \
               f"Seconds left: {self.seconds_left_in_round}"
