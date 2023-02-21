from memonster.memtypes import *
from .memtypes import *


class RenderContext(MemType):
    ui_scale = MemFloat32(152)


# TODO: Monster
class CurrentRenderContext(RenderContext):
    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_render_context_base()
