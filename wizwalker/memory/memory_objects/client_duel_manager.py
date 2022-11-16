from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memonster import memclass
from .duel import Duel


@memclass
class ClientDuelManager(PropertyClass):
    def fieldsize(self) -> int:
        # unverified
        return 24

    # TODO: Make work
    # async def duelmap(self) -> dict[int, DynamicDuel]:
    #     return await self.read_std_map(8, DynamicDuel)
