from memonster.memtypes import *
from .memtypes import *


# TODO: Monster
class TeleportHelper(MemType):
    async def read_base_address(self) -> int:
        return await self.hook_handler.read_teleport_helper()

    position = MemXYZ(0)
    should_update = MemBool(12)
    target_object_address = MemUInt64(13)
