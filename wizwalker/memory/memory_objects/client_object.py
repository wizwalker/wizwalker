from typing import List, Optional

from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memonster.memtypes import *
from wizwalker.memory.memonster import memclass
from .game_stats import GameStats
from .game_object_template import WizGameObjectTemplate
from .behavior_instance import BehaviorInstance
from .client_zone import ClientZone
from .actor_body import ActorBody


@memclass(False)
class _ClientObjectClientObjectPtr(MemPointer["ClientObject"]):
    def __post_init__(self):
        self._lazy_dummy = LazyDummy(ClientObject, (0,))
        return super().__post_init__()

class _ClientObject(MemType):
    pass

@memclass
class ClientObject(PropertyClass):
    """
    Base class for ClientObjects
    """
    def fieldsize(self) -> int:
        # unverified
        return 552

    global_id_full = MemUInt64(72)
    perm_id = MemUInt64(80)
    
    # note: not defined
    object_template = MemPointer[WizGameObjectTemplate](88, WizGameObjectTemplate)

    template_id_full = MemUInt64(96)

    debug_name = MemCppString(104)

    display_key = MemCppString(136)

    mobile_id = MemUInt16(164)
    location = MemXYZ(168)
    
    orientation = MemOrient(180)

    speed_multiplier = MemUInt16(192)
    scale = MemFloat32(196)
    
    # note: not defined
    parent = MemPointer(208, _ClientObject)

    # TODO: test if this is actually active behaviors
    inactive_behaviors = MemCppVector(224, MemCppSharedPointer(0, BehaviorInstance))

    # note: not defined
    client_zone = MemPointer[ClientZone](304, ClientZone)

    zone_tag_id = MemUInt32(334)

    # note: not defined
    children = MemCppVector(384, MemCppSharedPointer(0, _ClientObject))

    character_id = MemUInt64(440)

    # Note: not defined
    game_stats = MemPointer[GameStats](544, GameStats)

    # helper method
    def object_name(self) -> Optional[str]:
        """
        This client object's object name if it has one
        """
        object_template = self.object_template.read()
        if not object_template.isnull():
            return object_template.object_name.read()

        # explict None
        return None

    # helper method
    def actor_body(self) -> Optional[ActorBody]:
        for behavior in self.inactive_behaviors.read():
            behavior: BehaviorInstance
            if behavior.behavior_name() == "AnimationBehavior":
                view = behavior._view.ptr_view(ActorBody().fieldsize(), 0x70)
                if view.backend.address() == 0:
                    return None
                return ActorBody.from_view(view)


    # TODO: Make work
    # # helper method
    # async def display_name(self) -> Optional[str]:
    #     """
    #     This client object's display name if it has one
    #     """
    #     object_template = self.object_template.read()
    #     if not object_template.isnull():
    #         display_name_code = object_template.display_name.read()
    #         # this is sometimes just a blank string
    #         if display_name_code:
    #             return await self.hook_handler.client.cache_handler.get_langcode_name(display_name_code)

    #     # explict None
    #     return None



# TODO: Update
class CurrentClientObject(ClientObject):
    """
    Client object tied to the client hook
    """

    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_client_base()
