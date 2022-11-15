from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memtypes import *


class CharacterRegistry(PropertyClass):
    @staticmethod
    def obj_size() -> int:
        # unverified
        return 340
    
    # async def displayed_tips(self) -> List[int]:
    #     sub_object_addrs = await self.read_linked_list(112)
    #
    #     res = []
    #     for sub_object in sub_object_addrs:
    #         res.append(await self.read_typed(sub_object, "unsigned long long"))
    #
    #     return res

    # todo add the useless properties

    active_quest_id = MemUInt64(304)
    active_goal_id = MemUInt32(336)
