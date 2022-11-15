from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memtypes import *


class BehaviorTemplate(PropertyClass):
    """
    Base class for behavior templates
    """

    @staticmethod
    def obj_size() -> int:
        # unverified
        return 90

    behavior_name = MemCppString(72)
