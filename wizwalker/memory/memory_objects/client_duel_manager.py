from wizwalker.memory.memory_object import PropertyClass
from .duel import DynamicDuel


class ClientDuelManager(PropertyClass):
    @staticmethod
    def obj_size() -> int:
        # unverified
        return 24

    # TODO: Make work
    # async def duelmap(self) -> dict[int, DynamicDuel]:
    #     return await self.read_std_map(8, DynamicDuel)
