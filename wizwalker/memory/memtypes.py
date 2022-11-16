from typing import TypeVar, Type, Any
from enum import Enum

from addon_primitives import XYZ, Orient, Rectangle
from memanagers import MemPrimitive, MemType, MemPointer, type_dict, memclass, ParamType

from wizwalker import ReadingEnumFailed

@memclass
class MemInt8(MemPrimitive[int]):
    typename = "int8"

@memclass
class MemUInt8(MemPrimitive[int]):
    typename = "uint8"

@memclass
class MemInt16(MemPrimitive[int]):
    typename = "int16"

@memclass
class MemUInt16(MemPrimitive[int]):
    typename = "uint16"

@memclass
class MemInt32(MemPrimitive[int]):
    typename = "int32"

@memclass
class MemUInt32(MemPrimitive[int]):
    typename = "uint32"

@memclass
class MemInt64(MemPrimitive[int]):
    typename = "int64"

@memclass
class MemUInt64(MemPrimitive[int]):
    typename = "uint64"

@memclass
class MemFloat32(MemPrimitive[float]):
    typename = "float32"

@memclass
class MemFloat64(MemPrimitive[float]):
    typename = "float64"


@memclass
class MemBool(MemPrimitive[bool]):
    typename = "bool"

@memclass
class MemChar(MemPrimitive[str]):
    typename = "char"


@memclass
class MemXYZ(MemType[XYZ]):
    def fieldsize(self) -> int:
        return 12

    def read(self) -> XYZ:
        view = self.fieldview()
        return XYZ(*view.read_typestring("<fff"))

    def write(self, value: XYZ):
        view = self.fieldview()
        view.write_typestring("<fff", value)

    # In case you just want one of them
    x = MemFloat32(0)
    y = MemFloat32(4)
    z = MemFloat32(8)

# class MemOrient(MemPrimitive[Orient]):
#     typename = "orient"

# class MemRect(MemPrimitive[Rectangle]):
#     typename = "rect"


@memclass
class MemBytes(MemType[bytes]):
    size: ParamType | int

    def get_dummy_inst(self) -> "MemBytes":
        return type(self)(0, self.size)

    def fieldsize(self) -> int:
        return self.size

    def read(self) -> bytes:
        return self.fieldview().read_bytes(self.fieldsize())

    def write(self, data: bytes) -> bytes:
        self.fieldview().write_bytes(data)


TET = TypeVar("TET", bound=Enum)
@memclass
class MemEnum(MemType[TET]):
    enum_type: ParamType | Type[TET]

    def get_dummy_inst(self) -> "MemEnum":
        return type(self)(0, self.enum_type)

    def fieldsize(self) -> int:
        return 4

    def read(self) -> TET:
        view = self.fieldview()
        value = view.read_primitive("int32")
        try:
            res = self.enum_type(value)
            return res
        except ValueError:
            raise ReadingEnumFailed(self.enum_type, value)

    def write(self, value: TET) -> None:
        view = self.fieldview()
        view.write_primitive("int32", int(value))


T = TypeVar("T", bound=MemType)
@memclass
class MemArray(MemType[list[T]]):
    mtype: ParamType | Type[T]
    count: ParamType | int

    def get_dummy_inst(self):
        return type(self)(0, self.mtype, self.count)

    def __len__(self) -> int:
        return self.count

    def fieldsize(self) -> int:
        return type_dict["pointer"].size

    def read(self) -> list[T]:
        raise NotImplementedError()
        view = self.fieldview()
        arr_view = view.read_memview_ptr(len(self) * self.fieldsize())
        arr_view.read_primitive_array(self.typename, self.count)
        result = []
        for off in range(0, len(self) * self.fieldsize(), self.fieldsize()):
            result.append(self.mtype())
        return result
    
    def write(self, value: list[T]):
        raise NotImplementedError()
        view = self.fieldview()
        arr_view = view.read_memview_ptr(len(self) * self.fieldsize())
        arr_view.write_primitive_array(self.typename, value)


# TODO: Implement on MemType only
# PVT = TypeVar("PVT", int, MemoryView)
# class MemCppPtrVector(MemType[list[PVT]]):
#     def __init__(self, oftype: Type[PVT], offset: int) -> None:
#         super().__init__(offset)
#         self.oftype = oftype

#     def _memsize(self) -> int:
#         view_start = self.view.read_primitive("pointer", self.offset)
#         view_end = self.view.read_primitive("pointer", self.offset + 8)
#         return view_end - view_start

#     def __len__(self) -> int:
#         type_size = type_dict["pointer"].size
#         return self._memsize() // type_size

#     def fieldsize(self) -> int:
#         return type_dict["pointer"].size * 2

#     def read(self) -> list[PVT]:
#         view_size = self._memsize()
#         if view_size == 0:
#             return []
#         view_start = self.view.read_primitive("pointer", self.offset)
#         vec_view = self.view.read_memview(view_size, view_start)

#         type_size = type_dict["pointer"].size
#         result = []
#         for off in range(0, view_size, type_size):
#             if isinstance(Type(self.oftype), MemoryView):
#                 result.append(vec_view.read_typeview_ptr(Type(self.oftype), off))
#             else:
#                 result.append(vec_view.read_primitive("pointer", off))
#         return result

#     def write(self, value: list[PVT]) -> None:
#         raise NotImplementedError()

# VVT = TypeVar("VVT", MemType)
# class MemCppValVector(MemType[T]):
#     def __init__(self, oftype: T, offset: int) -> None:
#         super().__init__(offset)
#         self.oftype = oftype

#     def _memsize(self) -> int:
#         view = self.fieldview()
#         view_start = view.read_primitive("pointer")
#         view_end = view.read_primitive("pointer", 8)
#         return view_end - view_start

#     def __len__(self) -> int:
#         type_size = type_dict["pointer"].size
#         return self._memsize() // type_size

#     def fieldsize(self) -> int:
#         return type_dict["pointer"] * 2

#     def read(self) -> list[PVT]:
#         view_size = self._memsize()
#         if view_size == 0:
#             return []
#         view = self.fieldview()
#         vec_view = view.read_memview_ptr(view_size)

#         type_size = type_dict["pointer"].size
#         result = []
#         for off in range(0, view_size, type_size):
#             if isinstance(Type(self.oftype), MemoryView):
#                 result.append(vec_view.read_typeview_ptr(Type(self.oftype), off))
#             else:
#                 result.append(vec_view.read_primitive("pointer", off))
#         return result

#     def write(self, value: list[PVT]) -> None:
#         raise NotImplementedError()

@memclass
class MemCppString(MemType[str]):
    def __len__(self) -> int:
        return self.length.read()

    def fieldsize(self) -> int:
        return 32

    data_ptr = MemPointer(0, MemBytes(0, -1))
    data_sso = MemBytes(0, 16)
    length = MemInt32(16)

    def read(self) -> str:
        str_len = len(self)
        if 1 > str_len:
            return ""
        
        if str_len >= 16:
            self.data_ptr._dummy.size = str_len
            str_ptr = self.data_sso.fieldview().ptr_view(str_len)
        else:
            str_ptr = self.fieldview().subview(str_len)
        
        try:
            return str_ptr.read_bytes(str_len).decode("utf-8")
        except UnicodeDecodeError:
            return ""

    def write(self, value: str) -> None:
        encoded = value.encode("utf-8")
        cur_str_len = len(self)
        new_str_len = len(encoded)

        # needs alloc
        if new_str_len >= 15 > cur_str_len:
            # +1 for 
            self.data_ptr.alloc_dummy(MemBytes(self.data_ptr._offset, new_str_len + 1))
            self.data_ptr.read().write(encoded + b"\x00")
        elif new_str_len >= 15 and cur_str_len >= 15:
            # TODO: This is definitely not right. But implementing from original for now
            self.data_ptr.read().write(encoded + "\x00")
        else:
            self.data_sso.write(encoded + b"\x00")
        
        self.length.write(new_str_len)
