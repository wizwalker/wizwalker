from typing import Optional

from wizwalker.memory.memonster.memtypes import *
from wizwalker.memory.memonster import memclass
from wizwalker.memory.memory_object import PropertyClass
from .behavior_template import BehaviorTemplate


@memclass
class BehaviorInstance(PropertyClass):
    """
    Base class for behavior instances
    """
    def fieldsize(self) -> int:
        # unverified
        return 108

    behavior_template_name_id = MemUInt32(104)

    # note: helper method
    def behavior_name(self) -> Optional[str]:
        template = self.behavior_template.read()
        if template.isnull():
            return None
        return template.behavior_name.read()

    behavior_template = MemPointer[BehaviorTemplate](0x58, BehaviorTemplate)
