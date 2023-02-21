from wizwalker.memory.memory_object import PropertyClass

from memonster.memtypes import *
from .memtypes import *


class GameStats(PropertyClass):
    def max_hitpoints(self) -> int:
        """
        Client's max hitpoints; base + bonus
        """
        base = self.base_hitpoints.read()
        bonus = self.bonus_hitpoints.read()
        return base + bonus

    def max_mana(self) -> int:
        """
        Clients's max mana; base + bonus
        """
        base = self.base_mana.read()
        bonus = self.bonus_mana.read()
        return base + bonus

    base_hitpoints = MemInt32(80)
    base_mana = MemInt32(84)
    base_gold_pouch = MemInt32(88)
    base_event_currency1_pouch = MemInt32(92)
    base_event_currency2_pouch = MemInt32(96)
    base_pvp_currency_pouch = MemInt32(100)
    energy_max = MemInt32(104)
    current_hitpoints = MemInt32(108)
    write_current_gold = MemInt32(112)
    current_event_currency1 = MemInt32(116)
    current_event_currency2 = MemInt32(120)
    current_pvp_currency = MemInt32(124)
    current_mana = MemInt32(128)
    current_arena_points = MemInt32(132)
    spell_charge_base = MemCppVector(136, MemInt32(0))
    potion_max = MemFloat32(160)
    potion_charge = MemFloat32(164)

    bonus_hitpoints = MemInt32(216)
    bonus_mana = MemInt32(220)

    bonus_energy = MemInt32(236)
    critical_hit_percent_all = MemFloat32(240)
    block_percent_all = MemFloat32(244)
    critical_hit_rating_all = MemFloat32(248)
    block_rating_all = MemFloat32(252)
    pip_conversion_rating_per_school = MemFloat32(256)

    pip_conversion_rating_all = MemFloat32(280)

    pip_conversion_percent_per_school = MemFloat32(288)

    pip_conversion_percent_all = MemFloat32(312)
    reference_level = MemInt32(316)
    highest_character_level_on_account = MemInt32(320)
    highest_character_world_on_account = MemInt32(324)
    pet_act_chance = MemInt32(328)

    dmg_bonus_percent = MemCppVector(336, MemFloat32(0))
    dmg_bonus_flat = MemCppVector(360, MemFloat32(0))
    acc_bonus_percent = MemCppVector(384, MemFloat32(0))
    ap_bonus_percent = MemCppVector(408, MemFloat32(0))
    dmg_reduce_percent = MemCppVector(432, MemFloat32(0))
    dmg_reduce_flat = MemCppVector(456, MemFloat32(0))
    acc_reduce_percent = MemCppVector(480, MemFloat32(0))
    heal_bonus_percent = MemCppVector(504, MemFloat32(0))
    heal_inc_bonus_percent = MemCppVector(528, MemFloat32(0))
    fishing_luck_bonus_percent = MemCppVector(552, MemFloat32(0))
    spell_charge_bonus = MemCppVector(576, MemInt32(0))
    critical_hit_percent_by_school = MemCppVector(600, MemFloat32(0))
    block_percent_by_school = MemCppVector(624, MemFloat32(0))
    critical_hit_rating_by_school = MemCppVector(648, MemFloat32(0))
    block_rating_by_school = MemCppVector(672, MemFloat32(0))
    dmg_bonus_percent_all = MemFloat32(696)
    dmg_bonus_flat_all = MemFloat32(700)
    acc_bonus_percent_all = MemFloat32(704)
    ap_bonus_percent_all = MemFloat32(708)
    dmg_reduce_percent_all = MemFloat32(712)
    dmg_reduce_flat_all = MemFloat32(716)
    acc_reduce_percent_all = MemFloat32(720)
    heal_bonus_percent_all = MemFloat32(724)
    heal_inc_bonus_percent_all = MemFloat32(728)
    fishing_luck_bonus_percent_all = MemFloat32(732)
    spell_charge_bonus_all = MemInt32(736)
    power_pip_base = MemFloat32(740)
    pip_conversion_base_all_schools = MemInt32(744)

    pip_conversion_base_per_school = MemInt32(752)

    power_pip_bonus_percent_all = MemFloat32(776)
    shadow_pip_bonus_percent = MemFloat32(780)
    xp_percent_increase = MemFloat32(784)

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
