from typing import List

from wizwalker.memory import memanagers
from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memonster.memtypes import *


class GameStats(PropertyClass):
    async def read_base_address(self) -> int:
        raise NotImplementedError()

    def max_hitpoints(self) -> int:
        """
        Client's max hitpoints; base + bonus
        """
        return self.base_hitpoints.read() + self.bonus_hitpoints.read()

    def max_mana(self) -> int:
        """
        Clients's max mana; base + bonus
        """
        return self.base_mana.read() + self.bonus_mana.read()

    base_hitpoints = MemInt32(80)
    base_mana = MemInt32(84)
    base_gold_pouch = MemInt32(88)
    base_event_currency1_pouch = MemInt32(92)
    base_event_currency2_pouch = MemInt32(96)
    base_pvp_currency_pouch = MemInt32(100)
    energy_max = MemInt32(104)
    current_hitpoints = MemInt32(108)
    current_gold = MemInt32(112)
    current_event_currency1 = MemInt32(116)
    current_event_currency2 = MemInt32(120)
    current_pvp_currency = MemInt32(124)
    current_mana = MemInt32(128)
    current_arena_points = MemInt32(132)

    potion_max = MemFloat32(160)
    potion_charge = MemFloat32(164)

    bonus_hitpoints = MemInt32(216)
    bonus_mana = MemInt32(220)

    bonus_energy = MemInt32(236)
    critical_hit_percent_all = MemFloat32(240)
    block_percent_all = MemFloat32(244)
    critical_hit_rating_all = MemFloat32(248)
    block_rating_all = MemFloat32(252)

    pip_conversion_rating_all = MemFloat32(280)

    pip_conversion_percent_all = MemFloat32(312)
    reference_level = MemInt32(316)
    highest_character_level_on_account = MemInt32(320)
    pet_act_chance = MemInt32(324)

    dmg_bonus_percent_all = MemFloat32(688)
    dmg_bonus_flat_all = MemFloat32(692)
    acc_bonus_percent_all = MemFloat32(696)
    ap_bonus_percent_all = MemFloat32(700)
    dmg_reduce_percent_all = MemFloat32(704)
    dmg_reduce_flat_all = MemFloat32(708)
    acc_reduce_percent_all = MemFloat32(712)
    heal_bonus_percent_all = MemFloat32(716)
    heal_inc_bonus_percent_all = MemFloat32(720)
    fishing_luck_bonus_percent_all = MemFloat32(724)
    spell_charge_bonus_all = MemInt32(728)
    power_pip_base = MemFloat32(732)
    pip_conversion_base_all_schools = MemInt32(736)

    power_pip_bonus_percent_all = MemFloat32(768)
    shadow_pip_bonus_percent = MemFloat32(772)
    xp_percent_increase = MemFloat32(776)

    wisp_bonus_percent = MemFloat32(796)

    balance_mastery = MemInt32(804)
    death_mastery = MemInt32(808)
    fire_mastery = MemInt32(812)
    ice_mastery = MemInt32(816)
    life_mastery = MemInt32(820)
    myth_mastery = MemInt32(824)
    storm_mastery = MemInt32(828)
    maximum_number_of_islands = MemInt32(832)
    gardening_level = MemUInt32(836)
    gardening_xp = MemInt32(840)
    invisible_to_friends = MemBool(844)
    show_item_lock = MemBool(845)
    quest_finder_enabled = MemBool(846)

    buddy_list_limit = MemInt32(848)
    stun_resistance_percent = MemFloat32(852)
    dont_allow_friend_finder_codes = MemBool(856)

    shadow_pip_max = MemInt32(860)

    shadow_magic_unlocked = MemBool(864)
    fishing_level = MemUInt8(865)

    fishing_xp = MemInt32(868)
    subscriber_benefit_flags = MemUInt32(872)
    elixir_benefit_flags = MemUInt32(876)
    monster_magic_level = MemUInt8(880)

    monster_magic_xp = MemInt32(884)
    player_chat_channel_is_public = MemBool(888)

    extra_inventory_space = MemInt32(892)
    remember_last_realm = MemBool(896)
    new_spellbook_layout_warning = MemBool(897)


    purchased_custom_emotes1 = MemUInt32(900)
    purchased_custom_teleport_effects1 = MemUInt32(904)
    equipped_teleport_effect = MemUInt32(908)
    highest_world1_id = MemUInt32(912)
    highest_world2_id = MemUInt32(916)
    active_class_projects_list = MemUInt32(920)

    disabled_item_slot_ids = MemUInt32(936)

    adventure_power_cooldown_time = MemUInt32(952)
    purchased_custom_emotes2 = MemUInt32(956)
    purchased_custom_teleport_effects2 = MemUInt32(960)
    purchased_custom_emotes3 = MemUInt32(964)
    purchased_custom_teleport_effects3 = MemUInt32(968)
    shadow_pip_rating = MemFloat32(972)
    bonus_shadow_pip_rating = MemFloat32(976)
    shadow_pip_rate_accumulated = MemFloat32(980)
    shadow_pip_rate_threshold = MemFloat32(984)
    shadow_pip_rate_percentage = MemInt32(988)
    friendly_player = MemBool(992)

    emoji_skin_tone = MemInt32(996)
    show_pvp_option = MemUInt32(1000)
    favorite_slot = MemInt32(1004)
    cantrip_level = MemUInt8(1008)

    cantrip_xp = MemInt32(1012)


    spell_charge_base = MemCppValVector()

    async def spell_charge_base(self) -> List[int]:
        return await self.read_dynamic_vector(136, "int")

    async def dmg_bonus_percent(self) -> List[float]:
        return await self.read_dynamic_vector(328, "float")

    async def write_dmg_bonus_percent(self, dmg_bonus_percent: float):
        await self.write_value_to_offset(328, dmg_bonus_percent, "float")

    async def dmg_bonus_flat(self) -> List[float]:
        return await self.read_dynamic_vector(352, "float")

    async def write_dmg_bonus_flat(self, dmg_bonus_flat: float):
        await self.write_value_to_offset(352, dmg_bonus_flat, "float")

    async def acc_bonus_percent(self) -> List[float]:
        return await self.read_dynamic_vector(376, "float")

    async def write_acc_bonus_percent(self, acc_bonus_percent: float):
        await self.write_value_to_offset(376, acc_bonus_percent, "float")

    async def ap_bonus_percent(self) -> List[float]:
        return await self.read_dynamic_vector(400, "float")

    async def write_ap_bonus_percent(self, ap_bonus_percent: float):
        await self.write_value_to_offset(400, ap_bonus_percent, "float")

    async def dmg_reduce_percent(self) -> List[float]:
        return await self.read_dynamic_vector(424, "float")

    async def write_dmg_reduce_percent(self, dmg_reduce_percent: float):
        await self.write_value_to_offset(424, dmg_reduce_percent, "float")

    async def dmg_reduce_flat(self) -> List[float]:
        return await self.read_dynamic_vector(448, "float")

    async def write_dmg_reduce_flat(self, dmg_reduce_flat: float):
        await self.write_value_to_offset(448, dmg_reduce_flat, "float")

    async def acc_reduce_percent(self) -> List[float]:
        return await self.read_dynamic_vector(472, "float")

    async def write_acc_reduce_percent(self, acc_reduce_percent: float):
        await self.write_value_to_offset(472, acc_reduce_percent, "float")

    async def heal_bonus_percent(self) -> List[float]:
        return await self.read_dynamic_vector(496, "float")

    async def write_heal_bonus_percent(self, heal_bonus_percent: float):
        await self.write_value_to_offset(496, heal_bonus_percent, "float")

    async def heal_inc_bonus_percent(self) -> List[float]:
        return await self.read_dynamic_vector(520, "float")

    async def write_heal_inc_bonus_percent(self, heal_inc_bonus_percent: float):
        await self.write_value_to_offset(520, heal_inc_bonus_percent, "float")

    async def spell_charge_bonus(self) -> List[int]:
        return await self.read_dynamic_vector(568, "int")

    async def write_spell_charge_bonus(self, spell_charge_bonus: int):
        await self.write_value_to_offset(568, spell_charge_bonus, "int")

    async def critical_hit_percent_by_school(self) -> List[float]:
        return await self.read_dynamic_vector(592, "float")

    async def write_critical_hit_percent_by_school(
        self, critical_hit_percent_by_school: float
    ):
        await self.write_value_to_offset(592, critical_hit_percent_by_school, "float")

    async def block_percent_by_school(self) -> List[float]:
        return await self.read_dynamic_vector(616, "float")

    async def write_block_percent_by_school(self, block_percent_by_school: float):
        await self.write_value_to_offset(616, block_percent_by_school, "float")

    async def critical_hit_rating_by_school(self) -> List[float]:
        return await self.read_dynamic_vector(640, "float")

    async def write_critical_hit_rating_by_school(
        self, critical_hit_rating_by_school: float
    ):
        await self.write_value_to_offset(640, critical_hit_rating_by_school, "float")

    async def block_rating_by_school(self) -> List[float]:
        return await self.read_dynamic_vector(664, "float")

    async def write_block_rating_by_school(self, block_rating_by_school: float):
        await self.write_value_to_offset(664, block_rating_by_school, "float")
    
    async def fishing_luck_bonus_percent(self) -> List[float]:
        return await self.read_dynamic_vector(544, "float")

    async def write_fishing_luck_bonus_percent(self, fishing_luck_bonus_percent: float):
        await self.write_value_to_offset(544, fishing_luck_bonus_percent, "float")
    
    async def pip_conversion_rating_per_school(self) -> List[float]:
        return await self.read_dynamic_vector(256, "float")

    async def write_pip_conversion_rating_per_school(
        self, pip_conversion_rating_per_school: float
    ):
        await self.write_value_to_offset(256, pip_conversion_rating_per_school, "float")

    async def pip_conversion_percent_per_school(self) -> List[float]:
        return await self.read_dynamic_vector(288, "float")

    async def write_pip_conversion_percent_per_school(
        self, pip_conversion_percent_per_school: float
    ):
        await self.write_value_to_offset(
            288, pip_conversion_percent_per_school, "float"
        )

    async def pip_conversion_base_per_school(self) -> List[int]:
        return await self.read_dynamic_vector(744, "int")

    async def write_pip_conversion_base_per_school(
        self, pip_conversion_base_per_school: int
    ):
        await self.write_value_to_offset(744, pip_conversion_base_per_school, "int")


class CurrentGameStats(GameStats):
    async def read_base_address(self) -> int:
        return await self.hook_handler.read_current_player_stat_base()
