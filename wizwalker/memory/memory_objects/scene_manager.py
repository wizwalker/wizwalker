from wizwalker.memory.memory_object import MemoryObject
from .enums import FogMode

class SceneManager(MemoryObject):
    async def read_base_address(self) -> int:
        raise NotImplementedError()

    # 0x60 has skybox list (0x68 end)

    # These fog settings are technically inlined
    async def fog_mode(self) -> FogMode:
        return await self.read_enum(0x180, FogMode)

    async def write_fog_mode(self, mode: FogMode):
        await self.write_enum(0x180, mode)

    async def fog_density(self) -> float:
        """
        This slowly approaches fog_density_target, but it's responsible for the density of filter/fog
        """
        return await self.read_value_from_offset(0x184, "float")

    async def write_fog_density(self, density: float):
        await self.write_value_to_offset(0x184, density, "float")

    async def fog_density_target(self) -> float:
        """
        A value for fog_density to approach
        """
        return await self.read_value_from_offset(0x188, "float")

    async def write_fog_density_target(self, target: float):
        await self.write_value_to_offset(0x188, target, "float")

    async def fog_start_density(self) -> float:
        """
        The value at which fog density begins. In filter mode this is gonna be the main thing you need
        """
        return await self.read_value_from_offset(0x18C, "float")

    async def write_fog_start_density(self, start: float):
        await self.write_value_to_offset(0x18C, start, "float")

    async def fog_color_red(self) -> float:
        return await self.read_value_from_offset(0x190, "float")

    async def write_fog_color_red(self, red: float):
        await self.write_value_to_offset(0x190, red, "float")

    async def fog_color_green(self) -> float:
        return await self.read_value_from_offset(0x194, "float")

    async def write_fog_color_green(self, green: float):
        await self.write_value_to_offset(0x194, green, "float")

    async def fog_color_blue(self) -> float:
        return await self.read_value_from_offset(0x198, "float")

    async def write_fog_color_blue(self, blue: float):
        await self.write_value_to_offset(0x198, blue, "float")
