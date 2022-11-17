from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memonster.memtypes import *
from wizwalker.memory.memonster import memclass


@memclass
class CharacterRegistry(PropertyClass):
    def fieldsize(self) -> int:
        # unverified
        return 340

    active_quest_id = MemUInt64(304)
    active_goal_id = MemUInt32(336)
