from typing import Optional

from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memory_objects import ActorBody
from .game_stats import GameStats
from .game_object_template import WizGameObjectTemplate
from .behavior_instance import BehaviorInstance
from .client_zone import ClientZone

from memonster import LazyType
from memonster.memtypes import *
from .memtypes import *


class ClientObject(PropertyClass):
    """
    Base class for ClientObjects
    """
    # helper method
    def actor_body(self) -> Optional[ActorBody]:
        for behavior_ptr in self.inactive_behaviors.read():
            behavior = behavior_ptr.read()
            if behavior.behavior_name() == "AnimationBehavior":
                return behavior.cast_offset(0x70, ActorBody)

    # helper method
    def object_name(self) -> Optional[str]:
        """
        This client object's object name if it has one
        """
        object_template = self.object_template.read()
        # TODO: Better error handling
        try:
            return object_template.object_name.read()
        except:
            return None

    # helper method
    def display_name(self) -> Optional[str]:
        """
        This client object's display name if it has one
        """
        object_template = self.object_template.read()
        try:
            display_name_code = object_template.display_name.read()
            # this is sometimes just a blank string
            if display_name_code:
                # TODO: Rework for memonster
                return self.hook_handler.client.cache_handler.get_langcode_name(display_name_code)
        except:
            return None

    def __init__(self, offset: int) -> None:
        super().__init__(offset)

        # note: note defined
        self.parent = MemPointer(208, LazyType(ClientObject)(0))
        # note: not defined
        self.children = MemCppVector(384, MemCppSharedPointer(0, ClientObject(0)))

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

    # TODO: test if this is actually active behaviors
    inactive_behaviors = MemCppVector(224, MemCppSharedPointer(0, BehaviorInstance(0)))

    # note: not defined
    client_zone = MemPointer(304, ClientZone(0))
    
    zone_tag_id = MemUInt32(334)

    character_id = MemUInt64(440)

    game_stats = MemPointer(544, GameStats(0))


class CurrentClientObject(ClientObject):
    """
    Client object tied to the client hook
    """

    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_client_base()
