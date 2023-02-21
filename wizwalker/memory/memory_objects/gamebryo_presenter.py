from wizwalker.memory.memory_objects.scene_manager import SceneManager

from memonster.memtypes import *
from .memtypes import *


class GamebryoPresenter(MemType):
    default_background_color_blue = MemInt32(0x48)
    default_background_color_green = MemInt32(0x4C)
    default_background_color_blue = MemInt32(0x50)

    scene_manager = MemPointer(0x68, SceneManager(0))

    shadow_detail = MemInt32(0x8C)
    #master_scene_root = MemUInt64(0x90)

    #master_collision_scene = MemUInt64(0xA8)

    nametag_flags = MemInt32(0x190)
