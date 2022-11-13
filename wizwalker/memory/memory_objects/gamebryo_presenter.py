from wizwalker.memory.memory_object import MemoryObject
from wizwalker.memory.memory_objects.scene_manager import DynamicSceneManager


class GamebryoPresenter(MemoryObject):
    async def read_base_address(self) -> int:
        raise NotImplementedError()

    async def default_background_color_red(self) -> int:
        return await self.read_value_from_offset(0x48, "int")

    async def write_default_background_color_red(self, red: int):
        await self.write_value_to_offset(0x48, red, "int")

    async def default_background_color_green(self) -> int:
        return await self.read_value_from_offset(0x4C, "int")

    async def write_default_background_color_green(self, green: int):
        await self.write_value_to_offset(0x4C, green, "int")

    async def default_background_color_blue(self) -> int:
        return await self.read_value_from_offset(0x50, "int")

    async def write_default_background_color_blue(self, blue: int):
        await self.write_value_to_offset(0x50, blue, "int")

    async def scene_manager(self) -> DynamicSceneManager:
        addr = await self.read_value_from_offset(0x68, "unsigned long long")

        if addr == 0:
            return None

        return DynamicSceneManager(self.hook_handler, addr)

    async def shadow_detail(self) -> int:
        return await self.read_value_from_offset(0x8C, "int")

    async def write_shadow_detail(self, value: int):
        await self.write_value_to_offset(0x8C, value, "int")

    async def master_scene_root(self) -> int:
        """
        Only defined for later
        """
        return await self.read_value_from_offset(0x90, "unsigned long long")

    async def master_collision_scene(self) -> int:
        """
        Only defined for later
        """
        return await self.read_value_from_offset(0xA8, "unsigned long long")

    async def nametag_flags(self) -> int:
        return await self.read_value_from_offset(0x190, "int")

    async def write_nametag_flags(self, flags: int):
        await self.write_value_to_offset(0x190, flags, "int")
