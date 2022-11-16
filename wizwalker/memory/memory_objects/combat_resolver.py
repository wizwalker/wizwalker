from typing import List, Optional

from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memonster.memtypes import *
from wizwalker.memory.memonster import memclass
from .spell_effect import SpellEffect


@memclass
class CombatResolver(PropertyClass):
    def fieldsize(self) -> int:
        # unverified
        return 144

    bool_global_effect = MemBool(112)

    global_effect = MemPointer[SpellEffect](120, SpellEffect)

    battlefield_effects = MemPointer[SpellEffect](136, SpellEffect)
