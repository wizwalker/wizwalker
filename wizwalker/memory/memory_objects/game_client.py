from .camera_controller import (
    CameraController,
    CameraController,
    FreeCameraController,
    ElasticCameraController,
)
from .client_object import ClientObject
from .character_registry import CharacterRegistry
from .enums import AccountPermissions
from .gamebryo_presenter import GamebryoPresenter

from memonster.memtypes import *
from .memtypes import *


# note: not defined
class GameClient(MemType):
    # TODO: Monster
    def __init__(self, offset: int) -> None:
        super().__init__(offset)

        if offset := self.pattern_scan_offset_cached(
                rb".......\x48\x8B\x01\xFF\x50\x40\x84\xC0\x75.\xE8",
                3,
                "gamebryo_presenter",
                0x21FB8
            ):
            self.gamebryo_presenter.offset = offset

        if offset := self.pattern_scan_offset_cached(
                rb"\x83\xBB\x40\x1D\x02\x00\x00\x75\x04\xB2\x01\xEB\x02\x33\xD2\x48\x8B.....\xE8",
                2,
                "has_membership",
                0x21D40
            ):
            self.has_membership.offset = offset

        if offset := self.pattern_scan_offset_cached(
                rb"\x38\x9F\xB8\x11\x02\x00\x74\xBE\xE8....\x83\xF8\x64\x0F\x8F....\xB9\x0F\x00\x00\x00",
                2,
                "shutdown_signal",
                0x211B8
            ):
            self.shutdown_signal.offset = offset

        if offset := self.pattern_scan_offset_cached(
                rb"\xF3\x0F\x11\x8B\xFC\x19\x02\x00\xC7\x05........\xF2\x0F"
                rb"\x11.....\x48\x8B\x8B\x00\x13\x02\x00\x48\x85\xC9\x74\x09",
                4,
                "frames_per_second",
                0x219FC
            ):
            self.frames_per_second.offset = offset

        if offset := self.pattern_scan_offset_cached(
                rb"\x0F\xB6\x88\x20\x20\x02\x00\x88\x8B\x6A"
                rb"\x02\x00\x00\x84\xC9\x0F\x85....\x48\x8D"
                rb"\x55\xE0\x48\x8B\xCB\xE8",
                3,
                "is_freecam",
                0x22020
            ):
            self.is_freecam.offset = offset

        if offset := self.pattern_scan_offset_cached(
                rb"\x48\x89\x87\x08\x20\x02\x00\x48\x8D\x8F"
                rb"\x10\x20\x02\x00\x48\x8D\x54\x24\x40\xE8"
                rb"....\x90\x48\x8B\x4C\x24",
                3,
                "selected_camera_controller",
                0x22008
            ):
            self.selected_camera_controller.offset = offset

        if offset := self.pattern_scan_offset_cached(
                rb"\x48\x8B\x93....\x48\x8B\x03\x4C\x8B\x88...."
                rb"\x41\xB8\x01\x00\x00\x00\x48\x8B\xCB\x48\x3B\xFA\x75",
                3,
                "free_camera_controller",
                0x21fe8
            ):
            self.free_camera_controller.offset = offset

    shutdown_signal = MemInt32(0x211B8)

    root_client_object = MemPointer(0x21318, ClientObject(0))

    frames_per_second = MemFloat32(0x219FC)

    account_permissions = MemEnum(0x21D3C, AccountPermissions)
    has_membership = MemBool(0x21D40)

    gamebryo_presenter = MemPointer(0x21FB8, GamebryoPresenter(0))

    free_camera_controller = MemPointer(0x21fe8, FreeCameraController(0))

    elastic_camera_controller = MemPointer(0x21fd8, ElasticCameraController(0))

    selected_camera_controller = MemPointer(0x22008, CameraController(0))

    is_freecam = MemBool(0x22020)

    character_registry = MemPointer(0x22488, CharacterRegistry(0))

class CurrentGameClient(GameClient):
    _base_address = None

    async def read_base_address(self) -> int:
        if self._base_address is not None:
            return self._base_address

        addr = await self.pattern_scan(rb"\x48\x8B.....\x48\x8B\xD9\x80\xB8\x45")
        offset = await self.read_typed(addr + 3, "int")

        self._base_address = await self.read_typed(addr + 7 + offset, "unsigned long long")
        return self._base_address
