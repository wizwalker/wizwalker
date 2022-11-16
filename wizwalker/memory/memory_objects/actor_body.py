from typing import Optional

from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memonster.memtypes import *
from wizwalker.memory.memonster import memclass
from wizwalker.memory.memory_objects.client_object import _ClientObjectClientObjectPtr


@memclass
class ActorBody(PropertyClass):
    """
    Base class for ActorBody
    """

    def fieldsize(self) -> int:
        # unverified
        return 140

    # note: internal
    parent_client_object = _ClientObjectClientObjectPtr(72)

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
