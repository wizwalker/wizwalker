from typing import Optional, Union

from wizwalker import utils
from wizwalker.memory.memory_object import MemoryObject
from wizwalker.memory.memonster.memanagers import MemoryView
from wizwalker.memory.memonster.memtypes import *
from wizwalker.memory.memory_objects.gamebryo_camera import GamebryoCamera

from .client_object import ClientObject


class CameraController(MemoryView):
    # TODO: camera 0x88 offset

    @staticmethod
    def obj_size() -> int:
        # unverified
        return 144

    position = MemXYZ(108)

    orientation = MemOrient(120)
    pitch = MemFloat32(120)
    roll = MemFloat32(124)
    yaw = MemFloat32(128)

    # TODO: Make work
    # async def gamebryo_camera(self) -> Optional[DynamicGamebryoCamera]:
    #     addr = await self.read_value_from_offset(136, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicGamebryoCamera(self.hook_handler, addr)

    # async def update_orientation(self, orientation: Orient = None):
    #     """
    #     Utility function that sets the camera's matrix using pitch, yaw and roll
    #     """
    #     gcam = await self.gamebryo_camera()
    #     view = await gcam.cam_view()
    #     mat = await gcam.base_matrix()
    #     if orientation is None:
    #         orientation = await self.orientation()
    #     else:
    #         await self.write_orientation(orientation)
    #     mat = utils.make_ypr_matrix(mat, orientation)
    #     await view.write_view_matrix(mat)


class FreeCameraController(CameraController):
    pass


class ElasticCameraController(CameraController):
    @staticmethod
    def obj_size() -> int:
        return 612

    # TODO: Make work
    # async def attached_client_object(self) -> Optional[DynamicClientObject]:
    #     addr = await self.read_value_from_offset(264, "unsigned long long")

    #     if addr == 0:
    #         return None

    #     return DynamicClientObject(self.hook_handler, addr)

    # async def write_attached_client_object(self, attached_client_object: Union[ClientObject, int]):
    #     if isinstance(attached_client_object, ClientObject):
    #         attached_client_object = await attached_client_object.read_base_address()

    #     await self.write_value_to_offset(264, attached_client_object, "unsigned long long")

    distance = MemFloat32(300)
    distance_target = MemFloat32(304)

    zoom_resolution = MemFloat32(324)

    max_distance = MemFloat32(328)
    min_distance = MemFloat32(332)

    check_collision = MemBool(608)
