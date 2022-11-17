from typing import List

from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memonster import memclass
from wizwalker.memory.memonster.memtypes import *
from .enums import ObjectType
from .behavior_template import BehaviorTemplate


@memclass
class WizGameObjectTemplate(PropertyClass):
    def fieldsize(self) -> int:
        # unverified
        return 520

    behaviors = MemCppVector(72, MemPointer[BehaviorTemplate](0, BehaviorTemplate))

    object_name = MemCppString(96)
    template_id = MemUInt32(128)
    visual_id = MemUInt32(132)
    description = MemCppString(136)
    display_name = MemCppString(168)
    object_type = MemEnum(200, ObjectType)
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

