"""The copy operation"""

from itertools import product

from language.definitions import REGISTERS, OPCODE_GROUPS, MODULE_CONTROL_FLAGS
import language.utils


def generate_datatemplates():
    """
    Gernerate datatemplates for all the copy operations.
    """

    sources = ["ACC", "A", "B", "C", "PC", "SP"]
    destinations = ["ACC", "A", "B", "C", "SP"]

    data_templates = []

    for src, dest in product(sources, destinations):
        if src != dest:
            template = create_datatemplate(src, dest)
            data_templates.append(template)

    return data_templates

def create_datatemplate(src, dest):
    """
    Create the datatemplates to define a copy from src to dest.
    """
    instruction_bits = "{group_code}{source_code}{dest_code}".format(
        group_code = OPCODE_GROUPS["COPY"],
        source_code = REGISTERS[src],
        dest_code = REGISTERS[dest]
    )

    flags_bits = utils.match_any_flag_bitpattern()

    steps = [
        [
            MODULE_CONTROL_FLAGS[src]["OUT"],
            MODULE_CONTROL_FLAGS[dest]["IN"]
        ]
    ]

    return language.utils.steps_to_data_templates(
        instruction_bits, flags_bits, steps
    )