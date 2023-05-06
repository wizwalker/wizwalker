from wizwalker.memory.memory_objects.enums import *
from wizwalker.memory.memory_object import PropertyClass, DynamicMemoryObject
from typing import Any


charm_effect_types = [
    SpellEffects.modify_outgoing_damage,
    SpellEffects.modify_outgoing_damage_flat,
    SpellEffects.modify_outgoing_heal,
    SpellEffects.modify_outgoing_heal_flat,
    SpellEffects.modify_outgoing_damage_type,
    SpellEffects.modify_outgoing_armor_piercing,
    SpellEffects.push_charm,
    SpellEffects.steal_charm,
    SpellEffects.remove_charm,
    SpellEffects.swap_charm,
    SpellEffects.cloaked_charm,
    SpellEffects.modify_card_charm,
    SpellEffects.push_converted_charm,
    SpellEffects.steal_converted_charm,
    SpellEffects.remove_converted_charm
    ]

over_time_effect_types = [
    SpellEffects.reduce_over_time,
    SpellEffects.detonate_over_time,
    SpellEffects.steal_over_time,
    SpellEffects.remove_over_time,
    SpellEffects.swap_over_time,
    SpellEffects.push_converted_over_time,
    SpellEffects.steal_converted_over_time,
    SpellEffects.remove_converted_over_time,
    SpellEffects.damage_over_time,
    SpellEffects.modify_over_time_duration,
    SpellEffects.heal_over_time
    ]

ward_effect_types =[
    SpellEffects.push_ward,
    SpellEffects.steal_ward,
    SpellEffects.remove_ward,
    SpellEffects.swap_ward,
    SpellEffects.cloaked_ward,
    SpellEffects.cloaked_ward_no_remove,
    SpellEffects.heal_by_ward,
    SpellEffects.push_converted_ward,
    SpellEffects.steal_converted_ward,
    SpellEffects.remove_converted_ward,
    SpellEffects.modify_incoming_damage,
    SpellEffects.modify_incoming_damage_flat,
    SpellEffects.maximum_incoming_damage,
    SpellEffects.modify_incoming_heal,
    SpellEffects.modify_incoming_heal_flat ,
    SpellEffects.modify_incoming_damage_type,
    SpellEffects.modify_incoming_armor_piercing,
    SpellEffects.modify_card_incoming_damage,
    SpellEffects.modify_incoming_damage_over_time,
    SpellEffects.modify_incoming_heal_over_time
    ]


class HangingSpellEffect(Enum):
    InvalidSpellEffect = 0,
    AbsorbDamage = 35,
    AbsorbHeal = 36,
    AddCombatTriggerList = 85,
    Afterlife = 80,
    BacklashDamage = 87,
    BounceAll = 34,
    BounceBack = 33,
    BounceNext = 31,
    BouncePrevious = 32,
    CloakedCharm = 40,
    CloakedWard = 41,
    CloakedWardNoRemove = 84,
    Confusion = 39,
    ConfusionBlock = 107,
    CritBlock = 45,
    CritBoost = 44,
    CritBoostSchoolSpecific = 95,
    Damage = 1,
    DamageNoCrit = 2,
    DamageOverTime = 73,
    DamagePerTotalPipPower = 82,
    Dampen = 66,
    DeferredDamage = 81,
    DelayCast = 47,
    DetonateOverTime = 7,
    Dispel = 38,
    DivideDamage = 103,
    Heal = 3,
    HealOverTime = 74,
    InstantKill = 79,
    Intercept = 89,
    MaxHealthDamage = 110,
    MaximumIncomingDamage = 23,
    MindControl = 68,
    ModifyAccuracy = 37,
    ModifyBacklash = 88,
    ModifyCardAccuracy = 51,
    ModifyCardArmorPiercing = 54,
    ModifyCardCloak = 48,
    ModifyCardDamage = 49,
    ModifyCardMutation = 52,
    ModifyCardRank = 53,
    ModifyHate = 72,
    ModifyIncomingArmorPiercing = 26,
    ModifyIncomingDamage = 22,
    ModifyIncomingDamageFlat = 117,
    ModifyIncomingDamageType = 25,
    ModifyIncomingHeal = 24,
    ModifyIncomingHealFlat = 116,
    ModifyIncomingHealOverTime = 136,
    ModifyOutgoingArmorPiercing = 30,
    ModifyOutgoingDamage = 27,
    ModifyOutgoingDamageFlat = 119,
    ModifyOutgoingDamageType = 29,
    ModifyOutgoingHeal = 28,
    ModifyOutgoingHealFlat = 118,
    ModifyPipRoundRate = 108,
    ModifyPips = 69,
    ModifyPowerPipChance = 75,
    ModifyPowerPips = 70,
    ModifyRank = 76,
    ModifyShadowCreatureLevel = 92,
    ModifyShadowPips = 71,
    PipConversion = 43,
    Polymorph = 46,
    PowerPipConversion = 98,
    ProtectBeneficial = 101,
    ProtectCardBeneficial = 99,
    ProtectCardHarmful = 100,
    ProtectHarmful = 102,
    PushCharm = 8,
    PushOverTime = 12,
    PushWard = 10,
    ReduceOverTime = 6,
    RemoveAura = 17,
    RemoveCharm = 14,
    RemoveCombatTriggerList = 86,
    RemoveOverTime = 16,
    RemoveWard = 15,
    Reshuffle = 67,
    RevealCloak = 78,
    SelectShadowCreatureAttackTarget = 93,
    ShadowCreature = 91,
    ShadowDecrementTurn = 94,
    ShadowSelf = 90,
    SpawnCreature = 96,
    StealCharm = 9,
    StealHealth = 5,
    StealOverTime = 13,
    StealWard = 11,
    Stun = 65,
    StunBlock = 77,
    StunResist = 42,
    SummonCreature = 63,
    SwapCharm = 19,
    SwapOverTime = 21,
    SwapWard = 20,
    TeleportPlayer = 64,
    UnPolymorph = 97,
    MaxHealthHeal = 127,
    HealByWard = 128,
    Taunt = 129,
    Pacify = 130

class Operator(Enum):
    AND = 0
    OR = 1

class RequirementTarget(Enum):
    Caster = 0
    Target = 1

class MinionType(Enum):
    Is_Minion = 0,
    Has_Minion = 1,
    On_Team = 2,
    On_Other_Team = 3,
    On_Any_Team = 4

class StatusEffect(Enum):
    Stunned = 0
    Confused = 1

class Requirement(DynamicMemoryObject, PropertyClass):
    async def applyNOT(self) -> bool:
        return await self.read_value_from_offset(72, 'bool')
        
    async def operator(self) -> Operator:
        return await self.read_enum(76, Operator)
    
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        # data can contain:
        # - combat: CombatHandler instance
        # - target_idx: combat member index
        raise NotImplementedError()
    
    async def _do_ops(self, original_state: bool, new_state: bool) -> bool:
        state = new_state ^ (await self.applyNOT())
        match await self.operator():
            case Operator.AND:
                return original_state and state
            case Operator.OR:
                return original_state or state
            
    async def apply(self, original_state: bool, data: dict[str, Any]) -> bool:
        return await self._do_ops(original_state, await self._evaluate(data))

class RequirementList(Requirement):
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        state = True
        for req in await self.requirements():
            preq = await promote_requirement(req)
            state = await preq.apply(state, data)
        return state
    
    async def requirements(self) -> list[Requirement]:
        results = []
        for items in await self.read_shared_linked_list(80):
            results.append(Requirement(self.hook_handler, items))
        return results

class ConditionalSpellEffectRequirement(Requirement):
    async def targetType(self) -> RequirementTarget:
        return await self.read_enum(80, RequirementTarget)
    
    async def get_target(self, data: dict[str, Any]):
        combat: CombatHandler = data['combat']
        if await self.targetType() == RequirementTarget.Caster:
            member = await combat.get_client_member()
        else:
            member = (await combat.get_members())[data["target_idx"]]

        return member
#"name": "class ReqHangingCharm

class ReqHangingCharm(ConditionalSpellEffectRequirement):
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        member = await self.get_target(data)
        participant = await member.get_participant()
        
        hanging_effects = await participant.hanging_effects()
        valid_effects = []
        for effect in hanging_effects:
            if await effect.effect_type() in charm_effect_types:
                if await effect.disposition() == HangingDisposition.both or await self.disposition() == HangingDisposition.both or await effect.disposition() == await self.disposition():
                    valid_effects.append(effect)

        # print(str(await self.minCount()) + ' minimum')
        # print(str(len(valid_effects)) + ' current')
        # print(str(await self.maxCount()) + ' maximum')
        return await self.minCount() <= len(valid_effects) <= await self.maxCount()

    async def disposition(self) -> HangingDisposition:
        return await self.read_enum(88, HangingDisposition)

    async def minCount(self) -> int:
        return await self.read_value_from_offset(92, 'int')
    
    async def maxCount(self) -> int:
        return await self.read_value_from_offset(96, 'int')

class ReqCombatHealth(ConditionalSpellEffectRequirement):
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        member = await self.get_target(data)
        member_health_percentage = (await member.health() / await member.max_health())
        return await self.fMinPercent() <= member_health_percentage <= await self.fMaxPercent()

    async def fMinPercent(self) -> float:
        return await self.read_value_from_offset(88, 'float')
    
    async def fMaxPercent(self) -> float:
        return await self.read_value_from_offset(92, 'float')

class ReqHangingOverTime(ConditionalSpellEffectRequirement):
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        member = await self.get_target(data)
        participant = await member.get_participant()
        hanging_effects = await participant.hanging_effects()
        valid_effects = []
        for effect in hanging_effects:
            if await effect.effect_type() in over_time_effect_types and await effect.disposition == await self.disposition:
                valid_effects.append(effect)
        return await self.minCount() <= len(valid_effects) <= await self.maxCount()

    async def disposition(self) -> HangingDisposition:
        return await self.read_enum(88, HangingDisposition)

    async def minCount(self) -> int:
        return await self.read_value_from_offset(92, 'int')
    
    async def maxCount(self) -> int:
        return await self.read_value_from_offset(96, 'int')

school_id_to_names = {'Fire': 2343174, 'Ice': 72777, 'Storm': 83375795, 'Myth': 2448141, 'Life': 2330892, 'Death': 78318724, 'Balance': 1027491821, 'Star': 2625203, 'Sun': 78483, 'Moon': 2504141, 'Gardening': 663550619, 'Shadow': 1429009101, 'Fishing': 1488274711, 'Cantrips': 1760873841, 'CastleMagic': 806477568, 'WhirlyBurly': 931528087}
school_to_str = {index: i for i, index in school_id_to_names.items()}

class ReqIsSchool(ConditionalSpellEffectRequirement):
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        member = await self.get_target(data)
        participant = await member.get_participant()
        school_id = await participant.primary_magic_school_id()
        return await self.magicSchoolName() == school_to_str[school_id]
        
    async def magicSchoolName(self) -> str:
        return await self.read_string_from_offset(88)

class ReqHangingWard(ConditionalSpellEffectRequirement):
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        member = await self.get_target(data)
        participant = await member.get_participant()
        hanging_effects = await participant.hanging_effects()
        valid_effects = []
        for effect in hanging_effects:
            if await effect.effect_type() in ward_effect_types and await effect.disposition == await self.disposition:
                valid_effects.append(effect)
        return await self.minCount() <= len(valid_effects) <= await self.maxCount()

    async def disposition(self) -> HangingDisposition:
        return await self.read_enum(88, HangingDisposition)

    async def minCount(self) -> int:
        return await self.read_value_from_offset(92, 'int')

    async def maxCount(self) -> int:
        return await self.read_value_from_offset(96, 'int')

class ReqHangingEffectType(ConditionalSpellEffectRequirement):
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        member = await self.get_target(data)
        participant = await member.get_participant()
        hanging_effects = await participant.hanging_effects()
        #TODO finsh this

    async def effectType(self) -> HangingSpellEffect:
        return await self.read_enum(88, HangingSpellEffect)
    
    async def param_low(self) -> int:
        return await self.read_value_from_offset(92, 'int')
    
    async def param_high(self) -> int:
        return await self.read_value_from_offset(96, 'int')
    
    async def min_count(self) -> int:
        return await self.read_value_from_offset(100, 'int')
    
    async def max_count(self) -> int:
        return await self.read_value_from_offset(104, 'int')

class ReqPvPCombat(ConditionalSpellEffectRequirement):
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        member = await self.get_target(data)
        participant = await member.get_participant()
        return await participant.pvp()

class ReqShadowPipCount(ConditionalSpellEffectRequirement):
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        member = await self.get_target(data)
        participant = await member.get_participant()
        num_shadow_pip = await participant.num_shadow_pips()
        return await self.minPips() <= num_shadow_pip <= await self.maxPips()

    async def minPips(self) -> int:
        return await self.read_value_from_offset(88, 'int')

    async def maxPips(self) -> int:
        return await self.read_value_from_offset(92, 'int')

class ReqPipCount(ConditionalSpellEffectRequirement):
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        member = await self.get_target(data)
        participant = await member.get_participant()
        num_power_pip = await participant.num_power_pips()
        return await self.minPips() <= num_power_pip <= await self.maxPips()

    async def minPips(self) -> int:
        return await self.read_value_from_offset(88, 'int')

    async def maxPips(self) -> int:
        return await self.read_value_from_offset(92, 'int')

class ReqMinion(ConditionalSpellEffectRequirement):
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        combat: CombatHandler = data['combat']
        
        member = await self.get_target(data)
        participant = await member.get_participant()
        match await self.minionType():
            case MinionType.Is_Minion:
                return await participant.is_minion()
            case MinionType.Has_Minion:
                #TODO find out what in the world this means
                raise NotImplementedError()
            case MinionType.On_Team:
                for combatmember in await combat.get_members():
                    if combatmember in await combat.get_members():
                        part = await combatmember.get_participant()
                        if combatmember.is_minion() and await part.team_id() == await participant.team_id():
                            return True
            case MinionType.On_Other_Team:
                for combatmember in await combat.get_members():
                    if combatmember in await combat.get_members():
                        part = await combatmember.get_participant()
                        if combatmember.is_minion() and not await part.team_id() == await participant.team_id():
                            return True
            case MinionType.On_Any_Team:
                for combatmember in await combat.get_members():
                    if await combatmember.is_minion():
                        return True
                    
        return False

    async def minionType(self) -> MinionType:
        return await self.read_enum(88, MinionType)

class ReqCombatStatus(ConditionalSpellEffectRequirement):
    async def _evaluate(self, data: dict[str, Any]) -> bool:
        member = await self.get_target(data)
        participant = await member.get_participant()
        match await self.status():
            case StatusEffect.Stunned:
                return await participant.stunned() != 0
            case StatusEffect.Confused:
                return await participant.confused() != 0

    async def status(self) -> StatusEffect:
        return await self.read_enum(88, StatusEffect)

async def promote_requirement(req: Requirement):
    print(await req.read_type_name())
    match await req.read_type_name():
        case 'ReqCombatHealth':
            prom_type = ReqCombatHealth
        case 'RequirementList':
            prom_type = RequirementList
        case 'ReqHangingCharm':
            prom_type =  ReqHangingCharm
        case 'ReqHangingOverTime':
            prom_type = ReqHangingOverTime
        case 'ReqHangingWard':
            prom_type = ReqHangingWard
        case 'ReqIsSchool':
            prom_type = ReqIsSchool
        # case 'ReqHangingEffectType':
        #     prom_type = ReqHangingEffectType
        case 'ReqPvPCombat':
            prom_type = ReqPvPCombat
        case 'ReqShadowPipCount':
            prom_type = ReqShadowPipCount
        case 'ReqPipCount':
            prom_type = ReqPipCount
        case 'ReqMinion':
            prom_type = ReqMinion
        case 'ReqCombatStatus':
            prom_type = ReqCombatStatus
        case _:
            raise RuntimeError(f"Unknown requirement type: {await req.read_type_name()}")
        
    return prom_type(req.hook_handler, await req.read_base_address())
