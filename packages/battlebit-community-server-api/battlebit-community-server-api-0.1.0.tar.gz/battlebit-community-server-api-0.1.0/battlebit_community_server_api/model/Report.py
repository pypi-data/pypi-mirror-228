from dataclasses import dataclass
from typing import Optional

from battlebit_community_server_api.model.SteamId import SteamId
from battlebit_community_server_api.model.ReportReason import ReportReason


@dataclass
class Report:
    reporter: SteamId
    reported: SteamId
    reason: ReportReason
    additional_info: Optional[str] = None
