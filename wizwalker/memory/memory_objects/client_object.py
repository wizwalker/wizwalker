from typing import List, Optional

from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memonster.memtypes import *
from wizwalker.memory.memonster import memclass
from .game_stats import GameStats
from .game_object_template import WizGameObjectTemplate
from .behavior_instance import BehaviorInstance
from .client_zone import ClientZone


@memclass
class _ClientObjectClientObjectPtr(MemPointer["ClientObject"]):
    def __post_init__(self):
        super().__post_init__()
        self._dummy = ClientObject()

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
    object_template = MemPointer[WizGameObjectTemplate](88, WizGameObjectTemplate())

    template_id_full = MemUInt64(96)

    debug_name = MemCppString(104)

    display_key = MemCppString(136)

    mobile_id = MemUInt16(164)
    location = MemXYZ(168)
    
    orientation = MemOrient(180)

    speed_multiplier = MemUInt16(192)
    scale = MemFloat32(196)
    
    # note: not defined
    parent = _ClientObjectClientObjectPtr(208)

    # note: not defined
    client_zone = MemPointer[ClientZone](304, ClientZone())
    zone_tag_id = MemUInt32(334)

    character_id = MemUInt64(440)

    # Note: not defined
    game_stats = MemPointer[GameStats](544, GameStats())


    # helper method
    async def object_name(self) -> Optional[str]:
        """
        This client object's object name if it has one
        """
        object_template = self.object_template.read()
        if not object_template.isnull():
            return object_template.object_name.read()

        # explict None
        return None



    # TODO: Make work

    # # TODO: test if this is actually active behaviors
    # async def inactive_behaviors(self) -> List[BehaviorInstance]:
    #     """
    #     This client object's inactive behaviors

    #     Returns:
    #         List of DynamicBehaviorInstace
    #     """
    #     behaviors = []
    #     for addr in await self.read_shared_vector(224):
    #         if addr != 0:
    #             behaviors.append(BehaviorInstance(self.hook_handler, addr))

    #     return behaviors

    # # helper method
    # async def actor_body(self) -> Optional[ActorBody]:
    #     for behavior in await self.inactive_behaviors():
    #         if await behavior.behavior_name() == "AnimationBehavior":
    #             addr = await behavior.read_value_from_offset(0x70, "unsigned long long")

    #             if addr == 0:
    #                 return None

    #             return DynamicActorBody(self.hook_handler, addr)

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

    # # note: not defined
    # async def children(self) -> List["DynamicClientObject"]:
    #     """
    #     This client object's child client objects

    #     Returns:
    #         List of DynamicClientObject
    #     """
    #     children = []
    #     for addr in await self.read_shared_vector(384):
    #         children.append(DynamicClientObject(self.hook_handler, addr))

    #     return children


# TODO: Update
class CurrentClientObject(ClientObject):
    """
    Client object tied to the client hook
    """

    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_client_base()
