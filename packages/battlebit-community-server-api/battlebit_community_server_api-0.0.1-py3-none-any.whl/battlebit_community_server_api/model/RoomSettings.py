from dataclasses import dataclass


@dataclass
class RoomSettings:
    damage_multiplier: float
    friendly_fire_enabled: bool
    hide_map_votes: bool
    only_winner_team_can_vote: bool

    medic_limit_per_squad: int
    engineer_limit_per_squad: int
    support_limit_per_squad: int
    recon_limit_per_squad: int
