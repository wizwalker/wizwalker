from wizwalker.memory.memory_object import PropertyClass

from memonster.memtypes import *
from .memtypes import *


class ClientZone(PropertyClass):
    """
    Base class for ClientZones
    """
    zone_id = MemInt64(72)
    
    zone_Name = MemCppString(88)
