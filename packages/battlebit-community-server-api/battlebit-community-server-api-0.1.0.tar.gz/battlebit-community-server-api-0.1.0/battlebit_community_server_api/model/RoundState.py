from dataclasses import dataclass

from battlebit_community_server_api.model.GameState import GameState


@dataclass
class RoundState:
    game_state: GameState
    team_a_tickets: int
    team_b_tickets: int
    max_tickets: int
    players_to_start: int
    seconds_left: int
