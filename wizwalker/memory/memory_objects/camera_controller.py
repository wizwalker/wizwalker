from typing import Optional, Union

from wizwalker.memory.memonster.memanagers import MemType
from wizwalker.memory.memonster.memtypes import *
from wizwalker.memory.memonster import memclass
from wizwalker.memory.memory_objects.gamebryo_camera import GamebryoCamera

from .client_object import ClientObject


@memclass
class CameraController(MemType):
    # TODO: camera 0x88 offset

    def fieldsize(self) -> int:
        return 144

    position = MemXYZ(108)

    orientation = MemOrient(120)
    pitch = MemFloat32(120)
    roll = MemFloat32(124)
    yaw = MemFloat32(128)

    gamebryo_camera = MemPointer[GamebryoCamera](136, GamebryoCamera())

    # TODO: Make work
    # def update_orientation(self, orientation: Orient = None):
    #     """
    #     Utility function that sets the camera's matrix using pitch, yaw and roll
    #     """
    #     gcam = self.gamebryo_camera.read()
    #     view = gcam.cam_view.read()
    #     mat = await gcam.base_matrix()
    #     if orientation is None:
    #         orientation = await self.orientation()
    #     else:
    #         await self.write_orientation(orientation)
    #     mat = utils.make_ypr_matrix(mat, orientation)
    #     await view.write_view_matrix(mat)


@memclass
class FreeCameraController(CameraController):
    pass


@memclass
class ElasticCameraController(CameraController):
    def fieldsize(self) -> int:
        # unverified
        return 612

    attached_client_object = MemPointer[ClientObject](264, ClientObject)

    distance = MemFloat32(300)
    distance_target = MemFloat32(304)

    zoom_resolution = MemFloat32(324)

    max_distance = MemFloat32(328)
    min_distance = MemFloat32(332)

    check_collision = MemBool(608)
