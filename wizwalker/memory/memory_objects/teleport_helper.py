from wizwalker.utils import XYZ
from wizwalker.memory.memory_object import MemoryObject


class TeleportHelper(MemoryObject):
    def __init__(self, hook_handler):
        super().__init__(hook_handler._allocator)
        self.hook_handler = hook_handler

    def address(self) -> int:
        return self.hook_handler.read_teleport_helper()

    def size(self) -> int:
        return 13

    async def position(self) -> XYZ:
        return await self.read_xyz(0)

    async def write_position(self, xyz: XYZ):
        await self.write_xyz(0, xyz)

    async def should_update(self) -> bool:
        return self.raw.read_primitive("bool", 12)

    async def write_should_update(self, should_update: bool = True):
        self.raw.write_primitive("bool", should_update, 12)

    async def target_object_address(self) -> int:
        return self.raw.read_primitive("pointer", 13)

    async def write_target_object_address(self, target_object_address: int):
        self.raw.write_primitive("pointer", target_object_address, 13)
