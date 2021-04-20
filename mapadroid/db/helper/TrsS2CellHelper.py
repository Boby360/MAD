from datetime import datetime
from typing import Optional, List

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from mapadroid.db.model import TrsS2Cell
from mapadroid.utils.collections import Location


class TrsS2CellHelper:
    @staticmethod
    async def get(session: AsyncSession, cell_id: int) -> Optional[TrsS2Cell]:
        stmt = select(TrsS2Cell).where(TrsS2Cell.id == cell_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def get_cells_in_rectangle(session: AsyncSession,
                                    ne_corner: Optional[Location], sw_corner: Optional[Location],
                                    old_ne_corner: Optional[Location] = None, old_sw_corner: Optional[Location] = None,
                                    timestamp: Optional[int] = None) -> List[TrsS2Cell]:
        stmt = select(TrsS2Cell)
        where_conditions = []
        where_conditions.append(and_(TrsS2Cell.latitude >= sw_corner.lat,
                                     TrsS2Cell.longitude >= sw_corner.lng,
                                     TrsS2Cell.latitude <= ne_corner.lat,
                                     TrsS2Cell.longitude <= ne_corner.lng))
        if old_ne_corner and old_sw_corner:
            where_conditions.append(and_(TrsS2Cell.latitude >= old_sw_corner.lat,
                                         TrsS2Cell.longitude >= old_sw_corner.lng,
                                         TrsS2Cell.latitude <= old_ne_corner.lat,
                                         TrsS2Cell.longitude <= old_ne_corner.lng))
        if timestamp:
            where_conditions.append(TrsS2Cell.updated >= timestamp)

        stmt = stmt.where(and_(*where_conditions))
        result = await session.execute(stmt)
        return result.scalars().all()
