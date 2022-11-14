from typing import List, Optional

from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memtypes import *
from .enums import PipAquiredByEnum
from .game_stats import GameStats
from .spell import Hand
from .play_deck import PlayDeck
from .spell_effect import SpellEffect


class CombatParticipant(PropertyClass):
    """
    Base class for CombatParticipants
    """

    @staticmethod
    def obj_size() -> int:
        return 842

    owner_id_full = MemUInt64(112)
    template_id_full = MemUInt64(120)
    is_player = MemBool(128)

    zone_id_full = MemUInt64(136)
    # TODO: look into what a team id is; i.e is it always the two ids
    team_id = MemUInt32(144)
    # TODO: turn this into an enum?
    primary_magic_school_id = MemUInt32(148)
    num_pips = MemUInt8(152)
    num_power_pips = MemUInt8(153)
    num_shadow_pips = MemUInt8(154)

    pips_suspended = MemBool(176)
    
    stunned = MemInt32(180)
    stunned_display = MemBool(184)

    confused = MemInt32(188)
    confusion_trigger = MemInt32(192)
    confusion_display = MemBool(196)
    confused_target = MemBool(197)
    untargetable = MemBool(198)

    untargetable_rounds = MemInt32(200)
    restricted_target = MemBool(204)
    exit_combat = MemBool(205)


    mindcontrolled = MemInt32(208)
    mindcontrolled_display = MemBool(212)

    original_team = MemInt32(216)
    clue = MemInt32(220)
    rounds_dead = MemInt32(224)
    aura_turn_length = MemInt32(228)
    polymorph_turn_length = MemInt32(232)
    player_health = MemInt32(236)
    max_player_health = MemInt32(240)
    hide_current_hp = MemBool(244)

    max_hand_size = MemInt32(248)

    saved_primary_magic_school_id = MemInt32(304)

    rotation = MemFloat32(332)
    radius = MemFloat32(336)
    subcircle = MemInt32(340)
    pvp = MemInt32(344)

    accuracy_bonus = MemFloat32(388)
    minion_sub_circle = MemInt32(392)
    is_minion = MemBool(396)

    is_monster = MemUInt32(400)

    polymorph_spell_template_id = MemUInt32(568)

    side = MemCppString(592)

    shadow_spells_disabled = MemBool(637)
    boss_mob = MemBool(638)
    hide_pvp_enemy_chat = MemBool(639)

    combat_trigger_ids = MemInt32(664)

    pet_combat_trigger = MemInt32(680)
    pet_combat_trigger_target = MemInt32(684)
    auto_pass = MemBool(688)
    vanish = MemBool(689)
    my_team_turn = MemBool(690)

    backlash = MemInt32(692)
    past_backlash = MemInt32(696)
    shadow_creature_level = MemInt32(700)
    past_shadow_creature_level = MemInt32(704)

    shadow_creature_level_count = MemInt32(712)

    rounds_since_shadow_pip = MemInt32(768)

    planning_phase_pip_aquired_type = MemEnum(PipAquiredByEnum, 784)

    shadow_pip_rate_threshold = MemFloat32(808)
    base_spell_damage = MemInt32(812)
    stat_damage = MemFloat32(816)
    stat_resist = MemFloat32(820)
    stat_pierce = MemFloat32(824)
    mob_level = MemInt32(828)
    player_time_updated = MemBool(832)
    player_time_eliminated = MemBool(833)


    # TODO: Make work
    # async def hand(self) -> Optional[DynamicHand]:
    #     addr = await self.read_value_from_offset(256, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicHand(self.hook_handler, addr)

    # async def saved_hand(self) -> Optional[DynamicHand]:
    #     addr = await self.read_value_from_offset(264, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicHand(self.hook_handler, addr)

    # async def play_deck(self) -> Optional[DynamicPlayDeck]:
    #     addr = await self.read_value_from_offset(272, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicPlayDeck(self.hook_handler, addr)

    # async def saved_play_deck(self) -> Optional[DynamicPlayDeck]:
    #     addr = await self.read_value_from_offset(280, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicPlayDeck(self.hook_handler, addr)

    # async def saved_game_stats(self) -> Optional[DynamicGameStats]:
    #     addr = await self.read_value_from_offset(288, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicGameStats(self.hook_handler, addr)

    # async def game_stats(self) -> Optional[DynamicGameStats]:
    #     addr = await self.read_value_from_offset(312, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicGameStats(self.hook_handler, addr)

    # # TODO: figure out what color is
    # # async def color(self) -> class Color:
    # #     return await self.read_value_from_offset(328, "class Color")
    # #
    # # async def write_color(self, color: class Color):
    # #     await self.write_value_to_offset(328, color, "class Color")

    # async def hanging_effects(self) -> List[DynamicSpellEffect]:
    #     hanging_effects = []
    #     for addr in await self.read_linked_list(408):
    #         hanging_effects.append(DynamicSpellEffect(self.hook_handler, addr))

    #     return hanging_effects

    # async def public_hanging_effects(self) -> List[DynamicSpellEffect]:
    #     hanging_effects = []
    #     for addr in await self.read_linked_list(424):
    #         hanging_effects.append(DynamicSpellEffect(self.hook_handler, addr))

    #     return hanging_effects

    # async def aura_effects(self) -> List[DynamicSpellEffect]:
    #     aura_effects = []
    #     for addr in await self.read_linked_list(440):
    #         aura_effects.append(DynamicSpellEffect(self.hook_handler, addr))

    #     return aura_effects

    # # TODO: add this class
    # # async def shadow_effects(self) -> class SharedPointer<class ShadowSpellTrackingData>:
    # #     return await self.read_value_from_offset(456, "class SharedPointer<class ShadowSpellTrackingData>")

    # async def shadow_spell_effects(self) -> List[DynamicSpellEffect]:
    #     shadow_spell_effects = []
    #     for addr in await self.read_linked_list(472):
    #         shadow_spell_effects.append(DynamicSpellEffect(self.hook_handler, addr))

    #     return shadow_spell_effects

    # async def death_activated_effects(self) -> List[DynamicSpellEffect]:
    #     death_activated_effects = []
    #     for addr in await self.read_shared_linked_list(504):
    #         death_activated_effects.append(DynamicSpellEffect(self.hook_handler, addr))

    #     return death_activated_effects

    # # note: these are actually DelaySpellEffects
    # async def delay_cast_effects(self) -> List[DynamicSpellEffect]:
    #     delay_cast_effects = []
    #     for addr in await self.read_linked_list(520):
    #         delay_cast_effects.append(DynamicSpellEffect(self.hook_handler, addr))

    #     return delay_cast_effects

    # async def intercept_effect(self) -> Optional[DynamicSpellEffect]:
    #     addr = await self.read_value_from_offset(736, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicSpellEffect(self.hook_handler, addr)

    # async def polymorph_effect(self) -> Optional[DynamicSpellEffect]:
    #     addr = await self.read_value_from_offset(792, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicSpellEffect(self.hook_handler, addr)