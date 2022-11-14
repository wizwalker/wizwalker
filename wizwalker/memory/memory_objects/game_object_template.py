from typing import List

from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memtypes import *
from .enums import ObjectType
from .behavior_template import BehaviorTemplate


class WizGameObjectTemplate(PropertyClass):
    @staticmethod
    def obj_size() -> int:
        return 520

    object_name = MemCppString(96)
    template_id = MemUInt32(128)
    visual_id = MemUInt32(132)
    description = MemCppString(136)
    display_name = MemCppString(168)
    object_type = MemEnum(ObjectType, 200)
    icon = MemCppString(208)
    exempt_from_aoi = MemBool(240)
    adjective_list = MemCppString(248)
    loot_table = MemCppString(280)
    death_particles = MemCppString(296)
    death_sound = MemCppString(328)
    hit_sound = MemCppString(360)
    cast_sound = MemCppString(392)
    aggro_sound = MemCppString(424)
    primary_school_name = MemCppString(456)
    location_preference = MemCppString(488)


    # TODO: Make work
    # # TODO: add all behavior template types
    # async def behaviors(self) -> List[DynamicBehaviorTemplate]:
    #     behaviors = []
    #     for addr in await self.read_dynamic_vector(72):
    #         # they sometimes set these to 0
    #         if addr != 0:
    #             behaviors.append(DynamicBehaviorTemplate(self.hook_handler, addr))

    #     return behaviors
