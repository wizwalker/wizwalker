from typing import Callable, List, Optional
from contextlib import suppress

from wizwalker.memory.memory_object import PropertyClass
from .enums import WindowFlags, WindowStyle
from .spell import GraphicalSpell
from .combat_participant import CombatParticipant
from wizwalker import AddressOutOfRange, MemoryReadError, Rectangle, utils

from memonster import LazyType
from memonster.memtypes import *
from .memtypes import *


# TODO: Window.click
class Window(PropertyClass):
    # TODO: Monster
    async def debug_print_ui_tree(self):
        print(await self.get_ui_tree_stringified())

    # TODO: Monster
    async def get_ui_tree_stringified(self, indent_str = "-") -> str:
        async def traverse_tree(branch, depth):
            nonlocal indent_str
            if type(branch) == str:
                return f"{indent_str * depth} {branch}\n"
            else:
                result = ""
                for x in branch:
                    result += await traverse_tree(x, depth + 1)
                return result
        return await traverse_tree(await self.get_ui_tree_strings(), 0)

    # TODO: Monster
    async def get_ui_tree_strings(self) -> list:
        result = [f"[{self.name.read()}] {self.maybe_read_type_name()}"]
        for child in await utils.wait_for_non_error(self.children):
            result.append(await child.get_ui_tree_strings())
        return result

    # TODO: Monster
    async def debug_paint(self):
        rect = await self.scale_to_client()
        rect.paint_on_screen(self.hook_handler.client.window_handle)

    # TODO: Monster
    async def scale_to_client(self) -> Rectangle:
        rect = self.window_rectangle.read()

        parent_rects = []
        for parent in self.get_parents():
            parent_rects.append(parent.window_rectangle.read())

        ui_scale = await self.hook_handler.client.render_context.ui_scale()

        return rect.scale_to_client(parent_rects, ui_scale)

    def get_windows_with_type(self, type_name: str) -> list["Window"]:
        def _pred(window: Window):
            return window.maybe_read_type_name() == type_name
        return self.get_windows_with_predicate(_pred)

    def get_windows_with_name(self, name: str) -> list["Window"]:
        def _pred(window: Window):
            return window.name.read()() == name
        return self.get_windows_with_predicate(_pred)

    def _recursive_get_windows_by_predicate(self, predicate, windows: list["Window"]):
        # TODO: Monster errors
        with suppress(ValueError, MemoryReadError, AddressOutOfRange):
            for child in [x.read() for x in self.children.read()]:
                if predicate(child):
                    windows.append(child)
                child._recursive_get_windows_by_predicate(predicate, windows)

    def get_windows_with_predicate(
        self, predicate: Callable
    ) -> List["Window"]:
        """
        async def my_pred(window) -> bool:
            if await window.name() == "friend's list":
              return True

            return False

        await client.root_window.get_windows_by_predicate(my_pred)
        """
        windows = []

        # check our own children
        try:
            children = [x.read() for x in self.children.read()]
        except (ValueError, MemoryReadError, AddressOutOfRange):
            children = []

        for child in children:
            if predicate(child):
                windows.append(child)

        for child in children:
            child._recursive_get_windows_by_predicate(predicate, windows)

        return windows

    def get_parents(self) -> list["Window"]:
        parents = []
        current = self
        while True:
            parent = current.parent.read()
            if parent._memview.address == 0:
                break
            parents.append(parent)
        return parents

    def get_child_by_name(self, name: str) -> "Window":
        children = [x.read() for x in self.children.read()]
        for child in children:
            if child.name.read() == name:
                return child
        raise ValueError(f"No child named {name}")

    @property
    def is_visible(self) -> bool:
        return WindowFlags.visible in self.flags.read()

    # This is here because checking in .children slows down window filtering majorly
    def maybe_graphical_spell(self, *, check_type: bool = False) -> Optional[GraphicalSpell]:
        if check_type:
            type_name = self.maybe_read_type_name()
            if type_name != "SpellCheckBox":
                raise ValueError(f"This object is a {type_name} not a SpellCheckBox.")
        return self.cast_offset(952, MemPointer(0, GraphicalSpell(0)))

    # note: not defined
    def maybe_spell_grayed(self, *, check_type: bool = False) -> bool:
        if check_type:
            type_name = self.read_type_name()
            if type_name != "SpellCheckBox":
                raise ValueError(f"This object is a {type_name} not a SpellCheckBox")
        return self.cast_offset(1024, MemBool(0))

    def maybe_combat_participant(self, *, check_type: bool=False) -> Optional(CombatParticipant):
        if check_type:
            type_name = self.maybe_read_type_name()
            if type_name != "CombatantDataControl":
                raise ValueError(
                    f"This object is a {type_name} not a CombatantDataControl."
                )
        return self.cast_offset(1672, MemPointer(0, CombatParticipant(0)))

    def __init__(self, offset: int) -> None:
        super().__init__(offset)
        self.children = MemCppVector(112, MemCppSharedPointer(0, LazyType(Window)(0)))
        self.parent = MemPointer(136, LazyType(Window)(0))

    name = MemCppString(80)

    style = MemEnum(152, WindowStyle)
    flags = MemEnum(156, WindowFlags)
    window_rectangle = MemRectangle(160)
    parent_offset = MemRectangle(176)
    offset = MemPoint(192)
    scale = MemPoint(200)
    alpha = MemFloat32(208)
    target_alpha = MemFloat32(212)
    disabled_alpha = MemFloat32(216)

    help = MemCppString(248)

    script = MemCppString(352)

    tip = MemCppString(392)

    maybe_text = MemCppWideString(584)


class DeckListControlSpellEntry(MemType):
    def size(self) -> int:
        return 0x28

    graphical_spell = MemPointer(0, GraphicalSpell(0))


class SpellListControlSpellEntry(MemType):
    def size(self):
        return 0x20

    graphical_spell = MemPointer(0, GraphicalSpell(0))

    max_copies = MemUInt32(0x10)
    current_copies = MemUInt32(0x14)
    window_rectangle = MemPointer(0x18, MemRectangle(0))


class DeckListControl(Window):
    spell_entries = MemCppVector(0x280, DeckListControlSpellEntry(0))

    card_size_horizontal = MemUInt32(0x2A4)
    card_size_vertical = MemUInt32(0x2A8)
    card_spacing = MemUInt32(0x2AC)
    card_spacing_vertical_adjust = MemUInt32(0x2B0)


class SpellListControl(Window):
    spell_entries = MemCppVector(0x278, SpellListControlSpellEntry(0))

    card_size_horizontal = MemUInt32(0x2C4)
    card_size_vertical = MemUInt32(0x2C8)


# TODO: Monster
class CurrentRootWindow(Window):
    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_root_window_base()
