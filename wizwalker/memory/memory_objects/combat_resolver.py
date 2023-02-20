from typing import List, Optional

from wizwalker.memory.memory_object import PropertyClass
from .spell_effect import SpellEffect

from memonster import LazyType
from memonster.memtypes import *
from .memtypes import *


class CombatResolver(PropertyClass):
    bool_global_effect = MemBool(112)

    global_effect = MemPointer(120, SpellEffect(0))

    battlefield_effects = MemCppVector(136, MemCppSharedPointer(0, SpellEffect(0)))
