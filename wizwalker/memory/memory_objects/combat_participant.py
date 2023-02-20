from typing import List, Optional

from wizwalker.memory.memory_object import PropertyClass

from .enums import PipAquiredByEnum
from .game_stats import GameStats
from .pip_count import PipCount
from .play_deck import PlayDeck
from .spell import Hand
from .spell_effect import SpellEffect

from memonster.memtypes import *
from .memtypes import *


class CombatParticipant(PropertyClass):
    """
    Base class for CombatParticipants
    """
    owner_id_full = MemUInt64(112)
    template_id_full = MemUInt64(120)
    is_player = MemBool(128)

    zone_id_full = MemUInt64(136)
    # TODO: look into what a team id is; i.e is it always the two ids
    team_id = MemInt32(144)
    primary_magic_school_id = MemInt32(148)
    pip_count = MemPointer(152, PipCount)

    pips_suspended = MemBool(184)

    stunned = MemInt32(188)
    stunned_display = MemBool(192)

    confused = MemInt32(196)
    confusion_trigger = MemInt32(200)
    confusion_display = MemBool(204)
    confused_target = MemBool(205)
    untargetable = MemBool(206)

    untargetable_rounds = MemInt32(208)
    restricted_target = MemBool(212)
    exit_combat = MemBool(213)

    mindcontrolled = MemInt32(216)
    mindcontrolled_display = MemBool(220)

    original_team = MemInt32(224)
    clue = MemInt32(228)
    rounds_dead = MemInt32(232)
    aura_turn_length = MemInt32(236)
    polymorph_turn_length = MemInt32(240)
    player_health = MemInt32(244)
    max_player_health = MemInt32(248)
    hide_current_hp = MemBool(252)
    
    max_hand_size = MemInt32(256)

    hand = MemPointer(264, Hand(0))
    saved_hand = MemPointer(272, Hand(0))
    play_deck = MemPointer(280, PlayDeck(0))
    saved_play_deck = MemPointer(288, PlayDeck(0))

    saved_game_stats = MemPointer(296, GameStats(0))

    saved_primary_magic_school_id = MemInt32(312)

    game_stats = MemPointer(320, GameStats(0))

    rotation = MemFloat32(340)
    radius = MemFloat32(344)
    subcircle = MemInt32(348)
    pvp = MemBool(352)
    raid = MemBool(353)

    accuracy_bonus = MemFloat32(396)
    minion_sub_circle = MemInt32(400)
    is_minion = MemBool(404)

    # TODO: Why did WW have this as uint32? Check if this is correct
    is_monster = MemUInt32(408)

    hanging_effects = MemCppLinkedList(416, SpellEffect(0))
    public_hanging_effects = MemCppLinkedList(432, SpellEffect(0))
    aura_effects = MemCppLinkedList(448, SpellEffect(0))

    shadow_spell_effects = MemCppLinkedList(480, SpellEffect(0))

    death_activated_effects = MemCppLinkedList(512, MemCppSharedPointer(0, SpellEffect(0)))
    # note: these are actually DelaySpellEffects
    delay_cast_effects = MemCppLinkedList(528, SpellEffect(0))

    polymorph_spell_template_id = MemUInt32(576)

    side = MemCppString(600)

    shadow_spells_disabled = MemBool(672)
    boss_mob = MemBool(673)
    hide_pvp_enemy_chat = MemBool(674)

    combat_trigger_ids = MemInt32(696)

    pet_combat_trigger = MemInt32(712)
    pet_combat_trigger_target = MemInt32(716)

    auto_pass = MemBool(720)
    vanish = MemBool(721)
    my_team_turn = MemBool(722)

    backlash = MemInt32(724)
    past_backlash = MemInt32(728)
    shadow_creature_level = MemInt32(732)
    past_shadow_creature_level = MemInt32(736)

    shadow_creature_level_count = MemInt32(744)

    intercept_effect = MemPointer(768, SpellEffect(0))

    rounds_since_shadow_pip = MemInt32(800)

    planning_phase_pip_aquired_type = MemEnum(816, PipAquiredByEnum)

    polymorph_effect = MemPointer(192, SpellEffect(0))

    shadow_pip_rate_threshold = MemFloat32(840)
    base_spell_damage = MemInt32(844)
    stat_damage = MemFloat32(848)
    stat_resist = MemFloat32(852)
    stat_pierce = MemFloat32(856)
    mob_level = MemInt32(860)
    player_time_updated = MemBool(864)
    player_time_eliminated = MemBool(865)
