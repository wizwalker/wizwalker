from wizwalker.memory.memory_object import DynamicMemoryObject
from .actor_body import DynamicActorBody
from .fish_template import FishTemplate


class Fish(DynamicMemoryObject):
    async def body(self) -> DynamicActorBody:
        addr = await self.read_value_from_offset(0x48, "unsigned long long")
        return DynamicActorBody(self.hook_handler, addr)

    async def template(self) -> FishTemplate:
        addr = await self.read_value_from_offset(0xD8, "unsigned long long")
        return FishTemplate(self.hook_handler, addr)

    async def fish_id(self) -> int:
        return await self.read_value_from_offset(0xE4, "int")

    async def template_id(self) -> int:
        return await self.read_value_from_offset(0xE8, "int")

    async def size(self) -> float:
        return await self.read_value_from_offset(0xEC, "float")

    async def is_chest(self) -> bool:
        return await self.read_value_from_offset(0xF0, "bool")
