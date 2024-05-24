from wizwalker.memory.memory_object import DynamicMemoryObject
from .fish import Fish


class FishingManager(DynamicMemoryObject):
    async def fish_list(self) -> list[Fish]:
        res = []
        for fish_addr in await self.read_shared_linked_list(0x1C0):
            res.append(Fish(self.hook_handler, fish_addr))
        return res
