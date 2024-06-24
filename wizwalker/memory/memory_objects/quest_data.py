from .goal_data import GoalData
from wizwalker.memory.memory_object import Primitive, DynamicMemoryObject


class QuestData(DynamicMemoryObject):
    async def name_lang_key(self) -> str:
        return await self.read_string_from_offset(112)

    async def goal_data(self) -> dict[int, GoalData]:
        return await self.read_std_map(176, GoalData)
