from wizwalker.memory.memory_object import PropertyClass
from .enums import ObjectType
from .behavior_template import BehaviorTemplate

from memonster.memtypes import *
from .memtypes import *


class WizGameObjectTemplate(PropertyClass):
    # TODO: add all behavior template types
    behaviors = MemCppVector(72, MemPointer(0, BehaviorTemplate(0)))

    object_name = MemCppString(96)
    template_id = MemUInt32(128)
    visual_id = MemUInt32(132)
    description = MemCppString(136)
    display_name = MemCppString(168)
    
    object_type = MemEnum(200, ObjectType)
    icon = MemCppString(208)

    exempt_from_aoi = MemBool(240)
    adjective_list = MemCppString(248)

    # TODO: FIX OFFSETS; original version made no sense
    #loot_table = MemCppString(280)
    death_particles = MemCppString(296)
    death_sound = MemCppString(328)
    hit_sound = MemCppString(360)
    cast_sound = MemCppString(392)
    aggro_sound = MemCppString(424)
    primary_school_name = MemCppString(456)
    location_preference = MemCppString(488)
