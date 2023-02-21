from wizwalker import XYZ

from memonster.memtypes import *
from .memtypes import *


# TODO: Monster
class CurrentQuestPosition(MemType):
    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_quest_base()

    position = MemXYZ(0)
