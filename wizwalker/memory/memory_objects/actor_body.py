from typing import Optional

from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memtypes import *


class ActorBody(PropertyClass):
    """
    Base class for ActorBody
    """

    @staticmethod
    def obj_size() -> int:
        return 140

    # note: internal
    # TODO: Make work
    """
    async def parent_client_object(self) -> Optional["memory_objects.DynamicClientObject"]:
        addr = await self.read_value_from_offset(72, "unsigned long long")

        if addr == 0:
            return None

        return memory_objects.DynamicClientObject(self.hook_handler, addr)
    """

    position = MemXYZ(88)

    orientation = MemOrient(100)
    pitch = MemFloat32(100)
    roll = MemFloat32(104)
    yaw = MemFloat32(108)

    height = MemFloat32(132)
    scale = MemFloat32(112)

    model_update_scheduled = MemBool(136)


# TODO: Update
class CurrentActorBody(ActorBody):
    """
    Actor body tied to the player hook
    """

    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_player_base()
