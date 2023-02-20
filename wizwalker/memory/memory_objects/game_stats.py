from typing import List

from wizwalker.memory.memory_object import DynamicMemoryObject, PropertyClass

from memonster import LazyType
from memonster.memtypes import *
from .memtypes import *


class GameStats(PropertyClass):
    async def max_hitpoints(self) -> int:
        """
        Client's max hitpoints; base + bonus
        """
        base = await self.base_hitpoints()
        bonus = await self.bonus_hitpoints()
        return base + bonus

    async def max_mana(self) -> int:
        """
        Clients's max mana; base + bonus
        """
        base = await self.base_mana()
        bonus = await self.bonus_mana()
        return base + bonus

    async def base_hitpoints(self) -> int:
        return await self.read_value_from_offset(80, "int")

    async def write_base_hitpoints(self, base_hitpoints: int):
        await self.write_value_to_offset(80, base_hitpoints, "int")

    async def base_mana(self) -> int:
        return await self.read_value_from_offset(84, "int")

    async def write_base_mana(self, base_mana: int):
        await self.write_value_to_offset(84, base_mana, "int")

    async def base_gold_pouch(self) -> int:
        return await self.read_value_from_offset(88, "int")

    async def write_base_gold_pouch(self, base_gold_pouch: int):
        await self.write_value_to_offset(88, base_gold_pouch, "int")

    async def base_event_currency1_pouch(self) -> int:
        return await self.read_value_from_offset(92, "int")

    async def write_base_event_currency1_pouch(self, base_event_currency1_pouch: int):
        await self.write_value_to_offset(92, base_event_currency1_pouch, "int")

    async def base_event_currency2_pouch(self) -> int:
        return await self.read_value_from_offset(96, "int")

    async def write_base_event_currency2_pouch(self, base_event_currency2_pouch: int):
        await self.write_value_to_offset(96, base_event_currency2_pouch, "int")

    async def base_pvp_currency_pouch(self) -> int:
        return await self.read_value_from_offset(100, "int")

    async def write_base_pvp_currency_pouch(self, base_pvp_currency_pouch: int):
        await self.write_value_to_offset(100, base_pvp_currency_pouch, "int")

    async def energy_max(self) -> int:
        return await self.read_value_from_offset(104, "int")

    async def write_energy_max(self, energy_max: int):
        await self.write_value_to_offset(104, energy_max, "int")

    async def current_hitpoints(self) -> int:
        return await self.read_value_from_offset(108, "int")

    async def write_current_hitpoints(self, current_hitpoints: int):
        await self.write_value_to_offset(108, current_hitpoints, "int")

    async def current_gold(self) -> int:
        return await self.read_value_from_offset(112, "int")

    async def write_current_gold(self, current_gold: int):
        await self.write_value_to_offset(112, current_gold, "int")

    async def current_event_currency1(self) -> int:
        return await self.read_value_from_offset(116, "int")

    async def write_current_event_currency1(self, current_event_currency1: int):
        await self.write_value_to_offset(116, current_event_currency1, "int")

    async def current_event_currency2(self) -> int:
        return await self.read_value_from_offset(120, "int")

    async def write_current_event_currency2(self, current_event_currency2: int):
        await self.write_value_to_offset(120, current_event_currency2, "int")

    async def current_pvp_currency(self) -> int:
        return await self.read_value_from_offset(124, "int")

    async def write_current_pvp_currency(self, current_pvp_currency: int):
        await self.write_value_to_offset(124, current_pvp_currency, "int")

    async def current_mana(self) -> int:
        return await self.read_value_from_offset(128, "int")

    async def write_current_mana(self, current_mana: int):
        await self.write_value_to_offset(128, current_mana, "int")

    async def current_arena_points(self) -> int:
        return await self.read_value_from_offset(132, "int")

    async def write_current_arena_points(self, current_arena_points: int):
        await self.write_value_to_offset(132, current_arena_points, "int")

    async def spell_charge_base(self) -> List[int]:
        return await self.read_dynamic_vector(136, "int")

    async def potion_max(self) -> float:
        return await self.read_value_from_offset(160, "float")

    async def write_potion_max(self, potion_max: float):
        await self.write_value_to_offset(160, potion_max, "float")

    async def potion_charge(self) -> float:
        return await self.read_value_from_offset(164, "float")

    async def write_potion_charge(self, potion_charge: float):
        await self.write_value_to_offset(164, potion_charge, "float")

    async def bonus_hitpoints(self) -> int:
        return await self.read_value_from_offset(216, "int")

    async def write_bonus_hitpoints(self, bonus_hitpoints: int):
        await self.write_value_to_offset(216, bonus_hitpoints, "int")

    async def bonus_mana(self) -> int:
        return await self.read_value_from_offset(220, "int")

    async def write_bonus_mana(self, bonus_mana: int):
        await self.write_value_to_offset(220, bonus_mana, "int")

    async def bonus_energy(self) -> int:
        return await self.read_value_from_offset(236, "int")

    async def write_bonus_energy(self, bonus_energy: int):
        await self.write_value_to_offset(236, bonus_energy, "int")

    async def critical_hit_percent_all(self) -> float:
        return await self.read_value_from_offset(240, "float")

    async def write_critical_hit_percent_all(self, critical_hit_percent_all: float):
        await self.write_value_to_offset(240, critical_hit_percent_all, "float")

    async def block_percent_all(self) -> float:
        return await self.read_value_from_offset(244, "float")

    async def write_block_percent_all(self, block_percent_all: float):
        await self.write_value_to_offset(244, block_percent_all, "float")

    async def critical_hit_rating_all(self) -> float:
        return await self.read_value_from_offset(248, "float")

    async def write_critical_hit_rating_all(self, critical_hit_rating_all: float):
        await self.write_value_to_offset(248, critical_hit_rating_all, "float")

    async def block_rating_all(self) -> float:
        return await self.read_value_from_offset(252, "float")

    async def write_block_rating_all(self, block_rating_all: float):
        await self.write_value_to_offset(252, block_rating_all, "float")

    async def reference_level(self) -> int:
        return await self.read_value_from_offset(316, "int")

    async def write_reference_level(self, reference_level: int):
        await self.write_value_to_offset(316, reference_level, "int")

    async def highest_character_level_on_account(self) -> int:
        return await self.read_value_from_offset(320, "int")

    async def write_highest_character_level_on_account(
        self, highest_character_level_on_account: int
    ):
        await self.write_value_to_offset(320, highest_character_level_on_account, "int")

    async def pet_act_chance(self) -> int:
        return await self.read_value_from_offset(328, "int")

    async def write_pet_act_chance(self, pet_act_chance: int):
        await self.write_value_to_offset(328, pet_act_chance, "int")

    async def dmg_bonus_percent(self) -> List[float]:
        return await self.read_dynamic_vector(336, "float")

    async def write_dmg_bonus_percent(self, dmg_bonus_percent: float):
        await self.write_value_to_offset(336, dmg_bonus_percent, "float")

    async def dmg_bonus_flat(self) -> List[float]:
        return await self.read_dynamic_vector(360, "float")

    async def write_dmg_bonus_flat(self, dmg_bonus_flat: float):
        await self.write_value_to_offset(360, dmg_bonus_flat, "float")

    async def acc_bonus_percent(self) -> List[float]:
        return await self.read_dynamic_vector(384, "float")

    async def write_acc_bonus_percent(self, acc_bonus_percent: float):
        await self.write_value_to_offset(384, acc_bonus_percent, "float")

    async def ap_bonus_percent(self) -> List[float]:
        return await self.read_dynamic_vector(408, "float")

    async def write_ap_bonus_percent(self, ap_bonus_percent: float):
        await self.write_value_to_offset(408, ap_bonus_percent, "float")

    async def dmg_reduce_percent(self) -> List[float]:
        return await self.read_dynamic_vector(432, "float")

    async def write_dmg_reduce_percent(self, dmg_reduce_percent: float):
        await self.write_value_to_offset(432, dmg_reduce_percent, "float")

    async def dmg_reduce_flat(self) -> List[float]:
        return await self.read_dynamic_vector(456, "float")

    async def write_dmg_reduce_flat(self, dmg_reduce_flat: float):
        await self.write_value_to_offset(456, dmg_reduce_flat, "float")

    async def acc_reduce_percent(self) -> List[float]:
        return await self.read_dynamic_vector(480, "float")

    async def write_acc_reduce_percent(self, acc_reduce_percent: float):
        await self.write_value_to_offset(480, acc_reduce_percent, "float")

    async def heal_bonus_percent(self) -> List[float]:
        return await self.read_dynamic_vector(504, "float")

    async def write_heal_bonus_percent(self, heal_bonus_percent: float):
        await self.write_value_to_offset(504, heal_bonus_percent, "float")

    async def heal_inc_bonus_percent(self) -> List[float]:
        return await self.read_dynamic_vector(528, "float")

    async def write_heal_inc_bonus_percent(self, heal_inc_bonus_percent: float):
        await self.write_value_to_offset(528, heal_inc_bonus_percent, "float")

    async def spell_charge_bonus(self) -> List[int]:
        return await self.read_dynamic_vector(576, "int")

    async def write_spell_charge_bonus(self, spell_charge_bonus: int):
        await self.write_value_to_offset(576, spell_charge_bonus, "int")

    async def dmg_bonus_percent_all(self) -> float:
        return await self.read_value_from_offset(696, "float")

    async def write_dmg_bonus_percent_all(self, dmg_bonus_percent_all: float):
        await self.write_value_to_offset(696, dmg_bonus_percent_all, "float")

    async def dmg_bonus_flat_all(self) -> float:
        return await self.read_value_from_offset(700, "float")

    async def write_dmg_bonus_flat_all(self, dmg_bonus_flat_all: float):
        await self.write_value_to_offset(700, dmg_bonus_flat_all, "float")

    async def acc_bonus_percent_all(self) -> float:
        return await self.read_value_from_offset(704, "float")

    async def write_acc_bonus_percent_all(self, acc_bonus_percent_all: float):
        await self.write_value_to_offset(704, acc_bonus_percent_all, "float")

    async def ap_bonus_percent_all(self) -> float:
        return await self.read_value_from_offset(708, "float")

    async def write_ap_bonus_percent_all(self, ap_bonus_percent_all: float):
        await self.write_value_to_offset(708, ap_bonus_percent_all, "float")

    async def dmg_reduce_percent_all(self) -> float:
        return await self.read_value_from_offset(712, "float")

    async def write_dmg_reduce_percent_all(self, dmg_reduce_percent_all: float):
        await self.write_value_to_offset(712, dmg_reduce_percent_all, "float")

    async def dmg_reduce_flat_all(self) -> float:
        return await self.read_value_from_offset(716, "float")

    async def write_dmg_reduce_flat_all(self, dmg_reduce_flat_all: float):
        await self.write_value_to_offset(716, dmg_reduce_flat_all, "float")

    async def acc_reduce_percent_all(self) -> float:
        return await self.read_value_from_offset(720, "float")

    async def write_acc_reduce_percent_all(self, acc_reduce_percent_all: float):
        await self.write_value_to_offset(720, acc_reduce_percent_all, "float")

    async def heal_bonus_percent_all(self) -> float:
        return await self.read_value_from_offset(724, "float")

    async def write_heal_bonus_percent_all(self, heal_bonus_percent_all: float):
        await self.write_value_to_offset(724, heal_bonus_percent_all, "float")

    async def heal_inc_bonus_percent_all(self) -> float:
        return await self.read_value_from_offset(728, "float")

    async def write_heal_inc_bonus_percent_all(self, heal_inc_bonus_percent_all: float):
        await self.write_value_to_offset(728, heal_inc_bonus_percent_all, "float")

    async def spell_charge_bonus_all(self) -> int:
        return await self.read_value_from_offset(736, "int")

    async def write_spell_charge_bonus_all(self, spell_charge_bonus_all: int):
        await self.write_value_to_offset(736, spell_charge_bonus_all, "int")

    async def power_pip_base(self) -> float:
        return await self.read_value_from_offset(740, "float")

    async def write_power_pip_base(self, power_pip_base: float):
        await self.write_value_to_offset(740, power_pip_base, "float")

    async def power_pip_bonus_percent_all(self) -> float:
        return await self.read_value_from_offset(776, "float")

    async def write_power_pip_bonus_percent_all(
        self, power_pip_bonus_percent_all: float
    ):
        await self.write_value_to_offset(776, power_pip_bonus_percent_all, "float")

    async def xp_percent_increase(self) -> float:
        return await self.read_value_from_offset(784, "float")

    async def write_xp_percent_increase(self, xp_percent_increase: float):
        await self.write_value_to_offset(784, xp_percent_increase, "float")

    async def critical_hit_percent_by_school(self) -> List[float]:
        return await self.read_dynamic_vector(600, "float")

    async def write_critical_hit_percent_by_school(
        self, critical_hit_percent_by_school: float
    ):
        await self.write_value_to_offset(600, critical_hit_percent_by_school, "float")

    async def block_percent_by_school(self) -> List[float]:
        return await self.read_dynamic_vector(624, "float")

    async def write_block_percent_by_school(self, block_percent_by_school: float):
        await self.write_value_to_offset(624, block_percent_by_school, "float")

    async def critical_hit_rating_by_school(self) -> List[float]:
        return await self.read_dynamic_vector(648, "float")

    async def write_critical_hit_rating_by_school(
        self, critical_hit_rating_by_school: float
    ):
        await self.write_value_to_offset(648, critical_hit_rating_by_school, "float")


    pip_conversion_rating_per_school = MemFloat32(256)

    pip_conversion_rating_all = MemFloat32(280)

    pip_conversion_percent_per_school = MemFloat32(288)

    pip_conversion_percent_all = MemFloat32(312)

    highest_character_world_on_account = MemInt32(324)

    fishing_luck_bonus_percent = MemFloat32(552)

    block_rating_by_school = MemCppVector(672, MemFloat32(0))

    fishing_luck_bonus_percent_all = MemFloat32(732)

    pip_conversion_base_all_schools = MemInt32(744)

    pip_conversion_base_per_school = MemInt32(752)

    shadow_pip_bonus_percent = MemFloat32(780)

    wisp_bonus_percent = MemFloat32(804)

    balance_mastery = MemInt32(812)
    death_mastery = MemInt32(816)
    fire_mastery = MemInt32(820)
    ice_mastery = MemInt32(824)
    life_mastery = MemInt32(828)
    myth_mastery = MemInt32(832)
    storm_mastery = MemInt32(836)
    maximum_number_of_islands = MemInt32(840)
    gardening_level = MemUInt8(844)

    gardening_xp = MemInt32(848)
    invisible_to_friends = MemBool(852)
    show_item_lock = MemBool(853)
    quest_finder_enabled = MemBool(854)

    buddy_list_limit = MemInt32(856)
    stun_resistance_percent = MemFloat32(860)
    dont_allow_friend_finder_codes = MemBool(864)

    shadow_pip_max = MemInt32(868)

    shadow_magic_unlocked = MemBool(872)
    fishing_level = MemUInt8(873)

    fishing_xp = MemInt32(876)
    subscriber_benefit_flags = MemUInt32(880)
    elixir_benefit_flags = MemUInt32(884)
    monster_magic_level = MemUInt8(888)

    monster_magic_xp = MemInt32(892)
    player_chat_channel_is_public = MemBool(896)

    extra_inventory_space = MemInt32(900)
    remember_last_realm = MemBool(904)
    new_spellbook_layout_warning = MemBool(905)

    purchased_custom_emotes1 = MemUInt32(908)
    purchased_custom_teleport_effects1 = MemUInt32(912)
    equipped_teleport_effect = MemUInt32(916)
    highest_world1_id = MemUInt32(920)
    highest_world2_id = MemUInt32(924)
    active_class_projects_list = MemUInt32(928)

    disabled_item_slot_ids = MemUInt32(944)

    adventure_power_cooldown_time = MemUInt32(960)
    purchased_custom_emotes2 = MemUInt32(964)
    purchased_custom_teleport_effects2 = MemUInt32(968)
    purchased_custom_emotes3 = MemUInt32(972)
    purchased_custom_teleport_effects3 = MemUInt32(976)
    shadow_pip_rating = MemFloat32(980)
    bonus_shadow_pip_rating = MemFloat32(984)
    shadow_pip_rate_accumulated = MemFloat32(988)
    shadow_pip_rate_threshold = MemFloat32(992)
    shadow_pip_rate_percentage = MemInt32(996)
    friendly_player = MemBool(1000)

    emoji_skin_tone = MemInt32(1004)
    show_pvp_option = MemUInt32(1008)
    favorite_slot = MemInt32(1012)
    cantrip_level = MemUInt8(1016)

    cantrip_xp = MemInt32(1020)
    base_archmastery_rating = MemFloat32(1024)
    bonus_archmastery_rating = MemFloat32(1028)


class CurrentGameStats(GameStats):
    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_player_stat_base()
