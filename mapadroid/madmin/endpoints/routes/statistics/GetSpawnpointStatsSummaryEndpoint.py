from typing import Optional, Tuple, Dict, List

from mapadroid.db.helper.TrsEventHelper import TrsEventHelper
from mapadroid.db.helper.TrsSpawnHelper import TrsSpawnHelper
from mapadroid.db.model import TrsSpawn, TrsEvent
from mapadroid.madmin.endpoints.routes.statistics.AbstractStatistictsRootEndpoint import AbstractStatisticsRootEndpoint
from mapadroid.madmin.functions import get_geofences, generate_coords_from_geofence


class GetSpawnpointStatsSummaryEndpoint(AbstractStatisticsRootEndpoint):
    """
    "/get_spawnpoints_stats_summary"
    """

    # TODO: Auth
    async def get(self):
        possible_fences = await get_geofences(self._get_mapping_manager(), self._session, self._get_instance_id())
        events: List[TrsEvent] = await TrsEventHelper.get_all(self._session)
        spawnpoints_total: int = await TrsSpawnHelper.get_all_spawnpoints_count(self._session)
        stats = {'fences': possible_fences, 'events': events, 'spawnpoints_count': spawnpoints_total}
        # TODO: Any component using it needs to determine "locked" (event.event_name == "DEFAULT") by itself
        return self._json_response(stats)