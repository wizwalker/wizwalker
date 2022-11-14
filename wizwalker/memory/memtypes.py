from typing import TypeVar, Type
from enum import Enum

from addon_primitives import XYZ, Orient, Rectangle
from memanagers import MemPrimitive, MemType

from wizwalker import ReadingEnumFailed


class MemInt8(MemPrimitive[int]):
    typename = "int8"

class MemUInt8(MemPrimitive[int]):
    typename = "uint8"

class MemInt16(MemPrimitive[int]):
    typename = "int16"

class MemUInt16(MemPrimitive[int]):
    typename = "uint16"

class MemInt32(MemPrimitive[int]):
    typename = "int32"

class MemUInt32(MemPrimitive[int]):
    typename = "uint32"

class MemInt64(MemPrimitive[int]):
    typename = "int64"

class MemUInt64(MemPrimitive[int]):
    typename = "uint64"


class MemFloat32(MemPrimitive[float]):
    typename = "float32"

class MemFloat64(MemPrimitive[float]):
    typename = "float64"


class MemBool(MemPrimitive[bool]):
    typename = "bool"

class MemChar(MemPrimitive[str]):
    typename = "char"


class MemPointer(MemPrimitive[int]):
    # TODO: Not yet sure if this is wanted
    typename = "pointer"

class MemXYZ(MemPrimitive[XYZ]):
    typename = "xyz"

class MemOrient(MemPrimitive[Orient]):
    typename = "orient"

class MemRect(MemPrimitive[Rectangle]):
    typename = "rect"



TET = TypeVar("TET", bound=Enum)
class MemEnum(MemType[TET]):
    def __init__(self, enum_type: Type[TET], offset) -> None:
        super().__init__(offset)
        self.enum_type = enum_type

    def read(self) -> TET:
        value = self.view.read_primitive("int32", self.offset)
        try:
            res = self.enum_type(value)
            return res
        except ValueError:
            raise ReadingEnumFailed(self.enum_type, value)

    def write(self, value: TET):
        self.view.write_primitive("int32", self.offset)


T = TypeVar("T", int, float, str, bool, XYZ, Orient, Rectangle)
class MemArray(MemType[list[T]]):
    def __init__(self, typename: str, count: int, offset) -> None:
        super().__init__(offset)
        self.typename = typename
        self.count = count

    def read(self) -> list[T]:
        return self.view.read_primitive_array(self.typename, self.count, self.offset)
    
    def write(self, value: list[T]):
        self.view.write_primitive_array(self.typename, value, self.offset)


class MemCppString(MemType[str]):
    def read(self) -> str:
        view = self.view.read_memview(20, self.offset)

        str_len = view.read_primitive("int32", 16)
        if 1 > str_len:
            return ""
        
        if str_len >= 16:
            str_ptr = view.read_memview_ptr(str_len)
        else:
            str_ptr = view.read_memview(str_len)
        
        try:
            return str_ptr.read_bytes(str_len).decode("utf-8")
        except UnicodeDecodeError:
            return ""

    def write(self, value: str):
        view = self.view.read_memview(20, self.offset)

        encoded = value.encode("utf-8")
        cur_str_len = view.read_primitive("int32", 16)
        new_str_len = len(encoded)

        # needs alloc
        if new_str_len >= 15 > cur_str_len:
            # +1 for null
            str_ptr = view.backend._allocator.alloc(new_str_len + 1)
            str_ptr.write_bytes(encoded + b"\x00")
            view.write_addr(str_ptr)
        elif new_str_len >= 15 and cur_str_len >= 15:
            # TODO: This is definitely not right. But copying from original for now
            str_ptr = view.read_memview(len(encoded) + 1)
            str_ptr.write_bytes(encoded + "\x00")
        else:
            view.write_bytes(encoded + b"\x00")
        
        view.write_primitive("int32", new_str_len, 16)
