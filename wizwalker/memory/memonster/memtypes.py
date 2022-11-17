from typing import TypeVar, Type
from enum import Enum

from .addon_primitives import XYZ, Orient, Rectangle
from .memanagers import MemPrimitive, MemType, MemPointer, memclass, ParamType, LazyDummy
from wizwalker.memory.memutils import is_power_of_two

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

    def get_lazy_dummy_args(self) -> tuple:
        return super().get_lazy_dummy_args() + (self.size,)

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
    enum_size: ParamType | int = 4

    def __post_init__(self):
        if self.enum_size < 1 or self.enum_size > 8 or not is_power_of_two(self.enum_size):
            raise ValueError()
        return super().__post_init__()

    def get_lazy_dummy_args(self) -> tuple:
        return super().get_lazy_dummy_args() + (self.enum_type, self.enum_size)

    def fieldsize(self) -> int:
        return self.enum_size

    def read(self) -> TET:
        view = self.fieldview()
        value = view.read_primitive(f"uint{self.enum_size * 8}")
        try:
            res = self.enum_type(value)
            return res
        except ValueError:
            raise ReadingEnumFailed(self.enum_type, value)

    def write(self, value: TET) -> None:
        view = self.fieldview()
        view.write_primitive(f"uint{self.enum_size * 8}", int(value))


@memclass
class MemCString(MemType[str]):
    max_size: ParamType | int

    def get_lazy_dummy_args(self) -> tuple:
        return super().get_lazy_dummy_args() + (self.max_size,)

    def fieldsize(self) -> int:
        return self.max_size

    def read(self) -> str:
        view = self.fieldview()
        data = view.read_bytes(self.max_size)
        end = data.find(b"\x00")
        if end == 0:
            return ""
        if end < 0:
            raise ValueError()
        return data[:end].decode("utf-8")

    def write(self, value: str):
        data = value.encode("utf-8")
        if len(data) == 0:
            return
        view = self.fieldview()
        view.write_bytes(data)


T = TypeVar("T", bound=MemType)



class _MemCppLinkedListNode(MemType):
    pass
@memclass(typemap={"_MemCppLinkedListNode": "MemCppLinkedListNode"})
class MemCppLinkedListNode(MemPointer[T]):
    next: MemPointer(0, _MemCppLinkedListNode)
    prev: MemPointer(8, _MemCppLinkedListNode)

    def fieldsize(self) -> int:
        inst = self._lazy_dummy.instantiate()
        return 24 + inst.fieldsize()

    def read(self) -> T:
        view = self.fieldview()
        inst = self._lazy_dummy.instantiate()
        instview = view.subview(inst.fieldsize(), 16)
        inst.load_view(instview)
        return inst

    def write(self):
        raise NotImplementedError()

@memclass
class MemCppLinkedList(MemPointer[T]):
    def fieldsize(self) -> int:
        return 12

    list_head = MemPointer(0, MemCppLinkedListNode[T])
    list_size = MemInt32(8)

    def __post_init__(self):
        self.list_head.load_dummy(self._lazy_dummy)
        return super().__post_init__()

    def read(self) -> list[T]:
        result = []
        if self.list_size.read() == 0:
            return result

        cur_node = self.list_head.read()
        for _ in range(self.list_size.read()):
            result.append(cur_node.val)
            cur_node = cur_node.next.read()

        return result

    def write(self, value: int):
        raise NotImplementedError()


class MemCppTreeNodeColor(Enum):
    Red = 0
    Black = 1

class _MemCppTreeNode(MemType):
    pass

@memclass(typemap={"_MemCppTreeNode": "MemCppTreeNode"})
class MemCppTreeNode(MemPointer[T]):
    left = MemPointer(0x0, _MemCppTreeNode)
    parent = MemPointer(0x8, _MemCppTreeNode)
    right = MemPointer(0x10, _MemCppTreeNode)
    color = MemEnum(0x19, MemCppTreeNodeColor, 1)
    is_nil = MemBool(0x1A)
    key = MemUInt64(0x20)
    valptr = MemPointer(0x28, T)
    
    def fieldsize(self) -> int:
        return 0x30

    def __post_init__(self):
        self.left.load_dummy(self._lazy_dummy)
        self.parent.load_dummy(self._lazy_dummy)
        self.right.load_dummy(self._lazy_dummy)
        self.valptr.load_dummy(self._lazy_dummy)
        return super().__post_init__()

    def read(self) -> T:
        return self.valptr.read()

    def read_tree(self) -> dict:
        result = {}
        if self.color.read() == MemCppTreeNodeColor.Red:
            result[self.key.read()] = self.valptr.read()

            left_node: MemCppTreeNode = self.left.read()
            if not left_node.isnull():
                result = result | left_node.read_tree()

            right_node: MemCppTreeNode = self.right.read()
            if not right_node.isnull():
                result = result | right_node.read_tree()

        return result

    def write(self, value: int):
        raise NotImplementedError()

# TODO: Is this type correct/needed???
@memclass
class MemCppTree(MemPointer[T]):
    root_node = MemPointer(MemCppTreeNode(0, T))

    def __post_init__(self):
        self.root_node.load_dummy(self._lazy_dummy)
        return super().__post_init__()

    def fieldsize(self) -> int:
        # TODO: Verify
        return super().fieldsize(0x8)

    def read(self) -> dict:
        root: MemCppTreeNode = self.root_node.read()
        first = root.parent
        if first._view.backend.address() == root._view.backend.address():
            return {}
        return root.read_tree()

    def write(self, value: int):
        raise NotImplementedError()


# Arrays are just spicy pointers
@memclass
class MemArray(MemPointer[T]):
    count: ParamType | int

    def get_lazy_dummy_args(self) -> tuple:
        return super().get_lazy_dummy_args() + (self.count,)

    def fieldsize(self) -> int:
        inst: MemType = self._lazy_dummy.instantiate()
        return inst.fieldsize() * len(self)

    def __getitem__(self, i: int) -> T:
        view = self.fieldview()
        inst: MemType = self._lazy_dummy.instantiate()
        dummysize = inst.fieldsize()
        inst.load_view(view.subview(dummysize, i * dummysize))
        return inst

    def __setitem__(self, i: int, val: MemType):
        view = self.fieldview()
        inst: MemType = self._lazy_dummy.instantiate()
        if dummysize == None:
            dummysize = inst.fieldsize()
        inst.load_view(view.subview(dummysize, i * dummysize))
        if isinstance(T, MemPointer):
            inst.write(val._view.backend.address())
        else:
            inst.write(val.read())

    def __len__(self) -> int:
        return self.count

    def read(self) -> list[T]:
        result = []

        for i in range(self.count):
            result.append(self[i])

        return result
    
    def write(self, value: list[T]):
        for i in range(self.count):
            self[i] = value[i]


@memclass
class MemCppVector(MemPointer[T]):
    def fieldsize(self) -> int:
        return 8 * 3

    start_container = MemArray(0, T)
    last_ptr = MemPointer(0x8, T)
    end_ptr = MemPointer(0x10, MemUInt64)

    def _memsize(self):
        start_addr = self.start_container._view.backend.address()
        end_addr = self.end_ptr._view.backend.address()
        return end_addr - start_addr

    def __len__(self):
        inst: MemType = self._lazy_dummy.instantiate()
        self.count = self._memsize() // inst.fieldsize()
        return self.count

    def read(self) -> list[T]:
        result = []
        self.start_container.count = len(self)
        for i in range(len(self)):
            result.append(self.start_container[i])
        return result

    def write(self):
        raise NotImplementedError()


@memclass
class MemCppSharedPointer(MemPointer[T]):
    def fieldsize(self) -> int:
        return 16


@memclass
class MemCppString(MemType[str]):
    def fieldsize(self) -> int:
        return 32

    data_ptr = MemPointer(0, MemBytes)
    data_sso = MemBytes(0, 16)
    length = MemInt32(16)

    def __len__(self) -> int:
        return self.length.read()

    def read(self) -> str:
        str_len = len(self)
        if 1 > str_len:
            return ""
        
        if str_len >= 16:
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
            # Use LazyDummy directly so we don't have to make the instance an extra time for no reason
            self.data_ptr.alloc_dummy(LazyDummy(MemBytes, (self.data_ptr._offset, new_str_len + 1)))
            self.data_ptr.read().write(encoded + b"\x00")
        elif new_str_len >= 15 and cur_str_len >= 15:
            # TODO: This is definitely not right. But implementing from original for now
            self.data_ptr.read().write(encoded + "\x00")
        else:
            self.data_sso.write(encoded + b"\x00")
        
        self.length.write(new_str_len)
