from wizwalker.memory.memory_object import PropertyClass
from .duel import Duel

from memonster.memtypes import *
from memtypes import *


class ClientDuelManager(PropertyClass):
    duelmap = MemCppMap(8, Duel(0))
