"""
The POP operation.

Loads the value in memory pointed to by SP into a module,
then increments SP.

This uses the ALU but the flags generated are not stored.
"""

from itertools import product

from ..language_defs import (
    INSTRUCTION_GROUPS,
    MODULE_CONTROL,
    ALU_CONTROL_FLAGS,
    SRC_REGISTERS,
    DEST_REGISTERS,
    FLAGS,
    instruction_byte_from_bitdefs,
)

from ..operation_utils import assemble_instruction, match_and_parse_line
from ..data_structures import (
    get_arg_def_template, get_machine_code_byte_template
)

_NAME = "POP"


def generate_signatures():
    """
    Generate the definitions of all possible arguments passable.

    Returns:
        list(list(dict)): All possible arguments. See
        :func:`~.get_arg_def_template` for more information.
    """

    signatures = []
    for module in ("ACC", "A", "B", "C"):
        signature = []

        arg_def = get_arg_def_template()
        arg_def["value_type"] = "module_name"
        arg_def["value"] = module
        signature.append(arg_def)

        signatures.append(signature)

    return signatures


def generate_microcode_templates():
    """
    Generate microcode for all the POP operations.

    Returns:
        list(DataTemplate): DataTemplates for all the POP microcode.
    """

    data_templates = []

    signatures = generate_signatures()
    for signature in signatures:
        templates = generate_operation_templates(signature)
        data_templates.extend(templates)

    return data_templates


def generate_operation_templates(signature):
    """
    Create the DataTemplates to define a POP with the given args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular not operation to generate
            templates for.
    Returns:
        list(DataTemplate) : Datatemplates that define this pop.
    """
    instruction_byte_bitdefs = generate_instruction_byte_bitdefs(signature)

    flags_bitdefs = [FLAGS["ANY"]]

    step_0 = [
        MODULE_CONTROL["SP"]["OUT"],
        MODULE_CONTROL["MAR"]["IN"],
    ]
    step_1 = [
        MODULE_CONTROL[signature[0]["value"]]["IN"],
        MODULE_CONTROL["RAM"]["OUT"],
    ]

    step_2 = [
        MODULE_CONTROL["SP"]["OUT"],
        MODULE_CONTROL["ALU"]["A_IS_BUS"],
        MODULE_CONTROL["ALU"]["STORE_RESULT"],
    ]
    step_2.extend(ALU_CONTROL_FLAGS["A_PLUS_1"])

    step_3 = [
        MODULE_CONTROL["ALU"]["OUT"],
        MODULE_CONTROL["SP"]["IN"],
    ]

    control_steps = [step_0, step_1, step_2, step_3]

    return assemble_instruction(
        instruction_byte_bitdefs, flags_bitdefs, control_steps
    )


def generate_instruction_byte_bitdefs(signature):
    """
    Generate bitdefs to specify the instruction byte for these args.

    Args:
        signature (list(dict)): List of argument definitions that
            specify which particular not operation to generate
            the instruction byte bitdefs for.
    Returns:
        list(str): Bitdefs that make up the instruction_byte
    """

    return [
        INSTRUCTION_GROUPS["LOAD"],
        SRC_REGISTERS["SP+/-"],
        DEST_REGISTERS[signature[0]["value"]],
    ]


def parse_line(line):
    """
    Parse a line of assembly code to create machine code byte templates.

    If a line is not identifiably an POP assembly line, return an
    empty list instead.

    Args:
        line (str): Assembly line to be parsed.
    Returns:
        list(dict): List of instruction byte template dictionaries or an
        empty list.
    """

    match, signature = match_and_parse_line(
        line, _NAME, generate_signatures()
    )

    if not match:
        return []

    instruction_byte = instruction_byte_from_bitdefs(
        generate_instruction_byte_bitdefs(signature)
    )
    mc_byte = get_machine_code_byte_template()
    mc_byte["byte_type"] = "instruction"
    mc_byte["bitstring"] = instruction_byte

    return [mc_byte]