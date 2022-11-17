import struct
from enum import Enum
from typing import Any, List, Type

from wizwalker.errors import (
    AddressOutOfRange,
    MemoryReadError,
    ReadingEnumFailed,
    PatternFailed,
    PatternMultipleResults
)
from .memonster.addon_primitives import XYZ, Orient
from . import memanagers, memutils
from .handler import HookHandler


MAX_STRING = 5_000


# TODO: add .find_instances that find instances of whichever class used it
class MemoryObject:
    """
    Class for any represented classes from memory
    """

    def __init__(self, raw: memanagers.MemoryView, allocator: memanagers.ProcessAllocator):
        self.allocator = allocator
        self.raw = raw

        self._offset_lookup_cache = {}

    async def pattern_scan_offset(
            self,
            pattern: bytes,
            instruction_length: int,
            static_backup: int = None,
    ) -> int:
        try:
            ptr = await memutils.pattern_scan(
                self.allocator.process_handle,
                pattern,
                instruction_length + 4,
                module="WizardGraphicalClient.exe"
            )
            return ptr.read_primitive(instruction_length, "uint32")
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

    async def read_null_terminated_string(
        self, address: int, max_size: int = 20, encoding: str = "utf-8"
    ):
        search_bytes = await self.read_bytes(address, max_size)
        string_end = search_bytes.find(b"\x00")

        if string_end == 0:
            return ""
        elif string_end == -1:
            raise MemoryReadError(f"Couldn't read string at {address}; no end byte.")

        # Don't include the 0 byte
        string_bytes = search_bytes[:string_end]
        return string_bytes.decode(encoding)

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

class PropertyClass(memanagers.MemType):
    async def maybe_read_type_name(self) -> str:
        try:
            return await self.read_type_name()
        except (MemoryReadError, UnicodeDecodeError):
            return ""

    async def read_type_name(self) -> str:
        vtable = self.read_memview(8)
        # first function
        get_class_name = vtable.read_memview(5)
        # sometimes is a function with a jmp, sometimes just a body pointer
        maybe_jmp = get_class_name.read_bytes(5)
        # 233 is 0xE9 (jmp)
        if maybe_jmp[0] == 233:
            offset = struct.unpack("<i", maybe_jmp[1:])[0]
            # 5 is length of this jmp instruction
            actual_get_class_name = get_class_name.backend.address() + offset + 5
        else:
            actual_get_class_name = get_class_name.backend.address()

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
