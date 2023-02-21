from wizwalker.memory.memory_object import PropertyClass

from memonster.memtypes import *
from .memtypes import *


class BehaviorTemplate(PropertyClass):
    """
    Base class for behavior templates
    """

    behavior_name = MemCppString(72)
