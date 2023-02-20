from typing import List

from wizwalker.memory.memory_object import PropertyClass

from memonster.memtypes import *
from memtypes import *


class CharacterRegistry(PropertyClass):
    active_quest_id = MemUInt64(304)

    active_goal_id = MemUInt32(336)
