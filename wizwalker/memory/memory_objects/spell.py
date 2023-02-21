from wizwalker.memory.memory_object import PropertyClass
from .enums import DelayOrder
from .spell_template import SpellTemplate
from .spell_effect import SpellEffect

from memonster import LazyType
from memonster.memtypes import *
from .memtypes import *


class Rank(MemType):
    regular_rank = MemUInt8(72)
    shadow_rank = MemUInt8(73)


class Spell(PropertyClass):
    delay_enchantment_order = MemEnum(72, DelayOrder)
    enchantment_spell_is_item_card = MemBool(76)
    enchanted_this_combat = MemBool(77)

    enchantment = MemUInt32(80)

    spell_effects = MemCppVector(88, MemCppSharedPointer(0, SpellEffect(0)))

    premutation_spell_id = MemUInt32(112)

    spell_template = MemPointer(120, SpellTemplate(0))
    template_id = MemUInt32(128)
    accuracy = MemUInt8(132)

    magic_school_id = MemUInt32(136)

    rank = Rank(176)

    regular_adjust = MemInt32(192)
    cloaked = MemBool(196)
    treasure_card = MemBool(197)
    battle_card = MemBool(198)
    item_card = MemBool(199)
    side_board = MemBool(200)

    spell_id = MemUInt32(204)

    leaves_play_when_cast_override = MemBool(216)

    delay_enchantment = MemBool(257)

    round_added_tc = MemInt32(260)
    pve = MemBool(264)


class GraphicalSpell(Spell):
    pass


class Hand(PropertyClass):
    spell_list = MemCppLinkedList(72, MemCppSharedPointer(0, Spell(0)))
