from .madlib_block import MadlibBlock
from wizwalker.memory.memory_object import Primitive, DynamicMemoryObject

class GoalData(DynamicMemoryObject):
    async def name_lang_key(self) -> str:
        return await self.read_string_from_offset(0x50)

    async def madlib_block(self) -> MadlibBlock:
        return MadlibBlock(self.hook_handler, await self.read_value_from_offset(0xC0, Primitive.uint64))
