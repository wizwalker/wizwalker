from wizwalker.memory.memory_object import MemoryObject, DynamicMemoryObject

class QuestData(DynamicMemoryObject):
    async def name_lang_key(self) -> str:
        return await self.read_string_from_offset(0x70)
