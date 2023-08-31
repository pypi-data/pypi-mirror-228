import struct
from dataclasses import dataclass


@dataclass
class PlayerProgress:
    kill_count: int
    leader_kills: int
    assault_kills: int
    medic_kills: int
    engineer_kills: int
    support_kills: int
    recon_kills: int
    death_count: int
    win_count: int
    lose_count: int
    friendly_shots: int
    friendly_kills: int
    revived: int
    revived_team_mates: int
    assists: int
    prestige: int
    rank: int
    exp: int
    shots_fired: int
    shots_hit: int
    headshots: int
    objectives_completed: int
    healed_hp: int
    road_kills: int
    suicides: int
    vehicles_destroyed: int
    vehicle_hp_repaired: int
    longest_kill: int
    play_time_seconds: int
    leader_play_time: int
    assault_play_time: int
    medic_play_time: int
    engineer_play_time: int
    support_play_time: int
    recon_play_time: int
    leader_score: int
    assault_score: int
    medic_score: int
    engineer_score: int
    support_score: int
    recon_score: int
    total_score: int

    def __len__(self) -> int:
        """ Returns the number of attributes """
        return len(self.__dict__)

    def to_bytes(self) -> bytes:
        out = struct.pack("I", len(self))
        out += struct.pack("I", self.kill_count)
        out += struct.pack("I", self.leader_kills)
        out += struct.pack("I", self.assault_kills)
        out += struct.pack("I", self.medic_kills)
        out += struct.pack("I", self.engineer_kills)
        out += struct.pack("I", self.support_kills)
        out += struct.pack("I", self.recon_kills)
        out += struct.pack("I", self.death_count)
        out += struct.pack("I", self.win_count)
        out += struct.pack("I", self.lose_count)
        out += struct.pack("I", self.friendly_shots)
        out += struct.pack("I", self.friendly_kills)
        out += struct.pack("I", self.revived)
        out += struct.pack("I", self.revived_team_mates)
        out += struct.pack("I", self.assists)
        out += struct.pack("I", self.prestige)
        out += struct.pack("I", self.rank)
        out += struct.pack("I", self.exp)
        out += struct.pack("I", self.shots_fired)
        out += struct.pack("I", self.shots_hit)
        out += struct.pack("I", self.headshots)
        out += struct.pack("I", self.objectives_completed)
        out += struct.pack("I", self.healed_hp)
        out += struct.pack("I", self.road_kills)
        out += struct.pack("I", self.suicides)
        out += struct.pack("I", self.vehicles_destroyed)
        out += struct.pack("I", self.vehicle_hp_repaired)
        out += struct.pack("I", self.longest_kill)
        out += struct.pack("I", self.play_time_seconds)
        out += struct.pack("I", self.leader_play_time)
        out += struct.pack("I", self.assault_play_time)
        out += struct.pack("I", self.medic_play_time)
        out += struct.pack("I", self.engineer_play_time)
        out += struct.pack("I", self.support_play_time)
        out += struct.pack("I", self.recon_play_time)
        out += struct.pack("I", self.leader_score)
        out += struct.pack("I", self.assault_score)
        out += struct.pack("I", self.medic_score)
        out += struct.pack("I", self.engineer_score)
        out += struct.pack("I", self.support_score)
        out += struct.pack("I", self.recon_score)
        out += struct.pack("I", self.total_score)
        return out


def build_player_progress_from_bytes(buf: bytes) -> tuple[PlayerProgress, bytes]:
    """ Builds a PlayerProgress object from bytes and returns this alongside of the remaining, unread bytes. """
    parameter_count = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    kill_count = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    leader_kills = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    assault_kills = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    medic_kills = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    engineer_kills = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    support_kills = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    recon_kills = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    death_count = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    win_count = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    lose_count = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    friendly_shots = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    friendly_kills = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    revived = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    revived_team_mates = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    assists = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    prestige = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    rank = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    exp = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    shots_fired = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    shots_hit = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    headshots = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    objectives_completed = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    healed_hp = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    road_kills = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    suicides = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    vehicles_destroyed = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    vehicle_hp_repaired = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    longest_kill = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    play_time_seconds = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    leader_play_time = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    assault_play_time = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    medic_play_time = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    engineer_play_time = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    support_play_time = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    recon_play_time = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    leader_score = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    assault_score = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    medic_score = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    engineer_score = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    support_score = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    recon_score = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]
    total_score = struct.unpack("I", buf[:4])[0]
    buf = buf[4:]

    return PlayerProgress(kill_count=kill_count,
                          leader_kills=leader_kills,
                          assault_kills=assault_kills,
                          medic_kills=medic_kills,
                          engineer_kills=engineer_kills,
                          support_kills=support_kills,
                          recon_kills=recon_kills,
                          death_count=death_count,
                          win_count=win_count,
                          lose_count=lose_count,
                          friendly_shots=friendly_shots,
                          friendly_kills=friendly_kills,
                          revived=revived,
                          revived_team_mates=revived_team_mates,
                          assists=assists,
                          prestige=prestige,
                          rank=rank,
                          exp=exp,
                          shots_fired=shots_fired,
                          shots_hit=shots_hit,
                          headshots=headshots,
                          objectives_completed=objectives_completed,
                          healed_hp=healed_hp,
                          road_kills=road_kills,
                          suicides=suicides,
                          vehicles_destroyed=vehicles_destroyed,
                          vehicle_hp_repaired=vehicle_hp_repaired,
                          longest_kill=longest_kill,
                          play_time_seconds=play_time_seconds,
                          leader_play_time=leader_play_time,
                          assault_play_time=assault_play_time,
                          medic_play_time=medic_play_time,
                          engineer_play_time=engineer_play_time,
                          support_play_time=support_play_time,
                          recon_play_time=recon_play_time,
                          leader_score=leader_score,
                          assault_score=assault_score,
                          medic_score=medic_score,
                          engineer_score=engineer_score,
                          support_score=support_score,
                          recon_score=recon_score,
                          total_score=total_score), buf
