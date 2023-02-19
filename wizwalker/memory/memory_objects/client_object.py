from typing import List, Optional

from wizwalker import XYZ
from wizwalker.memory.memory_object import PropertyClass, DynamicMemoryObject
from wizwalker.memory.memory_objects import ActorBody
from .game_stats import DynamicGameStats
from .game_object_template import WizGameObjectTemplate
from .behavior_instance import DynamicBehaviorInstance
from .client_zone import ClientZone

from memonster import LazyType
from memonster.memtypes import *
from memtypes import *


class ClientObject(PropertyClass):
    """
    Base class for ClientObjects
    """
    # TODO: monsterify
    # TODO: test if this is actually active behaviors
    async def inactive_behaviors(self) -> List[DynamicBehaviorInstance]:
        """
        This client object's inactive behaviors

        Returns:
            List of DynamicBehaviorInstace
        """
        behaviors = []
        for addr in await self.read_shared_vector(224):
            if addr != 0:
                behaviors.append(DynamicBehaviorInstance(self.hook_handler, addr))

        return behaviors

    # helper method
    async def actor_body(self) -> Optional[DynamicActorBody]:
        for behavior in await self.inactive_behaviors():
            if await behavior.behavior_name() == "AnimationBehavior":
                addr = await behavior.read_value_from_offset(0x70, "unsigned long long")

                if addr == 0:
                    return None

                return DynamicActorBody(self.hook_handler, addr)

    # helper method
    async def object_name(self) -> Optional[str]:
        """
        This client object's object name if it has one
        """
        object_template = await self.object_template()
        if object_template is not None:
            return await object_template.object_name()

        # explict None
        return None

    # helper method
    async def display_name(self) -> Optional[str]:
        """
        This client object's display name if it has one
        """
        object_template = await self.object_template()
        if object_template is not None:
            display_name_code = await object_template.display_name()
            # this is sometimes just a blank string
            if display_name_code:
                return await self.hook_handler.client.cache_handler.get_langcode_name(display_name_code)

        # explict None
        return None

    # note: not defined
    async def children(self) -> List["DynamicClientObject"]:
        """
        This client object's child client objects

        Returns:
            List of DynamicClientObject
        """
        children = []
        for addr in await self.read_shared_vector(384):
            children.append(DynamicClientObject(self.hook_handler, addr))

        return children

    def __init__(self, offset: int) -> None:
        super().__init__(offset)

        # note: note defined
        self.parent = MemPointer(208, LazyType(ClientObject)(0))

    global_id_full = MemUInt64(72)
    perm_id = MemUInt64(80)
    # note: not defined
    object_template = MemPointer(88, WizGameObjectTemplate(0))

    template_id_full = MemUInt64(96)
    debug_name = MemCppString(104)

    display_key = MemCppString(136)

    location = MemXYZ(168)
    orientation = MemOrient(180)
    speed_multiplier = MemInt16(192)
    mobile_id = MemUInt16(194)
    scale = MemFloat32(196)

    # note: not defined
    client_zone = MemPointer(304, ClientZone(0))
    
    zone_tag_id = MemUInt32(334)

    character_id = MemUInt64(440)

    # Note: not defined
    async def game_stats(self) -> Optional[DynamicGameStats]:
        """
        This client object's game stats or None if doesn't have them

        Returns:
            DynamicGameStats
        """
        addr = await self.read_value_from_offset(544, "long long")

        if addr == 0:
            return None

        return DynamicGameStats(self.hook_handler, addr)


class CurrentClientObject(ClientObject):
    """
    Client object tied to the client hook
    """

    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_client_base()


class DynamicClientObject(DynamicMemoryObject, ClientObject):
    """
    Dynamic client object that can take an address
    """

    pass
