from typing import TypeVar, Generic

from memonster import LazyType
from memonster.memtypes import *

from wizwalker.utils import XYZ, Orient


T = TypeVar("T")
MT = TypeVar("MT")

# Maybe one day count can be part of generic signature
class MemArray(MemType, Generic[MT]):
    def __init__(self, offset: int, elements: int, dummy: MT) -> None:
        super().__init__(offset)
        self.elements = elements
        self._dummy = dummy

    def read(self) -> list[MT]:
        tsize = self._dummy.size()
        res = []
        for i in range(self.elements):
            res.append(self.cast_offset(i * tsize, self._dummy))
        return res

    # TODO: Make sure this works at all
    def write(self, data: list[MT]):
        assert len(data) == self.elements
        tsize = self._dummy.size()
        for i in range(self.elements):
            self.cast_offset(i * tsize, self._dummy).write(data[i].cast(self._dummy).read())

# TODO: Convert to use MemArray
class MemXYZ(MemType):
    x = MemFloat32(0)
    y = MemFloat32(4)
    z = MemFloat32(8)

    def read(self) -> XYZ:
        return XYZ(self.x.read(), self.y.read(), self.z.read())

    def write(self, data: XYZ):
        self.x.write(data.x)
        self.y.write(data.y)
        self.z.write(data.z)

class MemOrient(MemType):
    pitch = MemFloat32(0)
    roll = MemFloat32(4)
    yaw = MemFloat32(8)

    def read(self) -> Orient:
        return Orient(self.pitch.read(), self.roll.read(), self.yaw.read())

    def write(self, data: Orient):
        self.pitch.write(data.pitch)
        self.roll.write(data.roll)
        self.yaw.write(data.yaw)

class MemCppString(MemType):
    sso_cstring = MemCString(0, 16)
    length = MemInt32(16)

    def read(self) -> bytes:
        l = self.length.read()

        cstring = self.sso_cstring
        if l >= 16:
            # TODO: Is this l+1 correct
            cstring = cstring.cast(MemPointer(0, MemCString(0, l+1))).read()

        return cstring.read_bytes(l)

class MemCppSharedPointer(MemPointer, Generic[MT]):
    # Only here to make python's type inference work
    def __init__(self, offset: int, dummy: MT) -> None:
        super().__init__(offset, dummy)

    # refer to above
    def read(self) -> MT:
        return super().read()

    def size(self) -> int:
        return 16

class MemCppVector(MemType, Generic[MT]):
    def __init__(self, offset: int, dummy: MT) -> None:
        super().__init__(offset)
        self._dummy = dummy
        self.start_ptr = MemPointer(0, dummy)
        self.end_ptr = MemPointer(8, dummy)

    def count(self) -> int:
        # TODO: Change this once inference is added, for now only support types that add this method
        s = self._dummy.size()
        size = self.end_ptr.cast(MemInt64(0)).read() - self.start_ptr.cast(MemInt64(0)).read()
        return size // s

    def read(self) -> list[MT]:
        res = []
        c = self.count()
        if c <= 0:
            return []

        s = self._dummy.size()
        p = self.start_ptr.read()
        for i in range(c):
            res.append(p.cast_offset(i * s, self._dummy))
        return res

class MemCppLinkedListNode(MemType, Generic[MT]):
    def __init__(self, offset: int, dummy: MT) -> None:
        super().__init__(offset)
        self._dummy = dummy

        # Empty on head node
        self.data = copy.copy(self._dummy)
        self.data.offset = 16

        self.next = MemPointer(0, LazyType(MemCppLinkedListNode)(self._dummy))
        self.prev = MemPointer(8, LazyType(MemCppLinkedListNode)(self._dummy))

    def read(self) -> MT:
        return self.data.read()

class MemCppLinkedList(MemType, Generic[MT]):
    def __init__(self, offset: int, dummy: MT) -> None:
        super().__init__(offset)
        self._dummy = dummy
        self.head = MemCppLinkedListNode(0, self._dummy)

    list_size = MemInt64(8)

    def read(self) -> list[MT]:
        res = []
        size = self.list_size.read()
        if size < 1:
            return res
        node = self.head.next.read()
        for _ in range(size):
            res.append(node.read())
            node = node.next.read()
        return res


class MemCppHashNode(MemType, Generic[MT]):
    def __init__(self, offset: int, _dummy: MT) -> None:
        super().__init__(offset)
        self._dummy = _dummy
        
        self.left = MemPointer(0, LazyType(MemCppHashNode)(0, self._dummy))
        self.parent = MemPointer(8, LazyType(MemCppHashNode)(0, self._dummy))
        self.right = MemPointer(0x10, LazyType(MemCppHashNode)(0, self._dummy))

        self.data = MemPointer(0x28, self._dummy)

    is_leaf = MemBool(0x19)
    hash = MemUInt32(0x20)

    def read(self) -> dict[int, MT]:
        res = {}

        if not self.is_leaf.read():
            res[self.hash.read()] = self.data.read()

            # TODO: Better error handling
            try:
                res = res | self.left.read().read()
            except:
                pass
            try:
                res = res | self.right.read().read()
            except:
                pass

        return res

class MemCppMap(MemType, Generic[MT]):
    def __init__(self, offset: int, _dummy: MT) -> None:
        super().__init__(offset)
        self._dummy = _dummy
        self.root = MemPointer(0, MemCppHashNode(0, self._dummy))

    def read(self) -> dict[int, MT]:
        res = {}

        root = self.root.read()
        first_node = root.parent.read()

        if first_node._memview.address == root._memview.address:
            return res

        return res
