from typing import Optional

from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory import memory_objects

from memory_objects.memtypes import MemXYZ, MemOrient
from memonster import MemFloat32, MemBool, MemPointer


class ActorBody(PropertyClass):
    """
    Base class for ActorBody
    """

    # note: internal
    parent_client_object = MemPointer(72, memory_objects.ClientObject(0))

    position = MemXYZ(88)

    orient = MemOrient(100)

    scale = MemFloat32(112)
    
    height = MemFloat32(132)

    # note: internal
    model_update_scheduled = MemBool(136)


# TODO: memonster
class CurrentActorBody(ActorBody):
    """
    Actor body tied to the player hook
    """

    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_player_base()
