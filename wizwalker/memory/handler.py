import asyncio
import struct
from typing import Any
import warnings

from loguru import logger

from . import memanagers, memutils
from wizwalker import HookAlreadyActivated, HookNotActive, HookNotReady
from .hooks import (
    ClientHook,
    MouselessCursorMoveHook,
    PlayerHook,
    PlayerStatHook,
    QuestHook,
    RootWindowHook,
    RenderContextHook,
    MovementTeleportHook,
)


# noinspection PyUnresolvedReferences
class HookHandler:
    """
    Manages hooks
    """

    AUTOBOT_PATTERN = (
        rb"\x48\x8B\xC4\x55\x41\x54\x41\x55\x41\x56\x41\x57......."
        rb"\x48......\x48.......\x48\x89\x58\x10\x48\x89"
        rb"\x70\x18\x48\x89\x78\x20.......\x48\x33\xC4....."
        rb"..\x4C\x8B\xE9.......\x80......\x0F"
    )
    # rounded down
    AUTOBOT_SIZE = 3900

    def __init__(self, allocator: memanagers.ProcessAllocator, client):
        self.client = client

        self._allocator = allocator

        self._autobot_allocator = None
        self._autobot_view = None
        self._autobot_lock = None
        self._original_autobot_bytes = b""

        self._active_hooks = []
        self._base_addrs = {}

        self._hook_cache = {}

    # noinspection PyTypeChecker
    async def _prepare_autobot(self):
        if self._autobot_allocator is None:
            cave_addr = await memutils.pattern_scan(
                self._allocator.process_handle,
                self.AUTOBOT_PATTERN,
                module="WizardGraphicalClient.exe"
            )
            if cave_addr is None:
                raise RuntimeError("Pattern scan failed for autobot pattern")
            self._autobot_allocator = memanagers.CaveAllocator(cave_addr, self.AUTOBOT_SIZE, self._allocator.process_handle)
            self._autobot_view = self._autobot_allocator.unsafe_view()

            # we only need to write back the pattern
            self._original_autobot_bytes = self._autobot_view.read_bytes(
                len(self.AUTOBOT_PATTERN)
            )
            logger.debug(
                f"Got original bytes {self._original_autobot_bytes} from autobot"
            )
            self._autobot_view.write_bytes(
                b"\x00" * self.AUTOBOT_SIZE
            )

    async def _rewrite_autobot(self):
        if self._autobot_allocator is not None:
            print("fixing autobot")
            compare_bytes = self._autobot_view.read_bytes(
                len(self.AUTOBOT_PATTERN)
            )
            # Give some time for execution point to leave hooks
            await asyncio.sleep(0.5)

            # Only write if the pattern isn't there
            if compare_bytes != self._original_autobot_bytes:
                logger.debug(
                    f"Rewriting bytes {self._original_autobot_bytes} to autobot"
                )
                self._autobot_view.write_bytes(
                    self._original_autobot_bytes
                )
            print("fixed autobot")

    async def close(self):
        for hook in self._active_hooks:
            await hook.unhook()

        async with self._autobot_lock:
            await self._rewrite_autobot()

        self._active_hooks = []
        self._autobot_allocator = None
        self._autobot_view = None
        self._base_addrs = {}

    async def _check_for_autobot(self):
        if self._autobot_lock is None:
            self._autobot_lock = asyncio.Lock()

        # this is so it isn't prepared more than once at the same time
        async with self._autobot_lock:
            await self._prepare_autobot()

    def _check_if_hook_active(self, hook_type) -> bool:
        for hook in self._active_hooks:
            if isinstance(hook, hook_type):
                return True

        return False

    def _get_hook_by_type(self, hook_type) -> Any:
        for hook in self._active_hooks:
            if isinstance(hook, hook_type):
                return hook

        return None

    async def _read_hook_base_addr(self, addr_name: str, hook_name: str):
        addr = self._base_addrs.get(addr_name)
        if addr is None:
            raise HookNotActive(hook_name)

        try:
            return await self.read_typed(addr, "long long")
        except pymem.exception.MemoryReadError:
            raise HookNotReady(hook_name)

    # wait for an addr to be set and not 0
    async def _wait_for_value(self, address: int, timeout: int = None):
        async def _wait_for_value_task():
            while True:
                try:
                    value = await self.read_typed(address, "long long")
                    logger.debug(
                        f"Waiting for address {hex(address)}; got value {value}"
                    )
                except pymem.exception.MemoryReadError:
                    pass
                else:
                    if value != 0:
                        logger.debug(f"Address {hex(address)} is set")
                        break
                    else:
                        logger.debug(f"Address {hex(address)} is not set yet; sleeping")
                        await asyncio.sleep(0.5)

        try:
            await asyncio.wait_for(_wait_for_value_task(), timeout)
        except TimeoutError:
            # TODO: replace error
            raise TimeoutError("Hook value took too long")

    # TODO: make this faster
    async def activate_all_hooks(
        self, *, wait_for_ready: bool = True, timeout: float = None
    ):
        """
        Activate all hooks but mouseless

        Keyword Args:
            wait_for_ready: Wait for hook values to be written
            timeout: How long to wait for hook values to be written (None for no timeout)
        """
        await self.activate_player_hook(wait_for_ready=False)
        # quest hook is not written if the quest arrow is off
        await self.activate_quest_hook()
        await self.activate_player_stat_hook(wait_for_ready=False)
        await self.activate_client_hook(wait_for_ready=False)
        await self.activate_root_window_hook(wait_for_ready=False)
        await self.activate_render_context_hook(wait_for_ready=False)
        await self.activate_movement_teleport_hook(wait_for_ready=False)

        if wait_for_ready:
            wait_tasks = []
            for atter_name in [
                "player_struct",
                "player_stat_struct",
                "current_client",
                "current_root_window",
                "current_render_context",
            ]:
                value = self._base_addrs[atter_name]
                wait_tasks.append(
                    asyncio.create_task(self._wait_for_value(value, timeout))
                )

            await asyncio.gather(*wait_tasks)

    async def activate_player_hook(
        self, *, wait_for_ready: bool = True, timeout: float = None
    ):
        """
        Activate player hook

        Keyword Args:
            wait_for_ready: Wait for hook values to be written
            timeout: How long to wait for hook values to be written (None for no timeout)
        """
        if self._check_if_hook_active(PlayerHook):
            raise HookAlreadyActivated("Player")

        await self._check_for_autobot()

        player_hook = PlayerHook(self)
        await player_hook.hook()

        self._active_hooks.append(player_hook)
        self._base_addrs["player_struct"] = player_hook.player_struct

        if wait_for_ready:
            await self._wait_for_value(player_hook.player_struct, timeout)

    async def deactivate_player_hook(self):
        """
        Deactivate player hook
        """
        if not self._check_if_hook_active(PlayerHook):
            raise HookNotActive("Player")

        hook = self._get_hook_by_type(PlayerHook)
        self._active_hooks.remove(hook)
        await hook.unhook()

        del self._base_addrs["player_struct"]

    async def read_current_player_base(self) -> int:
        """
        Read player base address

        Returns:
            The player base address
        """
        return await self._read_hook_base_addr("player_struct", "Player")

    async def activate_duel_hook(
        self, *, wait_for_ready: bool = False, timeout: float = None
    ):
        """
        Deprecated
        """
        warnings.warn(DeprecationWarning("The duel hook is deprecated as it is unneeded. activate_duel_hook will remain as a noop until 2.0"))

    async def deactivate_duel_hook(self):
        """
        Deprecated
        """
        warnings.warn(DeprecationWarning("The duel hook is deprecated as it is unneeded. deactivate_duel_hook will remain as a noop until 2.0"))

    async def read_current_duel_base(self) -> int:
        """
        Deprecated
        """
        warnings.warn(DeprecationWarning("The duel hook is deprecated as it is unneeded. read_current_duel_base will remain as a noop until 2.0"))
        return 0

    async def read_current_duel_phase(self) -> int:
        """
        Deprecated
        """
        warnings.warn(DeprecationWarning("The duel hook is deprecated as it is unneeded. read_current_duel_phase will remain as a noop until 2.0"))
        return 0

    async def activate_quest_hook(
        self, *, wait_for_ready: bool = False, timeout: float = None
    ):
        """
        Activate quest hook

        Keyword Args:
            wait_for_ready: Wait for hook values to be written
            timeout: How long to wait for hook values to be written (None for no timeout)
        """
        if self._check_if_hook_active(QuestHook):
            raise HookAlreadyActivated("Quest")

        await self._check_for_autobot()

        quest_hook = QuestHook(self)
        await quest_hook.hook()

        self._active_hooks.append(quest_hook)
        self._base_addrs["quest_struct"] = quest_hook.cord_struct

        if wait_for_ready:
            await self._wait_for_value(quest_hook.cord_struct, timeout)

    async def deactivate_quest_hook(self):
        """
        Deactivate quest hook
        """
        if not self._check_if_hook_active(QuestHook):
            raise HookNotActive("Quest")

        hook = self._get_hook_by_type(QuestHook)
        self._active_hooks.remove(hook)
        await hook.unhook()

        del self._base_addrs["quest_struct"]

    async def read_current_quest_base(self) -> int:
        """
        Read quest base address

        Returns:
            The quest base address
        """
        return await self._read_hook_base_addr("quest_struct", "Quest")

    async def activate_player_stat_hook(
        self, *, wait_for_ready: bool = True, timeout: float = None
    ):
        """
        Activate player stat hook

        Keyword Args:
            wait_for_ready: Wait for hook values to be written
            timeout: How long to wait for hook values to be written (None for no timeout)
        """
        if self._check_if_hook_active(PlayerStatHook):
            raise HookAlreadyActivated("Player stat")

        await self._check_for_autobot()

        player_stat_hook = PlayerStatHook(self)
        await player_stat_hook.hook()

        self._active_hooks.append(player_stat_hook)
        self._base_addrs["player_stat_struct"] = player_stat_hook.stat_addr

        if wait_for_ready:
            await self._wait_for_value(player_stat_hook.stat_addr, timeout)

    async def deactivate_player_stat_hook(self):
        """
        Deactivate player stat hook
        """
        if not self._check_if_hook_active(PlayerStatHook):
            raise HookNotActive("Player stat")

        hook = self._get_hook_by_type(PlayerStatHook)
        self._active_hooks.remove(hook)
        await hook.unhook()

        del self._base_addrs["player_stat_struct"]

    async def read_current_player_stat_base(self) -> int:
        """
        Read player stat base address

        Returns:
            The player stat base address
        """
        return await self._read_hook_base_addr("player_stat_struct", "Player stat")

    async def activate_client_hook(
        self, *, wait_for_ready: bool = True, timeout: float = None
    ):
        """
        Activate client hook

        Keyword Args:
            wait_for_ready: Wait for hook values to be written
            timeout: How long to wait for hook values to be written (None for no timeout)
        """
        if self._check_if_hook_active(ClientHook):
            raise HookAlreadyActivated("Client")

        await self._check_for_autobot()

        client_hook = ClientHook(self)
        await client_hook.hook()

        self._active_hooks.append(client_hook)
        self._base_addrs["current_client"] = client_hook.current_client_addr

        if wait_for_ready:
            await self._wait_for_value(client_hook.current_client_addr, timeout)

    async def deactivate_client_hook(self):
        """
        Deactivate client hook
        """
        if not self._check_if_hook_active(ClientHook):
            raise HookNotActive("Client")

        hook = self._get_hook_by_type(ClientHook)
        self._active_hooks.remove(hook)
        await hook.unhook()

        del self._base_addrs["current_client"]

    async def read_current_client_base(self) -> int:
        """
        Read cureent client base address

        Returns:
            The current client base address
        """
        return await self._read_hook_base_addr("current_client", "Client")

    async def activate_root_window_hook(
        self, *, wait_for_ready: bool = True, timeout: float = None
    ):
        """
        Activate root window hook

        Keyword Args:
            wait_for_ready: Wait for hook values to be written
            timeout: How long to wait for hook values to be written (None for no timeout)
        """
        if self._check_if_hook_active(RootWindowHook):
            raise HookAlreadyActivated("Root window")

        await self._check_for_autobot()

        root_window_hook = RootWindowHook(self)
        await root_window_hook.hook()

        self._active_hooks.append(root_window_hook)
        self._base_addrs[
            "current_root_window"
        ] = root_window_hook.current_root_window_addr

        if wait_for_ready:
            await self._wait_for_value(
                root_window_hook.current_root_window_addr, timeout
            )

    async def deactivate_root_window_hook(self):
        """
        Deactivate root window hook
        """
        if not self._check_if_hook_active(RootWindowHook):
            raise HookNotActive("Root window")

        hook = self._get_hook_by_type(RootWindowHook)
        self._active_hooks.remove(hook)
        await hook.unhook()

        del self._base_addrs["current_root_window"]

    async def read_current_root_window_base(self) -> int:
        """
        Read current root window base address

        Returns:
            The current root window base address
        """
        return await self._read_hook_base_addr("current_root_window", "Root window")

    async def activate_render_context_hook(
        self, *, wait_for_ready: bool = True, timeout: float = None
    ):
        """
        Activate render context hook

        Keyword Args:
            wait_for_ready: Wait for hook values to be written
            timeout: How long to wait for hook values to be written (None for no timeout)
        """
        if self._check_if_hook_active(RenderContextHook):
            raise HookAlreadyActivated("Render context")

        await self._check_for_autobot()

        render_context_hook = RenderContextHook(self)
        await render_context_hook.hook()

        self._active_hooks.append(render_context_hook)
        self._base_addrs[
            "current_render_context"
        ] = render_context_hook.current_render_context_addr

        if wait_for_ready:
            await self._wait_for_value(
                render_context_hook.current_render_context_addr, timeout
            )

    async def deactivate_render_context_hook(self):
        """
        Deactivate render context hook
        """
        if not self._check_if_hook_active(RenderContextHook):
            raise HookNotActive("Render context")

        hook = self._get_hook_by_type(RenderContextHook)
        self._active_hooks.remove(hook)
        await hook.unhook()

        del self._base_addrs["current_render_context"]

    async def read_current_render_context_base(self) -> int:
        """
        Read current render context base address

        Returns:
            The current render context base address
        """
        return await self._read_hook_base_addr(
            "current_render_context", "Render context"
        )

    async def activate_movement_teleport_hook(
            self, *, wait_for_ready: bool = False, timeout: float = None
    ):
        """
        Activate movement teleport hook

        wait_for_ready is useless for this hook

        Keyword Args:
            wait_for_ready: Wait for hook values to be written
            timeout: How long to wait for hook values to be written (None for no timeout)
        """
        if self._check_if_hook_active(MovementTeleportHook):
            raise HookAlreadyActivated("Movement teleport")

        await self._check_for_autobot()

        movement_teleport_hook = MovementTeleportHook(self)
        await movement_teleport_hook.hook()

        self._active_hooks.append(movement_teleport_hook)
        self._base_addrs[
            "teleport_helper"
        ] = movement_teleport_hook.teleport_helper

    async def deactivate_movement_teleport_hook(self):
        """
        Deactivate movement teleport hook
        """
        if not self._check_if_hook_active(MovementTeleportHook):
            raise HookNotActive("Movement teleport")

        hook = self._get_hook_by_type(MovementTeleportHook)
        self._active_hooks.remove(hook)
        await hook.unhook()

        del self._base_addrs["teleport_helper"]

    def read_teleport_helper(self) -> int:
        """
        Read teleport helper base address

        Returns:
            The teleport helper base address
        """
        addr = self._base_addrs.get("teleport_helper")
        if addr is None:
            raise HookNotActive("Movement teleport")

        return addr

    # nothing to wait for in this hook
    async def activate_mouseless_cursor_hook(self):
        """
        Activate mouseless cursor hook
        """
        if self._check_if_hook_active(MouselessCursorMoveHook):
            raise HookAlreadyActivated("Mouseless cursor")

        await self._check_for_autobot()

        mouseless_cursor_hook = MouselessCursorMoveHook(self, self._hook_cache)
        await mouseless_cursor_hook.hook()

        self._active_hooks.append(mouseless_cursor_hook)
        self._base_addrs["mouse_position"] = mouseless_cursor_hook.mouse_pos_addr

        await self.write_mouse_position(0, 0)

    async def deactivate_mouseless_cursor_hook(self):
        """
        Deactivate mouseless cursor hook
        """
        if not self._check_if_hook_active(MouselessCursorMoveHook):
            raise HookNotActive("Mouseless cursor")

        hook = self._get_hook_by_type(MouselessCursorMoveHook)
        self._active_hooks.remove(hook)
        await hook.unhook()

        del self._base_addrs["mouse_position"]

    # TODO: 2.0 switch this to a helper object like movement teleport and quest
    async def write_mouse_position(self, x: int, y: int):
        """
        Write mouse position to memory

        Args:
            x: x position of mouse
            y: y position of mouse
        """
        addr = self._base_addrs.get("mouse_position")
        if addr is None:
            raise HookNotActive("Mouseless cursor")

        packed_position = struct.pack("<ii", x, y)

        await self.write_bytes(addr, packed_position)
