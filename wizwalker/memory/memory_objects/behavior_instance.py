from typing import Optional

from wizwalker.memory import memanagers
from wizwalker.memory.memonster.memtypes import *
from wizwalker.memory.memory_object import PropertyClass
from .behavior_template import BehaviorTemplate


class BehaviorInstance(memanagers.MemoryView):
    """
    Base class for behavior instances
    """
    @staticmethod
    def obj_size() -> int:
        # unverified
        return 108

    behavior_template_name_id = MemUInt32(104)

    # TODO: Make work
    # # note: helper method
    # async def behavior_name(self) -> Optional[str]:
    #     template = await self.behavior_template()

    #     if template is None:
    #         return None

    #     return await template.behavior_name()

    # # note: not defined
    # async def behavior_template(self) -> Optional[BehaviorTemplate]:
    #     addr = await self.read_primitive("pointer", 0x58)

    #     if addr == 0:
    #         return None

    #     return BehaviorTemplate(self.hook_handler, addr)
