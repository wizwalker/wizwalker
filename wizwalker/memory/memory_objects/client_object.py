from typing import List, Optional

from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memtypes import *
from .behavior_instance import BehaviorInstance
from .actor_body import ActorBody


class ClientObject(PropertyClass):
    """
    Base class for ClientObjects
    """

    @staticmethod
    def obj_size() -> int:
        # unverified
        return 552

    global_id_full = MemUInt64(72)
    perm_id = MemUInt64(80)

    template_id_full = MemUInt64(96)

    debug_name = MemCppString(104)

    display_key = MemCppString(136)

    mobile_id = MemUInt16(164)
    location = MemXYZ(168)
    
    orientation = MemOrient(180)

    speed_multiplier = MemUInt16(192)
    scale = MemFloat32(196)

    zone_tag_id = MemUInt32(334)

    character_id = MemUInt64(440)

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
    # async def object_name(self) -> Optional[str]:
    #     """
    #     This client object's object name if it has one
    #     """
    #     object_template = await self.object_template()
    #     if object_template is not None:
    #         return await object_template.object_name()

    #     # explict None
    #     return None

    # # helper method
    # async def display_name(self) -> Optional[str]:
    #     """
    #     This client object's display name if it has one
    #     """
    #     object_template = await self.object_template()
    #     if object_template is not None:
    #         display_name_code = await object_template.display_name()
    #         # this is sometimes just a blank string
    #         if display_name_code:
    #             return await self.hook_handler.client.cache_handler.get_langcode_name(display_name_code)

    #     # explict None
    #     return None

    # # note: not defined
    # async def parent(self) -> Optional["DynamicClientObject"]:
    #     """
    #     This client object's parent or None if it is the root client object

    #     Returns:
    #         DynamicClientObject
    #     """
    #     addr = await self.read_value_from_offset(208, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicClientObject(self.hook_handler, addr)

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

    # # note: not defined
    # async def client_zone(self) -> Optional["DynamicClientZone"]:
    #     """
    #     This client object's client zone or None

    #     Returns:
    #         DynamicClientZone
    #     """
    #     addr = await self.read_value_from_offset(304, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicClientZone(self.hook_handler, addr)

    # # note: not defined
    # async def object_template(self) -> Optional[WizGameObjectTemplate]:
    #     """
    #     This client object's template object

    #     Returns:
    #         DynamicWizGameObjectTemplate
    #     """
    #     addr = await self.read_value_from_offset(88, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicWizGameObjectTemplate(self.hook_handler, addr)

    # # Note: not defined
    # async def game_stats(self) -> Optional[DynamicGameStats]:
    #     """
    #     This client object's game stats or None if doesn't have them

    #     Returns:
    #         DynamicGameStats
    #     """
    #     addr = await self.read_value_from_offset(544, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicGameStats(self.hook_handler, addr)


# TODO: Update
class CurrentClientObject(ClientObject):
    """
    Client object tied to the client hook
    """

    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_client_base()
