from wizwalker import utils
from wizwalker import Orient
from wizwalker.memory.memory_objects.gamebryo_camera import GamebryoCamera

from .client_object import ClientObject

from memonster.memtypes import *
from memtypes import *


class CameraController(MemType):
    position = MemXYZ(108)
    orientation = MemOrient(120)

    gamebryo_camera = MemPointer(136, GamebryoCamera(0))

    def update_orientation(self, orientation: Orient = None):
        """
        Utility function that sets the camera's matrix using pitch, yaw and roll
        """
        gcam = self.gamebryo_camera.read()
        view = gcam.cam_view.read()
        mat = [x.read() for x in gcam.base_matrix.read()]
        if orientation is None:
            orientation = self.orientation.read()
        else:
            self.orientation.write(orientation)
        mat = utils.make_ypr_matrix(mat, orientation)
        view.view_matrix.write(mat)


class FreeCameraController(CameraController):
    pass


class ElasticCameraController(CameraController):
    attached_client_object = MemPointer(264, ClientObject(0))
    
    distance = MemFloat32(300)
    distance_target = MemFloat32(304)

    zoom_resolution = MemFloat32(324)
    max_distance = MemFloat32(328)
    min_distance = MemFloat32(332)

    check_collisions = MemBool(608)
