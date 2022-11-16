from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memonster.memtypes import *
from wizwalker.memory.memonster import memclass


@memclass
class ClientZone(PropertyClass):
    """
    Base class for ClientZones
    """
    def fieldsize(self) -> int:
        # unverified
        return 108

    zone_id = MemInt64(72)

    zone_name = MemCppString(88)

