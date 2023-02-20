from wizwalker.memory.memory_object import MemoryObject

from memonster.memtypes import *
from memtypes import *


class CamView(MemType):
    # TODO: Find real name (or more fitting)

    view_matrix = MemArray(80, 9, MemFloat32(0))
    
    viewport_left = MemFloat32(288)
    viewport_right = MemFloat32(292)
    viewport_top = MemFloat32(296)
    viewport_bottom = MemFloat32(300)
    cull_near = MemFloat32(304)
    cull_far = MemFloat32(308)
    
    base_cull_near = MemFloat32(316)
    base_cull_far = MemFloat32(320)
    screenport_left = MemFloat32(324)
    screenport_right = MemFloat32(328)
    screenport_top = MemFloat32(32)
    screenport_bottom = MemFloat32(336)
