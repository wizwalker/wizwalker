from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memonster.memtypes import *
from wizwalker.memory.memonster import memclass


@memclass
class BehaviorTemplate(PropertyClass):
    """
    Base class for behavior templates
    """

    def fieldsize(self) -> int:
        # unverified
        return 90

    behavior_name = MemCppString(72)
