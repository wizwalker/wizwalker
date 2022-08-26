from wizwalker.memory.memory_object import MemoryObject, DynamicMemoryObject


class CamView(MemoryObject):
    # TODO: Find real name (or more fitting)
    async def read_base_address(self) -> int:
        raise NotImplementedError()    

    async def view_matrix(self) -> list[float]:
        return list(await self.read_vector(80, 9))

    async def write_view_matrix(self, values: list[float]):
        await self.write_vector(80, tuple(values), 9)


class DynamicCamView(DynamicMemoryObject, CamView):
    pass
