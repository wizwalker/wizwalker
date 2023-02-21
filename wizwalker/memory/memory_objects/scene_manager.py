from .enums import FogMode

from memonster.memtypes import *
from .memtypes import *


class SceneManager(MemType):
    # 0x60 has skybox list (0x68 end)

    # These fog settings are technically inlined
    fog_mode = MemEnum(0x180, FogMode)
    fog_density = MemFloat32(0x184)
    fog_density_target = MemFloat32(0x188)
    fog_start_density = MemFloat32(0x18C)
    fog_color_red = MemFloat32(0x190)
    fog_color_green = MemFloat32(0x194)
    fog_color_blue = MemFloat32(0x198)
