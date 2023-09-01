from dataclasses import dataclass

from battlebit_community_server_api.helper.StructHelper import *


@dataclass
class RoomSettings:
    damage_multiplier: float
    friendly_fire_enabled: bool
    hide_map_votes: bool
    only_winner_team_can_vote: bool
    player_collision_enabled: bool

    medic_limit_per_squad: int
    engineer_limit_per_squad: int
    support_limit_per_squad: int
    recon_limit_per_squad: int

    can_vote_for_day: bool
    can_vote_for_night: bool

    tank_spawn_delay_multiplier: float
    transport_spawn_delay_multiplier: float
    sea_vehicle_spawn_delay_multiplier: float
    apc_spawn_delay_multiplier: float
    helicopter_spawn_delay_multiplier: float

    unlock_all_attachments: bool
    teamless_mode_enabled: bool
    squad_required_to_change_role: bool

    def to_bytes(self) -> bytes:
        out = write_float32(self.damage_multiplier)
        out += write_bool(self.friendly_fire_enabled)
        out += write_bool(self.hide_map_votes)
        out += write_bool(self.only_winner_team_can_vote)
        out += write_bool(self.player_collision_enabled)

        out += write_uint8(self.medic_limit_per_squad)
        out += write_uint8(self.engineer_limit_per_squad)
        out += write_uint8(self.support_limit_per_squad)
        out += write_uint8(self.recon_limit_per_squad)

        out += write_bool(self.can_vote_for_day)
        out += write_bool(self.can_vote_for_night)

        out += write_float32(self.tank_spawn_delay_multiplier)
        out += write_float32(self.transport_spawn_delay_multiplier)
        out += write_float32(self.sea_vehicle_spawn_delay_multiplier)
        out += write_float32(self.apc_spawn_delay_multiplier)
        out += write_float32(self.helicopter_spawn_delay_multiplier)

        out += write_bool(self.unlock_all_attachments)
        out += write_bool(self.teamless_mode_enabled)
        out += write_bool(self.squad_required_to_change_role)
        return out


def from_bytes(data: bytes) -> RoomSettings:
    damage_multiplier, data = read_float32(data)
    friendly_fire_enabled, data = read_bool(data)
    hide_map_votes, data = read_bool(data)
    only_winner_team_can_vote, data = read_bool(data)
    player_collision_enabled, data = read_bool(data)

    medic_limit_per_squad, data = read_uint8(data)
    engineer_limit_per_squad, data = read_uint8(data)
    support_limit_per_squad, data = read_uint8(data)
    recon_limit_per_squad, data = read_uint8(data)

    can_vote_for_day, data = read_bool(data)
    can_vote_for_night, data = read_bool(data)

    tank_spawn_delay_multiplier, data = read_float32(data)
    transport_spawn_delay_multiplier, data = read_float32(data)
    sea_vehicle_spawn_delay_multiplier, data = read_float32(data)
    apc_spawn_delay_multiplier, data = read_float32(data)
    helicopter_spawn_delay_multiplier, data = read_float32(data)

    unlock_all_attachments, data = read_bool(data)
    teamless_mode_enabled, data = read_bool(data)
    squad_required_to_change_role, data = read_bool(data)

    return RoomSettings(damage_multiplier, friendly_fire_enabled, hide_map_votes, only_winner_team_can_vote,
                        player_collision_enabled, medic_limit_per_squad, engineer_limit_per_squad,
                        support_limit_per_squad, recon_limit_per_squad, can_vote_for_day, can_vote_for_night,
                        tank_spawn_delay_multiplier, transport_spawn_delay_multiplier,
                        sea_vehicle_spawn_delay_multiplier, apc_spawn_delay_multiplier,
                        helicopter_spawn_delay_multiplier, unlock_all_attachments, teamless_mode_enabled,
                        squad_required_to_change_role)
