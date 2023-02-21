from .spell import Spell

from memonster.memtypes import *
from .memtypes import *


class CombatAction(MemType):
    spell_caster = MemInt32(72)

    target_subcircle_list = MemInt32(80)

    spell = MemPointer(96, Spell(0))

    spell_hits = MemInt8(112)
    interrupt = MemBool(113)
    sigil_spell = MemBool(114)
    show_cast = MemBool(115)
    critical_hit_roll = MemUInt8(116)
    stun_resist_roll = MemUInt8(117)

    pip_conversion_roll = MemInt32(120)
    handled_random_spell_per_target = MemBool(124)

    random_spell_effect_per_target_rolls = MemInt32(128)

    blocks_calculated = MemBool(152)

    serialized_blocks = MemCppString(160, False)

    confused_target = MemBool(208)
    after_died = MemBool(209)

    effect_chosen = MemUInt32(212)
    string_key_message = MemCppString(216)
    sound_file_name = MemCppString(248)
    duration_modifier = MemFloat32(280)
    serialized_targets_affected = MemCppString(288, False)

    force_spell = MemBool(336)
    delayed = MemBool(337)
    delayed_enchanted = MemBool(338)
    pet_cast = MemBool(339)
    pet_casted = MemBool(340)

    pet_cast_target = MemInt32(344)    
