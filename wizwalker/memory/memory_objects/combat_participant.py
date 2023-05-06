from typing import List, Optional

from wizwalker.memory.memory_object import DynamicMemoryObject, PropertyClass

from .enums import PipAquiredByEnum
from .game_stats import DynamicGameStats
from .pip_count import DynamicPipCount
from .play_deck import DynamicPlayDeck
from .spell import DynamicHand
from .spell_effect import DynamicSpellEffect


class CombatParticipant(PropertyClass):
    """
    Base class for CombatParticipants
    """

    def read_base_address(self) -> int:
        raise NotImplementedError()

    async def owner_id_full(self) -> int:
        """
        This combat participant's owner id
        """
        return await self.read_value_from_offset(112, "unsigned long long")

    async def write_owner_id_full(self, owner_id_full: int):
        """
        Write this combat participant's owner id

        Args:
            owner_id_full: The owner id to write
        """
        await self.write_value_to_offset(112, owner_id_full, "unsigned long long")

    async def template_id_full(self) -> int:
        """
        This combat participant's template id
        """
        return await self.read_value_from_offset(120, "unsigned long long")

    async def write_template_id_full(self, template_id_full: int):
        """
        Write this combat participant's template id

        Args:
            template_id_full: The template id to write
        """
        await self.write_value_to_offset(120, template_id_full, "unsigned long long")

    async def is_player(self) -> bool:
        """
        If this combat participant is a player
        """
        return await self.read_value_from_offset(128, "bool")

    async def write_is_player(self, is_player: bool):
        """
        Write if this combat participant is a player

        Args:
            is_player: The bool to write
        """
        await self.write_value_to_offset(128, is_player, "bool")

    async def zone_id_full(self) -> int:
        """
        This combat participant's zone id
        """
        return await self.read_value_from_offset(136, "unsigned long long")

    async def write_zone_id_full(self, zone_id_full: int):
        """
        Write this combat participant's zone id

        Args:
            zone_id_full: The zone id to write
        """
        await self.write_value_to_offset(136, zone_id_full, "unsigned long long")

    # TODO: look into what a team id is; i.e is it always the two ids
    async def team_id(self) -> int:
        """
        This combat participant's team id
        """
        return await self.read_value_from_offset(144, "int")

    async def write_team_id(self, team_id: int):
        """
        Write this combat participant's team id

        Args:
            team_id: The team id to write
        """
        await self.write_value_to_offset(144, team_id, "int")

    # TODO: turn this into an enum?
    async def primary_magic_school_id(self) -> int:
        """
        This combat participant's primary school id

        Notes:
            This is a template id
        """
        return await self.read_value_from_offset(148, "int")

    async def write_primary_magic_school_id(self, primary_magic_school_id: int):
        """
        Write this combat participant's primate school id

        Args:
            primary_magic_school_id: The school id to write

        Notes:
            this is a template id
        """
        await self.write_value_to_offset(148, primary_magic_school_id, "int")

    async def pip_count(self) -> Optional[DynamicPipCount]:
        addr = await self.read_value_from_offset(152, "long long")

        if addr == 0:
            return None

        return DynamicPipCount(self.hook_handler, addr)

    async def num_pips(self) -> int:
        """
        The number of pips this combat participant has
        """
        pipcount = await self.pip_count()
        return await pipcount.generic_pips()

    async def write_num_pips(self, num_pips: int):
        """
        Write this participant's pip number

        Args:
            num_pips: The pip number to write
        """
        pipcount = await self.pip_count()
        return await pipcount.write_generic_pips(num_pips)

    async def num_power_pips(self) -> int:
        """
        The number of power pips this combat participant has
        """
        pipcount = await self.pip_count()
        return await pipcount.power_pips()

    async def write_num_power_pips(self, num_power_pips: int):
        """
        Write the number of power pips this combat participant has

        Args:
            num_power_pips: The power pip number to write
        """
        pipcount = await self.pip_count()
        return await pipcount.write_power_pips(num_power_pips)

    async def num_shadow_pips(self) -> int:
        """
        The number of shadow pips this combat participant has
        """
        pipcount = await self.pip_count()
        return await pipcount.shadow_pips()

    async def write_num_shadow_pips(self, num_shadow_pips: int):
        """
        Write the number of shadow pips this combat participant has

        Args:
            num_shadow_pips: The power pip number to write
        """
        pipcount = await self.pip_count()
        return await pipcount.write_shadow_pips(num_shadow_pips)

    async def pips_suspended(self) -> bool:
        """
        If this participant's pips are suspended
        """
        return await self.read_value_from_offset(184, "bool")

    async def write_pips_suspended(self, pips_suspended: bool):
        """
        Write if this participant's pips are suspended

        Args:
            pips_suspended: bool if pips are suspended
        """
        await self.write_value_to_offset(184, pips_suspended, "bool")

    # TODO: finish docs
    async def stunned(self) -> int:
        return await self.read_value_from_offset(188, "int")

    async def write_stunned(self, stunned: int):
        await self.write_value_to_offset(188, stunned, "int")

    async def mindcontrolled(self) -> int:
        return await self.read_value_from_offset(216, "int")

    async def write_mindcontrolled(self, mindcontrolled: int):
        await self.write_value_to_offset(216, mindcontrolled, "int")

    async def original_team(self) -> int:
        return await self.read_value_from_offset(224, "int")

    async def write_original_team(self, original_team: int):
        await self.write_value_to_offset(224, original_team, "int")

    async def aura_turn_length(self) -> int:
        return await self.read_value_from_offset(236, "int")

    async def write_aura_turn_length(self, n_aura_turn_length: int):
        await self.write_value_to_offset(236, n_aura_turn_length, "int")

    async def clue(self) -> int:
        return await self.read_value_from_offset(228, "int")

    async def write_clue(self, clue: int):
        await self.write_value_to_offset(228, clue, "int")

    async def rounds_dead(self) -> int:
        return await self.read_value_from_offset(232, "int")

    async def write_rounds_dead(self, rounds_dead: int):
        await self.write_value_to_offset(232, rounds_dead, "int")

    async def polymorph_turn_length(self) -> int:
        return await self.read_value_from_offset(240, "int")

    async def write_polymorph_turn_length(self, n_polymorph_turn_length: int):
        await self.write_value_to_offset(240, n_polymorph_turn_length, "int")

    async def player_health(self) -> int:
        return await self.read_value_from_offset(244, "int")

    async def write_player_health(self, player_health: int):
        await self.write_value_to_offset(244, player_health, "int")

    async def max_player_health(self) -> int:
        return await self.read_value_from_offset(248, "int")

    async def write_max_player_health(self, max_player_health: int):
        await self.write_value_to_offset(248, max_player_health, "int")

    async def hide_current_hp(self) -> bool:
        return await self.read_value_from_offset(252, "bool")

    async def write_hide_current_hp(self, _hide_current_h_p: bool):
        await self.write_value_to_offset(252, _hide_current_h_p, "bool")

    async def max_hand_size(self) -> int:
        return await self.read_value_from_offset(256, "int")

    async def write_max_hand_size(self, max_hand_size: int):
        await self.write_value_to_offset(256, max_hand_size, "int")

    async def hand(self) -> Optional[DynamicHand]:
        addr = await self.read_value_from_offset(264, "long long")

        if addr == 0:
            return None

        return DynamicHand(self.hook_handler, addr)

    async def saved_hand(self) -> Optional[DynamicHand]:
        addr = await self.read_value_from_offset(272, "long long")

        if addr == 0:
            return None

        return DynamicHand(self.hook_handler, addr)

    async def play_deck(self) -> Optional[DynamicPlayDeck]:
        addr = await self.read_value_from_offset(280, "long long")

        if addr == 0:
            return None

        return DynamicPlayDeck(self.hook_handler, addr)

    async def saved_play_deck(self) -> Optional[DynamicPlayDeck]:
        addr = await self.read_value_from_offset(288, "long long")

        if addr == 0:
            return None

        return DynamicPlayDeck(self.hook_handler, addr)

    async def saved_game_stats(self) -> Optional[DynamicGameStats]:
        addr = await self.read_value_from_offset(296, "long long")

        if addr == 0:
            return None

        return DynamicGameStats(self.hook_handler, addr)

    async def saved_primary_magic_school_id(self) -> int:
        return await self.read_value_from_offset(312, "int")

    async def write_saved_primary_magic_school_id(
        self, saved_primary_magic_school_id: int
    ):
        await self.write_value_to_offset(312, saved_primary_magic_school_id, "int")

    async def game_stats(self) -> Optional[DynamicGameStats]:
        addr = await self.read_value_from_offset(320, "long long")

        if addr == 0:
            return None

        return DynamicGameStats(self.hook_handler, addr)

    # TODO: figure out what color is
    # async def color(self) -> class Color:
    #     return await self.read_value_from_offset(328, "class Color")
    #
    # async def write_color(self, color: class Color):
    #     await self.write_value_to_offset(328, color, "class Color")

    async def rotation(self) -> float:
        return await self.read_value_from_offset(340, "float")

    async def write_rotation(self, rotation: float):
        await self.write_value_to_offset(340, rotation, "float")

    async def radius(self) -> float:
        return await self.read_value_from_offset(344, "float")

    async def write_radius(self, radius: float):
        await self.write_value_to_offset(344, radius, "float")

    async def subcircle(self) -> int:
        return await self.read_value_from_offset(348, "int")

    async def write_subcircle(self, subcircle: int):
        await self.write_value_to_offset(348, subcircle, "int")

    async def pvp(self) -> bool:
        return await self.read_value_from_offset(352, "bool")

    async def write_pvp(self, pvp: bool):
        await self.write_value_to_offset(352, pvp, "bool")

    async def raid(self) -> bool:
        return await self.read_value_from_offset(353, "bool")

    async def write_raid(self, raid: int):
        await self.write_value_to_offset(353, raid, "bool")

    # TODO: add class for this
    # async def dynamic_symbol(self):
    #   return await self.read_value_from_offset(356, "enum DynamicSigilSymbol"")

    async def accuracy_bonus(self) -> float:
        return await self.read_value_from_offset(396, "float")

    async def write_accuracy_bonus(self, accuracy_bonus: float):
        await self.write_value_to_offset(396, accuracy_bonus, "float")

    async def minion_sub_circle(self) -> int:
        return await self.read_value_from_offset(400, "int")

    async def write_minion_sub_circle(self, minion_sub_circle: int):
        await self.write_value_to_offset(400, minion_sub_circle, "int")

    async def is_minion(self) -> bool:
        return await self.read_value_from_offset(404, "bool")

    async def write_is_minion(self, is_minion: bool):
        await self.write_value_to_offset(404, is_minion, "bool")

    async def hanging_effects(self) -> List[DynamicSpellEffect]:
        hanging_effects = []
        for addr in await self.read_linked_list(416):
            hanging_effects.append(DynamicSpellEffect(self.hook_handler, addr))

        return hanging_effects

    async def public_hanging_effects(self) -> List[DynamicSpellEffect]:
        hanging_effects = []
        for addr in await self.read_linked_list(432):
            hanging_effects.append(DynamicSpellEffect(self.hook_handler, addr))

        return hanging_effects

    async def aura_effects(self) -> List[DynamicSpellEffect]:
        aura_effects = []
        for addr in await self.read_linked_list(448):
            aura_effects.append(DynamicSpellEffect(self.hook_handler, addr))

        return aura_effects

    # TODO: add this class
    # async def shadow_effects(self) -> class SharedPointer<class ShadowSpellTrackingData>:
    #     return await self.read_value_from_offset(464, "class SharedPointer<class ShadowSpellTrackingData>")

    async def shadow_spell_effects(self) -> List[DynamicSpellEffect]:
        shadow_spell_effects = []
        for addr in await self.read_linked_list(480):
            shadow_spell_effects.append(DynamicSpellEffect(self.hook_handler, addr))

        return shadow_spell_effects

    async def death_activated_effects(self) -> List[DynamicSpellEffect]:
        death_activated_effects = []
        for addr in await self.read_shared_linked_list(512):
            death_activated_effects.append(DynamicSpellEffect(self.hook_handler, addr))

        return death_activated_effects

    # note: these are actually DelaySpellEffects
    async def delay_cast_effects(self) -> List[DynamicSpellEffect]:
        delay_cast_effects = []
        for addr in await self.read_linked_list(528):
            delay_cast_effects.append(DynamicSpellEffect(self.hook_handler, addr))

        return delay_cast_effects

    async def polymorph_spell_template_id(self) -> int:
        return await self.read_value_from_offset(576, "unsigned int")

    async def write_polymorph_spell_template_id(self, polymorph_spell_template_id: int):
        await self.write_value_to_offset(576, polymorph_spell_template_id, "unsigned int")

    async def side(self) -> str:
        return await self.read_string_from_offset(600)

    async def write_side(self, side: str):
        await self.write_string_to_offset(600, side)

    async def shadow_spells_disabled(self) -> bool:
        return await self.read_value_from_offset(672, "bool")

    async def write_shadow_spells_disabled(self, shadow_spells_disabled: bool):
        await self.write_value_to_offset(672, shadow_spells_disabled, "bool")

    async def boss_mob(self) -> bool:
        return await self.read_value_from_offset(673, "bool")

    async def write_boss_mob(self, boss_mob: bool):
        await self.write_value_to_offset(673, boss_mob, "bool")

    async def hide_pvp_enemy_chat(self) -> bool:
        return await self.read_value_from_offset(674, "bool")

    async def write_hide_pvp_enemy_chat(self, hide_pvp_enemy_chat: bool):
        await self.write_value_to_offset(674, hide_pvp_enemy_chat, "bool")

    async def combat_trigger_ids(self) -> int:
        return await self.read_value_from_offset(696, "int")

    async def write_combat_trigger_ids(self, combat_trigger_ids: int):
        await self.write_value_to_offset(696, combat_trigger_ids, "int")

    async def backlash(self) -> int:
        return await self.read_value_from_offset(724, "int")

    async def write_backlash(self, backlash: int):
        await self.write_value_to_offset(724, backlash, "int")

    async def past_backlash(self) -> int:
        return await self.read_value_from_offset(728, "int")

    async def write_past_backlash(self, past_backlash: int):
        await self.write_value_to_offset(728, past_backlash, "int")

    async def shadow_creature_level(self) -> int:
        return await self.read_value_from_offset(732, "int")

    async def write_shadow_creature_level(self, shadow_creature_level: int):
        await self.write_value_to_offset(732, shadow_creature_level, "int")

    async def past_shadow_creature_level(self) -> int:
        return await self.read_value_from_offset(736, "int")

    async def write_past_shadow_creature_level(self, past_shadow_creature_level: int):
        await self.write_value_to_offset(736, past_shadow_creature_level, "int")

    async def shadow_creature_level_count(self) -> int:
        return await self.read_value_from_offset(744, "int")

    async def write_shadow_creature_level_count(self, shadow_creature_level_count: int):
        await self.write_value_to_offset(744, shadow_creature_level_count, "int")

    async def intercept_effect(self) -> Optional[DynamicSpellEffect]:
        addr = await self.read_value_from_offset(768, "long long")

        if addr == 0:
            return None

        return DynamicSpellEffect(self.hook_handler, addr)

    async def rounds_since_shadow_pip(self) -> int:
        return await self.read_value_from_offset(800, "int")

    async def write_rounds_since_shadow_pip(self, rounds_since_shadow_pip: int):
        await self.write_value_to_offset(800, rounds_since_shadow_pip, "int")

    async def polymorph_effect(self) -> Optional[DynamicSpellEffect]:
        addr = await self.read_value_from_offset(824, "long long")

        if addr == 0:
            return None

        return DynamicSpellEffect(self.hook_handler, addr)

    async def confused(self) -> int:
        return await self.read_value_from_offset(196, "int")

    async def write_confused(self, confused: int):
        await self.write_value_to_offset(196, confused, "int")

    async def confusion_trigger(self) -> int:
        return await self.read_value_from_offset(200, "int")

    async def write_confusion_trigger(self, confusion_trigger: int):
        await self.write_value_to_offset(200, confusion_trigger, "int")

    async def confusion_display(self) -> bool:
        return await self.read_value_from_offset(204, "bool")

    async def write_confusion_display(self, confusion_display: bool):
        await self.write_value_to_offset(204, confusion_display, "bool")

    async def confused_target(self) -> bool:
        return await self.read_value_from_offset(205, "bool")

    async def write_confused_target(self, confused_target: bool):
        await self.write_value_to_offset(205, confused_target, "bool")

    async def untargetable(self) -> bool:
        return await self.read_value_from_offset(206, "bool")

    async def write_untargetable(self, untargetable: bool):
        await self.write_value_to_offset(206, untargetable, "bool")

    async def untargetable_rounds(self) -> int:
        return await self.read_value_from_offset(208, "int")

    async def write_untargetable_rounds(self, untargetable_rounds: int):
        await self.write_value_to_offset(208, untargetable_rounds, "int")

    async def restricted_target(self) -> bool:
        return await self.read_value_from_offset(212, "bool")

    async def write_restricted_target(self, restricted_target: bool):
        await self.write_value_to_offset(212, restricted_target, "bool")

    async def exit_combat(self) -> bool:
        return await self.read_value_from_offset(213, "bool")

    async def write_exit_combat(self, exit_combat: bool):
        await self.write_value_to_offset(213, exit_combat, "bool")

    async def stunned_display(self) -> bool:
        return await self.read_value_from_offset(192, "bool")

    async def write_stunned_display(self, stunned_display: bool):
        await self.write_value_to_offset(192, stunned_display, "bool")

    async def mindcontrolled_display(self) -> bool:
        return await self.read_value_from_offset(220, "bool")

    async def write_mindcontrolled_display(self, mindcontrolled_display: bool):
        await self.write_value_to_offset(220, mindcontrolled_display, "bool")

    async def auto_pass(self) -> bool:
        return await self.read_value_from_offset(720, "bool")

    async def write_auto_pass(self, auto_pass: bool):
        await self.write_value_to_offset(720, auto_pass, "bool")

    async def vanish(self) -> bool:
        return await self.read_value_from_offset(721, "bool")

    async def write_vanish(self, vanish: bool):
        await self.write_value_to_offset(721, vanish, "bool")

    async def my_team_turn(self) -> bool:
        return await self.read_value_from_offset(722, "bool")

    async def write_my_team_turn(self, my_team_turn: bool):
        await self.write_value_to_offset(722, my_team_turn, "bool")

    async def planning_phase_pip_aquired_type(self) -> PipAquiredByEnum:
        return await self.read_enum(816, PipAquiredByEnum)

    async def write_planning_phase_pip_aquired_type(
        self, planning_phase_pip_aquired_type: PipAquiredByEnum
    ):
        await self.write_enum(816, planning_phase_pip_aquired_type)

    # async def cheat_settings(self) -> class SharedPointer<class CombatCheatSettings>:
    #     return await self.read_value_from_offset(96, "class SharedPointer<class CombatCheatSettings>")

    async def is_monster(self) -> int:
        return await self.read_value_from_offset(408, "unsigned int")

    async def write_is_monster(self, is_monster: int):
        await self.write_value_to_offset(408, is_monster, "unsigned int")

    # async def weapon_nif_sound_list(self) -> class SharedPointer<class SpellNifSoundOverride>:
    #     return await self.read_value_from_offset(80, "class SharedPointer<class SpellNifSoundOverride>")

    async def pet_combat_trigger(self) -> int:
        return await self.read_value_from_offset(712, "int")

    async def write_pet_combat_trigger(self, pet_combat_trigger: int):
        await self.write_value_to_offset(712, pet_combat_trigger, "int")

    async def pet_combat_trigger_target(self) -> int:
        return await self.read_value_from_offset(716, "int")

    async def write_pet_combat_trigger_target(self, pet_combat_trigger_target: int):
        await self.write_value_to_offset(716, pet_combat_trigger_target, "int")

    async def shadow_pip_rate_threshold(self) -> float:
        return await self.read_value_from_offset(840, "float")

    async def write_shadow_pip_rate_threshold(self, shadow_pip_rate_threshold: float):
        await self.write_value_to_offset(840, shadow_pip_rate_threshold, "float")

    async def base_spell_damage(self) -> int:
        return await self.read_value_from_offset(844, "int")

    async def write_base_spell_damage(self, base_spell_damage: int):
        await self.write_value_to_offset(844, base_spell_damage, "int")

    async def stat_damage(self) -> float:
        return await self.read_value_from_offset(848, "float")

    async def write_stat_damage(self, stat_damage: float):
        await self.write_value_to_offset(848, stat_damage, "float")

    async def stat_resist(self) -> float:
        return await self.read_value_from_offset(852, "float")

    async def write_stat_resist(self, stat_resist: float):
        await self.write_value_to_offset(852, stat_resist, "float")

    async def stat_pierce(self) -> float:
        return await self.read_value_from_offset(856, "float")

    async def write_stat_pierce(self, stat_pierce: float):
        await self.write_value_to_offset(856, stat_pierce, "float")

    async def mob_level(self) -> int:
        return await self.read_value_from_offset(860, "int")

    async def write_mob_level(self, mob_level: int):
        await self.write_value_to_offset(860, mob_level, "int")

    async def player_time_updated(self) -> bool:
        return await self.read_value_from_offset(864, "bool")

    async def write_player_time_updated(self, player_time_updated: bool):
        await self.write_value_to_offset(864, player_time_updated, "bool")

    async def player_time_eliminated(self) -> bool:
        return await self.read_value_from_offset(865, "bool")

    async def player_time_warning(self):
        await self.read_value_from_offset(866, "bool")
    
    async def write_player_time_warning(self, player_time_warning: bool):
        await self.write_value_to_offset(866, player_time_warning, "bool")

    async def deck_fullness(self):
        await self.read_value_from_offset(868, "float")
    
    async def write_deck_fullness(self, deck_fullness: float):
        await self.write_value_to_offset(868, deck_fullness, "float")
    
    async def archmastery_points(self):
        await self.read_value_from_offset(872, "float")
    
    async def write_archmastery_points(self, archmastery_points: float):
        await self.write_value_to_offset(872, archmastery_points, "float")

    async def max_archmastery_points(self):
        await self.read_value_from_offset(876, "float")
    
    async def write_max_archmastery_points(self, max_archmastery_points: float):
        await self.write_value_to_offset(876, max_archmastery_points, "float")
        
    async def archmastery_school(self):
        await self.read_value_from_offset(880, "unsigned int")
    
    async def write_archmastery_school(self, archmastery_school: int):
        await self.write_value_to_offset(880, archmastery_school, "unsigned int")
        
    async def archmastery_flags(self):
        await self.read_value_from_offset(884, "unsigned int")
    
    async def write_archmastery_flags(self, archmastery_flags: int):
        await self.write_value_to_offset(884, archmastery_flags, "unsigned int")

class DynamicCombatParticipant(DynamicMemoryObject, CombatParticipant):
    pass