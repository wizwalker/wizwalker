from typing import List, Optional

from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memtypes import *
from .spell_effect import SpellEffect


class CombatResolver(PropertyClass):
    @staticmethod
    def obj_size() -> int:
        # unverified
        return 144

    bool_global_effect = MemBool(112)

    # TODO: Make work
    # async def global_effect(self) -> Optional[DynamicSpellEffect]:
    #     addr = await self.read_value_from_offset(120, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicSpellEffect(self.hook_handler, addr)

    # async def battlefield_effects(self) -> List[DynamicSpellEffect]:
    #     effects = []
    #     for addr in await self.read_shared_vector(136):
    #         effects.append(DynamicSpellEffect(self.hook_handler, addr))

    #     return effects
