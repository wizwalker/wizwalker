from typing import Optional

from wizwalker.memory.memory_object import PropertyClass, DynamicMemoryObject
from .behavior_template import BehaviorTemplate

from memonster.memtypes import *
from memtypes import *


class BehaviorInstance(PropertyClass):
    """
    Base class for behavior instances
    """

    # note: helper method
    def behavior_name(self) -> Optional[str]:
        template = self.behavior_template.read()
        # TODO: Better error handling
        try:
            return template.behavior_name.read()
        except:
            return None

    # note: not defined
    behavior_template = MemPointer(88, BehaviorTemplate(0))

    behavior_template_name_id = MemUInt32(104)



class DynamicBehaviorInstance(DynamicMemoryObject, BehaviorInstance):
    """
    Dynamic behavior instance that can be given an address
    """

    pass
