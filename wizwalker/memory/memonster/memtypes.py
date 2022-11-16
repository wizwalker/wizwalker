from typing import TypeVar, Type
from enum import Enum

from .addon_primitives import XYZ, Orient, Rectangle
from .memanagers import MemPrimitive, MemType, MemPointer, memclass, ParamType

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

    # In case you just want one of them
    x = MemFloat32(0)
    y = MemFloat32(4)
    z = MemFloat32(8)

    def read(self) -> XYZ:
        view = self.fieldview()
        return XYZ(*view.read_typestring("<fff"))

    def write(self, value: XYZ):
        view = self.fieldview()
        view.write_typestring("<fff", value)


@memclass
class MemOrient(MemType[Orient]):
    def fieldsize(self) -> int:
        return 12

    pitch = MemFloat32(0)
    roll = MemFloat32(4)
    yaw = MemFloat32(8)

    def read(self) -> Orient:
        view = self.fieldview()
        return Orient(*view.read_typestring("<fff"))

    def write(self, value: Orient):
        view = self.fieldview()
        view.write_typestring("<fff", value)


@memclass
class MemRect(MemType[Rectangle]):
    def fieldsize(self) -> int:
        return 16

    x1 = MemInt32(0)
    y1 = MemInt32(4)
    x2 = MemInt32(8)
    y2 = MemInt32(12)

    def read(self) -> Orient:
        view = self.fieldview()
        return Orient(*view.read_typestring("<iiii"))

    def write(self, value: Orient):
        view = self.fieldview()
        view.write_typestring("<iiii", value)



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
# Arrays are just spicy pointers
@memclass
class MemArray(MemPointer[list[T]]):
    count: ParamType | int

    def get_dummy_inst(self):
        return type(self)(0, self._dummy, self.count)

    def __len__(self) -> int:
        return self.count

    def fieldsize(self) -> int:
        # might be kinda heavy
        return self._dummy.get_dummy_inst().fieldsize() * self.count

    # Am not yet 100% convinced I want this
    def __getitem__(self, i: int) -> T:
        view = self.fieldview()
        inst: MemType = self._dummy.get_dummy_inst()
        dummysize = inst.fieldsize()
        inst.load_view(view.subview(dummysize, i * dummysize))
        return inst

    # Even less convinced on this
    def __setitem__(self, i: int, val: MemType):
        view = self.fieldview()
        inst: MemType = self._dummy.get_dummy_inst()
        if dummysize == None:
            dummysize = inst.fieldsize()
        inst.load_view(view.subview(dummysize, i * dummysize))
        if isinstance(T, MemPointer):
            inst.write(val._view.backend.address())
        else:
            inst.write(val.read())

    def read(self) -> list[T]:
        result = []

        for i in range(self.count):
            result.append(self[i])

        return result
    
    def write(self, value: list[T]):
        for i in range(self.count):
            self[i] = value[i]


# TODO: Implement
class MemCppVector(MemPointer[list[T]]):
    _dummy: ParamType | Type[T]


@memclass
class MemCppString(MemType[str]):
    def fieldsize(self) -> int:
        return 32

    data_ptr = MemPointer(0, MemBytes(0, -1))
    data_sso = MemBytes(0, 16)
    length = MemInt32(16)

    def __len__(self) -> int:
        return self.length.read()

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
