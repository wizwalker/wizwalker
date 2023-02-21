from wizwalker.memory.memory_object import PropertyClass

from memonster.memtypes import *
from .memtypes import *


class PipCount(PropertyClass):  
    generic_pips = MemUInt8(80)
    power_pips = MemUInt8(81)
    balance_pips = MemUInt8(82)
    death_pips = MemUInt8(83)
    fire_pips = MemUInt8(84)
    ice_pips = MemUInt8(85)
    life_pips = MemUInt8(86)
    myth_pips = MemUInt8(87)
    storm_pips = MemUInt8(88)
    shadow_pips = MemUInt8(89)
