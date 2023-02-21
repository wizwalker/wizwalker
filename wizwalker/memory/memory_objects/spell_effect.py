from typing import List

from wizwalker.memory.memory_object import PropertyClass
from .enums import SpellEffects, EffectTarget, HangingDisposition

from memonster.memtypes import *
from .memtypes import *


class SpellEffect(PropertyClass):
    effect_type = MemEnum(72, SpellEffects)
    effect_param = MemInt32(76)
    disposition = MemEnum(80, HangingDisposition)
    damage_type = MemUInt32(84)
    string_damage_type = MemCppString(88)

    spell_template_id = MemUInt32(120)
    enchantment_spell_template_id = MemUInt32(124)

    pip_num = MemInt32(128)
    act_num = MemInt32(132)
    act = MemBool(136)

    effect_target = MemEnum(140, EffectTarget)
    num_rounds = MemInt32(144)
    param_per_round = MemInt32(148)
    heal_modifier = MemFloat32(152)

    cloaked = MemBool(157)

    armor_piercing_param = MemInt32(160)
    chance_per_target = MemInt32(164)
    protected = MemBool(168)
    converted = MemBool(169)

    rank = MemInt32(208)

    def maybe_effect_list(self, *, check_type: bool = False):
        if check_type:
            type_name = self.maybe_read_type_name()
            if type_name not in ("RandomSpellEffect", "RandomPerTargetSpellEffect", "VariableSpellEffect"):
                raise ValueError(
                    f"This object is a {type_name} not a"
                    f" Random/RandomPerTarget/Variable SpellEffect."
                )
        return self.cast_offset(224, MemCppLinkedList(0, MemCppSharedPointer(0, SpellEffect(0))))
