from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memonster import memclass
from wizwalker.memory.memonster.memtypes import *
from .duel import Duel


@memclass
class ClientDuelManager(PropertyClass):
    def fieldsize(self) -> int:
        # unverified
        return 24

    duelmap = MemCppTree(8, Duel)
