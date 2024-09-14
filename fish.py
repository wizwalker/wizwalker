from enum import Enum

from wizwalker.memory.memory_object import DynamicMemoryObject
from .actor_body import DynamicActorBody
from .fish_template import FishTemplate


class FishStatusCode(Enum): # note that if multiple fish bite the lure you will be given two status codes at the same time (from the status_code function), resulting in numbers such as "26"
    neutral = 0
    scared = 1
    biting = 2
    escaping = 3 # works on sentinels
    escaped = 4 # works on sentinels
    hooked = 5
    unknown6 = 6 # only been seen when multiple fish bit the lure, possibly a different state of escaped specifically for this case


class Fish(DynamicMemoryObject):
    async def body(self) -> DynamicActorBody:
        addr = await self.read_value_from_offset(0x48, "unsigned long long")
        return DynamicActorBody(self.hook_handler, addr)

    async def status_code(self) -> FishStatusCode:
        return await self.read_enum(0xB8, FishStatusCode)

    async def write_status_code(self, val: FishStatusCode):
        await self.write_enum(0xB8, val)

    async def template(self) -> FishTemplate:
        addr = await self.read_value_from_offset(0xD8, "unsigned long long")
        return FishTemplate(self.hook_handler, addr)

    async def bobber_submerge_ease(self) -> float:
        return await self.read_value_from_offset(0xE0, "float")

    async def write_bobber_submerge_ease(self, val: float):
        ## At 1.0 the bobber is guaranteed to go down
        await self.write_value_to_offset(0xE0, val, "float")

    async def fish_id(self) -> int:
        return await self.read_value_from_offset(0xE4, "int")

    async def template_id(self) -> int:
        return await self.read_value_from_offset(0xE8, "int")

    async def size(self) -> float:
        return await self.read_value_from_offset(0xEC, "float")

    async def is_chest(self) -> bool:
        return await self.read_value_from_offset(0xF0, "bool")
