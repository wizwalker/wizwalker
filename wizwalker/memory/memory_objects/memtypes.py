from typing import TypeVar, Generic

from memonster.memtypes import *

from wizwalker.utils import XYZ, Orient


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

    def read(self) -> str:
        l = self.length.read()

        cstring = self.sso_cstring
        if l >= 16:
            # TODO: Is this l+1 correct
            cstring = cstring.cast(MemPointer(0, MemCString(0, l+1))).read()

        return cstring.read_bytes(l)

MT = TypeVar("MT", bound=MemType)

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
        self.end_ptr = MemPointer(0, dummy)

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
            res.append(p.cast_offset(self._dummy, i * s))
        return res
