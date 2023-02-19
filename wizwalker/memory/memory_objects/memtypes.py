from memonster import MemType, MemFloat32, MemInt32, MemCString, MemPointer

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

        # TODO: Maybe read bytes instead to deal with null inside of string
        return cstring.read()
