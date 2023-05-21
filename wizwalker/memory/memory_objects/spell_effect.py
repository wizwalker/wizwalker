from typing import List

from wizwalker.memory.memory_object import DynamicMemoryObject, PropertyClass
from .enums import (
    SpellEffects,
    EffectTarget,
    HangingDisposition,
    HangingEffectType,
    OutputEffectSelector,
    CountBasedType,
)
from wizwalker.memory.memory_objects.conditionals import RequirementList


class SpellEffect(PropertyClass):
    async def read_base_address(self) -> int:
        raise NotImplementedError()

    async def effect_type(self) -> SpellEffects:
        return await self.read_enum(72, SpellEffects)

    async def write_effect_type(self, effect_type: SpellEffects):
        await self.write_enum(72, effect_type)

    async def effect_param(self) -> int:
        return await self.read_value_from_offset(76, "int")

    async def write_effect_param(self, effect_param: int):
        await self.write_value_to_offset(76, effect_param, "int")

    async def string_damage_type(self) -> str:
        return await self.read_string_from_offset(88)

    async def write_string_damage_type(self, string_damage_type: str):
        await self.write_string_to_offset(88, string_damage_type)

    async def disposition(self) -> HangingDisposition:
        return await self.read_enum(80, HangingDisposition)

    async def write_disposition(self, disposition: HangingDisposition):
        await self.write_enum(80, disposition)

    async def damage_type(self) -> int:
        return await self.read_value_from_offset(84, "unsigned int")

    async def write_damage_type(self, damage_type: int):
        await self.write_value_to_offset(84, damage_type, "unsigned int")

    async def pip_num(self) -> int:
        return await self.read_value_from_offset(128, "int")

    async def write_pip_num(self, pip_num: int):
        await self.write_value_to_offset(128, pip_num, "int")

    async def act_num(self) -> int:
        return await self.read_value_from_offset(132, "int")

    async def write_act_num(self, act_num: int):
        await self.write_value_to_offset(132, act_num, "int")

    async def effect_target(self) -> EffectTarget:
        return await self.read_enum(140, EffectTarget)

    async def write_effect_target(self, effect_target: EffectTarget):
        await self.write_enum(140, effect_target)

    async def num_rounds(self) -> int:
        return await self.read_value_from_offset(144, "int")

    async def write_num_rounds(self, num_rounds: int):
        await self.write_value_to_offset(144, num_rounds, "int")

    async def param_per_round(self) -> int:
        return await self.read_value_from_offset(148, "int")

    async def write_param_per_round(self, param_per_round: int):
        await self.write_value_to_offset(148, param_per_round, "int")

    async def heal_modifier(self) -> float:
        return await self.read_value_from_offset(152, "float")

    async def write_heal_modifier(self, heal_modifier: float):
        await self.write_value_to_offset(152, heal_modifier, "float")

    async def spell_template_id(self) -> int:
        return await self.read_value_from_offset(120, "unsigned int")

    async def write_spell_template_id(self, spell_template_id: int):
        await self.write_value_to_offset(120, spell_template_id, "unsigned int")

    async def enchantment_spell_template_id(self) -> int:
        return await self.read_value_from_offset(124, "unsigned int")

    async def write_enchantment_spell_template_id(
        self, enchantment_spell_template_id: int
    ):
        await self.write_value_to_offset(
            124, enchantment_spell_template_id, "unsigned int"
        )

    async def act(self) -> bool:
        return await self.read_value_from_offset(136, "bool")

    async def write_act(self, act: bool):
        await self.write_value_to_offset(136, act, "bool")

    async def cloaked(self) -> bool:
        return await self.read_value_from_offset(157, "bool")

    async def write_cloaked(self, cloaked: bool):
        await self.write_value_to_offset(157, cloaked, "bool")

    async def armor_piercing_param(self) -> int:
        return await self.read_value_from_offset(160, "int")

    async def write_armor_piercing_param(self, armor_piercing_param: int):
        await self.write_value_to_offset(160, armor_piercing_param, "int")

    async def chance_per_target(self) -> int:
        return await self.read_value_from_offset(164, "int")

    async def write_chance_per_target(self, chance_per_target: int):
        await self.write_value_to_offset(164, chance_per_target, "int")

    async def protected(self) -> bool:
        return await self.read_value_from_offset(168, "bool")

    async def write_protected(self, protected: bool):
        await self.write_value_to_offset(168, protected, "bool")

    async def converted(self) -> bool:
        return await self.read_value_from_offset(169, "bool")

    async def write_converted(self, converted: bool):
        await self.write_value_to_offset(169, converted, "bool")

    async def rank(self) -> int:
        return await self.read_value_from_offset(208, "int")

    async def write_rank(self, rank: int):
        await self.write_value_to_offset(208, rank, "int")

    async def maybe_effect_list(
        self, *, check_type: bool = False
    ) -> List["DynamicSpellEffect"]:
        if check_type:
            type_name = await self.maybe_read_type_name()
            if type_name not in (
                "RandomSpellEffect",
                "RandomPerTargetSpellEffect",
                "VariableSpellEffect",
                "EffectListSpellEffect",
                "ShadowSpellEffect"
            ):
                raise ValueError(
                    f"This object is a {type_name} not a"
                    f" Random/RandomPerTarget/Variable/EffectList SpellEffect."
                )

        effects = []

        for addr in await self.read_shared_linked_list(224):
            effect = await cast_effect_variant(DynamicSpellEffect(self.hook_handler, addr))
            effects.append(effect)

        return effects


class DynamicSpellEffect(DynamicMemoryObject, SpellEffect):
    pass


class HangingConversionSpellEffect(DynamicSpellEffect):
    async def hanging_effect_type(self) -> HangingEffectType:
        return await self.read_enum(224, HangingEffectType)

    async def write_hanging_effect_type(self, hanging_effect_type: HangingEffectType):
        await self.write_enum(self, hanging_effect_type)

    async def specific_effect_types(self) -> list[SpellEffects]: #TODO: missing a write function, doesn't really matter -slack
        results = []
        for i in await self.read_shared_linked_list(232):
            effect = DynamicSpellEffect(self.hook_handler, i)
            results.append(await effect.effect_type())

        return results

    async def min_effect_value(self) -> int:
        return await self.read_value_from_offset(248, "int")

    async def write_min_effect_value(self, min_effect_value: int):
        await self.write_value_to_offset(248, min_effect_value, "int")

    async def max_effect_value(self) -> int:
        return await self.read_value_from_offset(252, "int")

    async def write_max_effect_value(self, max_effect_value: int):
        await self.write_value_to_offset(252, max_effect_value, "int")

    async def not_damage_type(self) -> bool:
        return await self.read_value_from_offset(256, "bool")

    async def write_not_damage_type(self, not_damage_type: bool):
        await self.write_value_to_offset(256, not_damage_type, "bool")

    async def min_effect_count(self) -> int:
        return await self.read_value_from_offset(260, "int")

    async def write_min_effect_count(self, min_effect_count: int):
        await self.write_value_to_offset(260, min_effect_count, "int")

    async def max_effect_count(self) -> int:
        return await self.read_value_from_offset(264, "int")

    async def write_max_effect_count(self, max_effect_count: int):
        await self.write_value_to_offset(264, max_effect_count, "int")

    async def bypass_protection(self) -> bool:
        return await self.read_value_from_offset(159, "bool")

    async def write_bypass_protection(self, bypass_protection: bool):
        await self.write_value_to_offset(159, bypass_protection, "bool")

    async def output_selector(self) -> OutputEffectSelector:
        return await self.read_enum(268, OutputEffectSelector)

    async def write_output_selector(self, output_selector: OutputEffectSelector):
        await self.write_enum(268, output_selector)

    async def scale_source_effect_value(self) -> bool:
        return await self.read_value_from_offset(272, "bool")

    async def write_scale_source_effect_value(self, scale_source_effect_value: bool):
        await self.write_value_to_offset(272, scale_source_effect_value, "bool")

    async def scale_source_effect_percent(self) -> float:
        return await self.read_value_from_offset(276, "float")

    async def write_scale_source_effect_percent(self, scale_source_effect_percent: float):
        await self.write_value_to_offset(276, scale_source_effect_percent, "float")

    async def apply_to_effect_source(self) -> bool:
        return await self.read_value_from_offset(280, "bool")

    async def write_apply_to_effect_source(self, apply_to_effect_source: bool):
        await self.write_value_to_offset(280, apply_to_effect_source, "bool")

    async def output_effect(self) -> List[DynamicSpellEffect]: #TODO: missing a write function, doesn't really matter -slack
        results = []
        for i in await self.read_shared_linked_list(288):
            effect = await cast_effect_variant(DynamicSpellEffect(self.hook_handler, i))
            results.append(effect)

        return results


#NOTE: This isn't specified by type dump, and is here to reduce code repetition
class CompoundSpellEffect(DynamicSpellEffect):
    async def effects_list(self) -> List[DynamicSpellEffect]:
        results = []
        for i in await self.read_shared_linked_list(224):
            results.append(DynamicSpellEffect(self.hook_handler, i))

        return results



class DynamicSpellEffect(DynamicMemoryObject, SpellEffect):
    pass


class ConditionalSpellElement(PropertyClass):
    async def reqs(self) -> RequirementList:
        return RequirementList(
            self.hook_handler,
            await self.read_value_from_offset(72, "unsigned long long"),
        )

    async def effect(self) -> DynamicSpellEffect:
        addr = await self.read_value_from_offset(88, "unsigned long long")
        return await cast_effect_variant(DynamicSpellEffect(self.hook_handler, addr))


class DynamicConditionalSpellElement(DynamicMemoryObject, ConditionalSpellElement):
    pass


class ConditionalSpellEffect(DynamicSpellEffect):
    async def elements(self) -> List[DynamicConditionalSpellElement]:
        elements = []
        for addr in await self.read_shared_linked_list(224):
            element = DynamicConditionalSpellElement(self.hook_handler, addr)
            elements.append(element)

        return elements


class ShadowSpellEffect(DynamicSpellEffect):
    async def initial_backlash(self) -> int:
        return await self.read_value_from_offset(240, "int")
    
    async def write_initial_backlash(self, intial_backlash: int):
        await self.write_value_to_offset(240, intial_backlash, "int")


class CountBasedSpellEffect(DynamicSpellEffect):
    async def mode(self) -> CountBasedType:
        return await self.read_enum(224, CountBasedType)

    async def write_mode(self, mode: CountBasedType):
        await self.write_enum(224, mode)

    async def effect_list(self) -> List[DynamicSpellEffect]: #TODO: missing a write function, doesn't really matter -slack
        effects = []
        for addr in await self.read_shared_linked_list(232):
            effect = cast_effect_variant(DynamicSpellEffect(self.hook_handler, addr))
            effects.append(effect)

        return effects


class CountBasedSpellEffect(DynamicSpellEffect):
    async def mode(self) -> CountBasedType:
        return await self.read_enum(224, CountBasedType)

    async def write_mode(self, mode: CountBasedType):
        await self.write_enum(224, mode)

    async def effect_list(self) -> List[DynamicSpellEffect]: #TODO: missing a write function, doesn't really matter -slack
        effects = []
        for addr in await self.read_shared_linked_list(232):
            effects.append(DynamicSpellEffect(self.hook_handler, addr))

        return effects


class RandomSpellEffect(CompoundSpellEffect):
    pass


class RandomPerTargetSpellEffect(RandomSpellEffect):
    pass


class VariableSpellEffect(CompoundSpellEffect):
    pass


class EffectListSpellEffect(CompoundSpellEffect):
    pass


class ShadowSpellEffect(EffectListSpellEffect):
    async def initial_backlash(self) -> int:
        return await self.read_value_from_offset(240, "int")
    
    async def write_initial_backlash(self, intial_backlash: int):
        await self.write_value_to_offset(240, intial_backlash, "int")


async def cast_effect_variant(read_effect: DynamicSpellEffect) -> DynamicSpellEffect:
    '''
    Creates an effect variant based on the output of read_type_name for an effect PropertyClass.\n
    Args:
    - read_effect (DynamicSpellEffect): Effect read from memory. Must be a child or instance of DynamicSpellEffect.
    '''
    addr = await read_effect.read_base_address()

    match await read_effect.read_type_name():
        case "HangingConversionSpellEffect":
            return HangingConversionSpellEffect(read_effect.hook_handler, addr)

        case "ConditionalSpellEffect":
            return ConditionalSpellEffect(read_effect.hook_handler, addr)

        case "ShadowSpellEffect":
            return ShadowSpellEffect(read_effect.hook_handler, addr)

        case "CountBasedSpellEffect":
            return CountBasedSpellEffect(read_effect.hook_handler, addr)

        case "RandomSpellEffect":
            return RandomSpellEffect(read_effect.hook_handler, addr)

        case "RandomPerTargetSpellEffect":
            return RandomPerTargetSpellEffect(read_effect.hook_handler, addr)

        case "VariableSpellEffect":
            return VariableSpellEffect(read_effect.hook_handler, addr)

        case "EffectListSpellEffect":
            return EffectListSpellEffect(read_effect.hook_handler, addr)

        case _:
            return read_effect


async def get_spell_effects(base: PropertyClass, offset: int) -> List[DynamicSpellEffect]:
    '''
    Gets spell effects from a PropertyClass (spell and spell_template), and properly assigns the variant SpellEffect type to each.\n
    Args:
    - base (PropertyClass): An instance of the class to read from
    - offset (int): The offset to use
    '''
    effects = []
    for addr in await base.read_shared_vector(offset):
        effect = await cast_effect_variant(DynamicSpellEffect(base.hook_handler, addr))
        effects.append(effect)

    return effects