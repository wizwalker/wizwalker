from wizwalker.memory.memory_objects.cam_view import CamView

from memonster.memtypes import *
from memtypes import *


class GamebryoCamera(MemType):
    base_matrix = MemArray(164, 9, MemFloat32(0))
    cam_view = MemPointer(200, CamView(0))
