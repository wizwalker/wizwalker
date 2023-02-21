from wizwalker.memory.memory_object import PropertyClass

from memonster.memtypes import *
from .memtypes import *


class PlayDeck(PropertyClass):
    def __init__(self, offset: int) -> None:
        super().__init__(offset)

        self.deck_to_save = MemCppVector(72, MemCppSharedPointer(0, PlaySpellData(0)))
        self.graveyard_to_save = MemCppVector(96, MemCppSharedPointer(0, PlaySpellData(0)))

class PlaySpellData(PropertyClass):
    template_id = MemUInt32(72)
    enchantment = MemUInt32(76)
