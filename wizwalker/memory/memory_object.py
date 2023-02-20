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
from .memory_reader import MemoryReader

from memonster import MemType


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

    async def read_wide_string(self, address: int, encoding: str = "utf-16") -> str:
        string_len = await self.read_typed(address + 16, "int")
        if string_len == 0:
            return ""

        # wide chars take 2 bytes
        string_len *= 2

        # wide strings larger than 8 bytes are pointers
        if string_len >= 8:
            string_address = await self.read_typed(address, "long long")
        else:
            string_address = address

        try:
            return (await self.read_bytes(string_address, string_len)).decode(encoding)
        except UnicodeDecodeError:
            return ""

    async def read_wide_string_from_offset(
        self, offset: int, encoding: str = "utf-16"
    ) -> str:
        base_address = await self.read_base_address()
        return await self.read_wide_string(base_address + offset, encoding)

    async def write_wide_string(
        self, address: int, string: str, encoding: str = "utf-16"
    ):
        string_len_addr = address + 16
        encoded = string.encode(encoding)
        # len(encoded) instead of string bc it can be larger in some encodings
        string_len = len(encoded)

        current_string_len = await self.read_typed(address + 16, "int")

        # we need to create a pointer to the string data
        if string_len >= 7 > current_string_len:
            # +1 for 0 byte after
            pointer_address = await self.allocate(string_len + 1)

            # need 0 byte for some c++ null termination standard
            await self.write_bytes(pointer_address, encoded + b"\x00")
            await self.write_typed(address, pointer_address, "long long")

        # string is already a pointer
        elif string_len >= 7 and current_string_len >= 8:
            pointer_address = await self.read_typed(address, "long long")
            await self.write_bytes(pointer_address, encoded + b"\x00")

        # normal buffer string
        else:
            await self.write_bytes(address, encoded + b"\x00")

        # take 2 bytes
        await self.write_typed(string_len_addr, string_len // 2, "int")

    async def write_wide_string_to_offset(
        self, offset: int, string: str, encoding: str = "utf-16"
    ):
        base_address = await self.read_base_address()
        await self.write_wide_string(base_address + offset, string, encoding)

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

class DynamicMemoryObject(MemoryObject):
    def __init__(self, hook_handler: HookHandler, base_address: int):
        super().__init__(hook_handler)

        # sanity check
        if base_address == 0:
            raise RuntimeError(
                f"Dynamic object {type(self).__name__} passed 0 base address."
            )

        self.base_address = base_address

    async def read_base_address(self) -> int:
        return self.base_address

    def __repr__(self):
        return f"<{type(self).__name__} {self.base_address=}>"


class PropertyClass(MemType):
    async def read_base_address(self) -> int:
        raise NotImplementedError()

    async def maybe_read_type_name(self) -> str:
        try:
            return await self.read_type_name()
        except (MemoryReadError, UnicodeDecodeError):
            return ""

    async def read_type_name(self) -> str:
        vtable = await self.read_value_from_offset(0, "long long")
        # first function
        get_class_name = await self.read_typed(vtable, "long long")
        # sometimes is a function with a jmp, sometimes just a body pointer
        maybe_jmp = await self.read_bytes(get_class_name, 5)
        # 233 is 0xE9 (jmp)
        if maybe_jmp[0] == 233:
            offset = struct.unpack("<i", maybe_jmp[1:])[0]
            # 5 is length of this jmp instruction
            actual_get_class_name = get_class_name + offset + 5
        else:
            actual_get_class_name = get_class_name

        # 63 is the length of the function up to the lea instruction
        lea_instruction = actual_get_class_name + 63
        # 48 8D 0D (here)
        lea_target = actual_get_class_name + 66
        rip_offset = await self.read_typed(lea_target, "int")

        # 7 is the size of this line (rip is set at the next instruction when this one is executed)
        type_name_addr = lea_instruction + rip_offset + 7

        # some of the class names can be quite long
        # i.e ClientShadowCreatureLevelTransitionCinematicAction
        return await self.read_null_terminated_string(type_name_addr, 60)
