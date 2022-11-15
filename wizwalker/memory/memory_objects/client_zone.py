from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memtypes import *


class ClientZone(PropertyClass):
    """
    Base class for ClientZones
    """
    @staticmethod
    def obj_size() -> int:
        # unverified
        108

    zone_id = MemInt64(72)

    zone_name = MemCppString(88)

