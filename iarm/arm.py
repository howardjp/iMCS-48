#!/usr/bin/env python3

import random
import re
import inspect

REGISTERS = 15  # 0 indexed
BIT_WIDTH = 32
MEMORY_SIZE = 1024

LOW_REGISTER = 7

GET_RANDOM_IF_NOT_DEFINED = False

register = {}
memory = {}
program = []
labels = {}
ops = {}


def get_register_value(R):
    """
    Get the register value of R

    If R has not been defined yet,
    then either 0 or a random number will be returned
    depending on the flag GET_RANDOM_IF_NOT_DEFINED
    :param R: The register to get the value
    :return: The integer value of hte register
    """
    if GET_RANDOM_IF_NOT_DEFINED:
        if register.get(R, None) is None:
            val = random.randint(0, 2**32 - 1)
            register[R] = val
    return register.get(R, 0)


def is_register(R):
    """
    Is R a register.

    Finds out by doing a regex match for R and a number
    Does not check if the register is within range
    :param R:
    :return:
    """
    #return re.match(r'R(?:(?:1[0-5])|[0-9])', R) is not none  # Checks within range as well
    return re.search(r'R(\d*)', R) is not None


def is_immediate(I):
    """
    Is I an immediate

    Only checks if a '#' symbol is preceeding a number
    Does not check bounds
    :param I:
    :return:
    """
    return re.search(r'#(\d*)', I) is not None


def separate_line(line):
    """
    separate the line into each of its parts
    line reference, instruction, param1, param2, param3
    :param line: The string to parse
    :return: A parsed 5 tuple
    """
    search = re.search(r'(\A[^ \s,]*)?\s*(\w*)(?:\s*([^ \s,]*)(?:,\s*([^ \s,]*)(?:,\s*([^ \s,]*))?)?)?\s*', line)
    groups = search.groups()
    return groups


def parse_lines(code):
    return [(separate_line(i), i) for i in code.split('\n')]


def check_arguments(**kwargs):
    """
    Determine if the parameters meet the specifications
    kwargs contains lists goruped by their parameter
    Low registers can only use R0-7
    High registers can use R-15
    Imm4 is a 4 bit number
    Imm10_4 is a 10 bit number that is a multiple for 4
    :param kwargs:
    :return:
    """
    for arg in kwargs.get('low_registers', []):
        if arg is None:
            raise ReferenceError("Parameter is None, did you miss a comma?")
        match = re.search(r'R(\d*)', arg)
        if match is None:
            raise ReferenceError("Parameter is not a register")
        r_num = int(match.groups()[0])
        if r_num > REGISTERS:
            raise ReferenceError("Undefined register")
        if r_num > LOW_REGISTER:
            raise ReferenceError("Using a high register in low register position")
    for arg in kwargs.get('high_registers', []):
        if arg is None:
            raise ReferenceError("Parameter is None, did you miss a comma?")
        match = re.search(r'R(\d*)', arg)
        if match is None:
            raise ReferenceError("Parameter is not a register")
        r_num = int(match.groups()[0])
        if r_num > REGISTERS:
            raise ReferenceError("Undefined register")
    for arg in kwargs.get('imm', []):
        # TODO implement this
        pass


def MOV(Rx, Ry):
    check_arguments(high_registers=(Rx, Ry))
    register[Rx] = get_register_value(Ry)
ops['MOV'] = MOV


def MOVS(Ra, Rb):
    if Rb is None:
        raise ReferenceError("Parameter is None, did you miss a comma?")
    if is_immediate(Rb):
        check_arguments(low_registers=[Ra], imm8=[Rb])
        register[Ra] = int(Rb[1:])
    else:
        check_arguments(low_registers=(Ra, Rb))
        register[Ra] = get_register_value(Rb)
ops['MOVS'] = MOVS


def ADD(Rx, Ry, Rz):
    # TODO implement ADD Rx, Rt, #imm10_4
    # TODO implement ADD Sp, SP, #imm9_4
    check_arguments(high_registers=(Rx, Ry, Rz))
    register[Rx] = get_register_value(Ry) + get_register_value(Rz)
ops['ADD'] = ADD


def evaluate(code):
    parsed = parse_lines(code)
    for i in parsed:
        if not any(i[0]):
            continue  # We have a blank line

        op = ops[i[0][1]]
        op(*i[0][2:len(inspect.signature(op).parameters) + 2])

        if i[0][0]:
            labels[i[0][0]] = len(program)
        program.append(i)
