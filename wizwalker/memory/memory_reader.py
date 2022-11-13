import struct
from typing import Any

import pefile
import pymem
import pymem.exception
import pymem.process
import pymem.ressources.structure

from wizwalker import (
    AddressOutOfRange,
    ClientClosedError,
    MemoryReadError,
    MemoryWriteError,
    utils,
)


class MemoryReader:
    """
    Represents anything that needs to read/write from/to memory
    """

    def __init__(self, process: pymem.Pymem):
        self.process = process

        self._symbol_table = {}



