from wizwalker.memory.memory_object import PropertyClass
from .enums import DelayOrder, SpellSourceType
from .spell_effect import SpellEffect

from memonster.memtypes import *
from .memtypes import *


class SpellTemplate(PropertyClass):
    name = MemCppString(96)

    display_name = MemCppString(136)
    description = MemCppString(168)
    base_cost = MemInt32(200)
    credits_cost = MemInt32(204)
    pvp_currency_cost = MemInt32(208)

    spell_base = MemCppString(216)
    effects = MemCppVector(248, MemCppSharedPointer(0, SpellEffect(0)))

    magic_school_name = MemCppString(280)

    type_name = MemCppString(320)
    training_cost = MemInt32(352)
    accuracy = MemInt32(356)
    valid_target_spells = MemUInt32(360)

    pvp = MemBool(376)
    pve = MemBool(377)
    no_pvp_enchant = MemBool(378)
    no_pve_enchant = MemBool(379)
    battlegrounds_only = MemBool(380)
    treasure = MemBool(381)
    no_discard = MemBool(382)

    image_index = MemInt32(384)

    image_name = MemCppString(392)

    card_front = MemCppString(424)
    use_gloss = MemBool(456)
    cloaked = MemBool(457)
    caster_invisible = MemBool(458)
    booster_pack_icon = MemCppString(464)
    spell_source_type = MemEnum(496, SpellSourceType)
    leaves_play_when_cast = MemBool(500)

    cloaked_name = MemCppString(504)

    adjectives = MemCppString(544)

    description_trainer = MemCppString(584)
    description_combat_hud = MemCppString(616)
    display_index = MemInt32(648)
    hidden_from_effects_window = MemBool(652)
    ignore_charms = MemBool(653)
    always_fizzle = MemBool(654)

    spell_category = MemCppString(656)
    show_polymorphed_name = MemBool(688)
    skip_truncation = MemBool(689)

    max_copies = MemUInt32(692)
    level_restriction = MemInt32(696)
    delay_enchantment = MemBool(700)

    delay_enchantment_order = MemEnum(704, DelayOrder)

    previous_spell_name = MemCppString(712)
    ignore_dispel = MemBool(744)
    backrow_friendly = MemBool(745)
