from typing import List, Optional

from wizwalker.errors import MemoryReadError
from wizwalker.utils import XYZ
from wizwalker.memory import HookHandler
from wizwalker.memory.memory_object import PropertyClass
from wizwalker.memory.memtypes import *
from .combat_participant import CombatParticipant
from .enums import DuelExecutionOrder, DuelPhase, SigilInitiativeSwitchMode
from .combat_resolver import CombatResolver


# TODO: add m_gameEffectInfo and friends, and fix offsets
class Duel(PropertyClass):
    @staticmethod
    def obj_size() -> int:
        # unverified
        return 672

    duel_id_full = MemUInt64(72)

    dynamic_turn = MemUInt32(120)
    dynamic_turn_subcircles = MemUInt32(124)
    dynamic_turn_counter = MemUInt32(128)

    planning_timer = MemFloat32(144)
    position = MemXYZ(148)

    yaw = MemFloat32(160)

    pvp = MemBool(176)
    battleground = MemBool(177)
    raid = MemBool(178)

    disable_timer = MemBool(179)
    tutorial_mode = MemBool(180)

    first_team_to_act = MemInt32(184)
    original_first_team_to_act = MemInt32(188)

    round_num = MemInt32(192)

    execution_phase_timer = MemFloat32(200)

    duel_phase = MemEnum(DuelPhase, 196)

    initiative_switch_mode = MemEnum(SigilInitiativeSwitchMode, 384)
    initiative_switch_rounds = MemInt32(388)

    alt_turn_counter = MemInt32(456)


    execution_order = MemEnum(DuelExecutionOrder, 528)

    no_henchmen = MemBool(532)

    hide_noncombatant_distance = MemFloat32(536)
    spell_truncation = MemBool(540)

    shadow_threshold_factor = MemFloat32(548)
    shadow_pip_rating_factor = MemFloat32(552)
    default_shadow_pip_rating = MemFloat32(556)
    shadow_pip_threshold_team0 = MemFloat32(560)
    shadow_pip_threshold_team1 = MemFloat32(560)

    scalar_damage = MemFloat32(592)
    scalar_resist = MemFloat32(596)
    scalar_pierce = MemFloat32(600)
    damage_limit = MemFloat32(604)
    k0 = MemFloat32(608)
    n0 = MemFloat32(612)
    resist_limit = MemFloat32(616)
    r_k0 = MemFloat32(620)
    r_n0 = MemFloat32(624)
    full_party_group = MemBool(628)
    is_player_timed_duel = MemBool(629)


    match_timer = MemFloat32(648)
    bonus_time = MemFloat32(652)
    pass_penalty = MemInt32(656)
    yellow_time = MemInt32(660)
    red_time = MemInt32(664)
    min_turn_time = MemInt32(668)


    # TODO: Make work
    # async def participant_list(
    #     self,
    # ) -> List[DynamicCombatParticipant]:
    #     pointers = await self.read_shared_vector(80)

    #     participants = []
    #     for addr in pointers:
    #         participants.append(DynamicCombatParticipant(self.hook_handler, addr))

    #     return participants

    # async def combat_resolver(self) -> Optional[DynamicCombatResolver]:
    #     addr = await self.read_value_from_offset(136, "long long")

    #     if addr == 0:
    #         return None

    #     return DynamicCombatResolver(self.hook_handler, addr)



# TODO: Update
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
        duel_manager = DynamicClientDuelManager(self.hook_handler, await self.read_typed(self._duel_manager_addr, "long long"))
        for duel in (await duel_manager.duelmap()).values():
            for part in await duel.participant_list():
                if await part.owner_id_full() == await self.hook_handler.client.client_object.global_id_full():
                    return await duel.read_base_address()
        return 0

    async def duel_phase(self) -> DuelPhase:
        try:
            return await super().duel_phase()
        except MemoryReadError:
            return DuelPhase.ended
