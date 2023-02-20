from typing import List, Optional

from wizwalker.errors import MemoryReadError
from wizwalker.utils import XYZ
from wizwalker.memory import HookHandler
from wizwalker.memory.memory_object import PropertyClass, DynamicMemoryObject
from .combat_participant import CombatParticipant
from .enums import DuelExecutionOrder, DuelPhase, SigilInitiativeSwitchMode
from .combat_resolver import CombatResolver

from memonster import LazyType
from memonster.memtypes import *
from .memtypes import *


# TODO: add m_gameEffectInfo and friends, and fix offsets
class Duel(PropertyClass):
    duel_id_full = MemUInt64(72)
    participant_list = MemCppVector(80, MemCppSharedPointer(0, CombatParticipant(0)))

    dynamic_turn = MemUInt32(120)
    dynamic_turn_subcircles = MemUInt32(124)
    dynamic_turn_counter = MemInt32(128)

    combat_resolver = MemPointer(136, CombatResolver(0))

    planning_timer = MemFloat32(144)
    position = MemXYZ(148)
    # TODO: Are the other orients next to this? Original did not define them
    yaw = MemFloat32(160)

    pvp = MemBool(176)
    battleground = MemBool(177)
    raid = MemBool(178)
    disable_timer = MemBool(179)
    tutorial_mode = MemBool(180)

    first_team_to_act = MemInt32(184)
    original_first_team_to_act = MemInt32(188)

    round_num = MemInt32(192)
    duel_phase = MemEnum(196, DuelPhase)
    execution_phase_timer = MemFloat32(200)

    initiative_switch_mode = MemEnum(384, SigilInitiativeSwitchMode)
    initiative_switch_rounds = MemInt32(388)

    alt_turn_counter = MemInt32(456)

    hide_noncombatant_distance = MemFloat32(536)

    execution_order = MemEnum(528, DuelExecutionOrder)
    no_henchmen = MemBool(532)
    
    spell_truncation = MemBool(540)

    shadow_threshold_factor = MemFloat32(548)
    shadow_pip_rating_factor = MemFloat32(552)
    default_shadow_pip_rating = MemFloat32(556)
    shadow_pip_threshold_team0 = MemFloat32(560)
    shadow_pip_threshold_team1 = MemFloat32(564)

    scalar_damage = MemFloat32(600)
    scalar_resist = MemFloat32(604)
    scalar_pierce = MemFloat32(608)
    damage_limit = MemFloat32(612)
    k0 = MemFloat32(616)
    d_n0 = MemFloat32(620)    
    resist_limit = MemFloat32(624)
    r_k0 = MemFloat32(628)
    r_n0 = MemFloat32(632)
    full_party_group = MemBool(636)
    is_player_timed_duel = MemBool(637)

    match_timer = MemFloat32(656)
    bonus_time = MemInt32(660)
    pass_penalty = MemInt32(664)
    yellow_time = MemInt32(668)
    red_time = MemInt32(672)
    min_turn_time = MemInt32(676)


# TODO: Monster
class CurrentDuel(Duel):
    def __init__(self, hook_handler: HookHandler):
        super().__init__(hook_handler)
        self._duel_manager_addr = None

    async def read_base_address(self) -> int:
        if not self._duel_manager_addr:
            mov_instruction_addr = await self.hook_handler.pattern_scan(
                rb".......\xE8....\x90.......\x48\x85\xC9\x74.\x0F\x28\x45",
                module="WizardGraphicalClient.exe"
            )
            rip_offset = await self.hook_handler.read_typed(
                mov_instruction_addr + 3, "int"
            )
            self._duel_manager_addr = mov_instruction_addr + 7 + rip_offset
        # avoid circular import
        from .client_duel_manager import DynamicClientDuelManager
        while True: # sometimes this can go wrong thanks to bad timing
            duel_manager = DynamicClientDuelManager(self.hook_handler, await self.read_typed(self._duel_manager_addr, "long long"))
            try:
                for duel in (await duel_manager.duelmap()).values():
                    for part in await duel.participant_list():
                        if await part.owner_id_full() == await self.hook_handler.client.client_object.global_id_full():
                            return await duel.read_base_address()
                return 0 # we succeeded but aren't in a duel
            except (ValueError, MemoryReadError):
                pass # if something else happens we want it to fail

    async def duel_phase(self) -> DuelPhase:
        try:
            return await super().duel_phase()
        except MemoryReadError:
            return DuelPhase.ended
