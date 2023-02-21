import struct
from enum import Enum
from typing import Any, List, Type

from wizwalker.constants import type_format_dict
from wizwalker.errors import (
    AddressOutOfRange,
    MemoryReadError,
    ReadingEnumFailed,
    PatternFailed,
    PatternMultipleResults
)
from wizwalker.utils import XYZ, Orient
from .handler import HookHandler

from memonster import LazyType
from memonster.memtypes import *
from wizwalker.memory.memory_objects.memtypes import *


MAX_STRING = 5_000


# TODO: add .find_instances that find instances of whichever class used it
class MemoryObject(MemoryReader):
    """
    Class for any represented classes from memory
    """

    def __init__(self, hook_handler: HookHandler):
        super().__init__(hook_handler.process)
        self.hook_handler = hook_handler

        self._offset_lookup_cache = {}

    async def read_base_address(self) -> int:
        raise NotImplementedError()

    async def read_value_from_offset(self, offset: int, data_type: str) -> Any:
        base_address = await self.read_base_address()
        return await self.read_typed(base_address + offset, data_type)

    async def write_value_to_offset(self, offset: int, value: Any, data_type: str):
        base_address = await self.read_base_address()
        await self.write_typed(base_address + offset, value, data_type)

    async def pattern_scan_offset(
            self,
            pattern: bytes,
            instruction_length: int,
            static_backup: int = None,
    ) -> int:
        try:
            addr = await self.pattern_scan(pattern, module="WizardGraphicalClient.exe")
            return await self.read_typed(addr + instruction_length, "unsigned int")
        except (PatternFailed, PatternMultipleResults) as exc:
            if static_backup is not None:
                return static_backup

            raise exc

    async def pattern_scan_offset_cached(
            self,
            pattern: bytes,
            instruction_length: int,
            name: str,
            static_backup: int = None
    ):
        try:
            return self._offset_lookup_cache[name]
        except KeyError:
            offset = await self.pattern_scan_offset(pattern, instruction_length, static_backup)
            self._offset_lookup_cache[name] = offset
            return offset

    async def read_inlined_vector(
            self,
            offset: int,
            object_size: int,
            object_type: type,
    ):
        start = await self.read_value_from_offset(offset, "unsigned long long")
        end = await self.read_value_from_offset(offset + 16, "unsigned long long")

        total_size = (end - start) // object_size

        current_addr = start

        res = []
        for _ in total_size:
            res.append(object_type(self.hook_handler, current_addr))
            current_addr += object_size

        return res


class PropertyClass(MemType):
    def maybe_read_type_name(self) -> str:
        # TODO: Better error handling
        try:
            return self.read_type_name()
        except:
            return ""

    # TODO: Check if monster impl works
    def read_type_name(self) -> str:
        vtable = self.cast_offset(0, MemPointer(0, MemPointer(0, MemUInt64(0)))).read()
        # first function
        get_class_name = vtable.read()
        # sometimes is a function with a jmp, sometimes just a body pointer
        maybe_jmp = get_class_name.read_bytes(5)
        # 233 is 0xE9 (jmp)
        if maybe_jmp[0] == 233:
            offset: int = struct.unpack("<i", maybe_jmp[1:])[0]
            # 5 is length of this jmp instruction
            actual_get_class_name = get_class_name.read() + offset + 5
        else:
            actual_get_class_name = get_class_name.read()

        # 63 is the length of the function up to the lea instruction
        lea_instruction = actual_get_class_name + 63
        # 48 8D 0D (here)
        lea_target = actual_get_class_name + 66
        rip_offset = self.cast_address(lea_target, MemInt32(0)).read()

        # 7 is the size of this line (rip is set at the next instruction when this one is executed)
        type_name_addr = lea_instruction + rip_offset + 7

        # some of the class names can be quite long
        # i.e ClientShadowCreatureLevelTransitionCinematicAction
        return self.cast_address(type_name_addr, MemCString(0, 60))
