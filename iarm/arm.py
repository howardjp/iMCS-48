#!/usr/bin/env python3

import re
import inspect

import iarm.cpu


class Arm(iarm.cpu.Cpu):
    REGISTER_REGEX = r'R(\d*)'
    IMMEDIATE_REGEX = r'#(\d*)'

    def separate_line(self, line):
        """
        separate the line into each of its parts
        line reference, instruction, param1, param2, param3
        :param line: The string to parse
        :return: A parsed 5 tuple
        """
        search = re.search(r'(\A[^ \s,]*)?\s*(\w*)(?:\s*([^ \s,]*)(?:,\s*([^ \s,]*)(?:,\s*([^ \s,]*))?)?)?\s*', line)
        groups = search.groups()
        return groups

    def parse_lines(self, code):
        return [(self.separate_line(i), i) for i in code.split('\n')]

    def is_register(self, R):
        """
        Is R a register.

        Finds out by doing a regex match for R and a number
        Does not check if the register is within range
        :param R: The parameter to check
        :return: True if the parameter is a register
        """
        return re.search(self.REGISTER_REGEX, R) is not None

    def is_immediate(self, I):
        """
        Is I an immediate

        Only checks if a '#' symbol is preceding a number
        Does not check bounds
        :param I: The parameter to check
        :return: True if the parameter is an immediate
        """
        return re.search(self.IMMEDIATE_REGEX, I) is not None

    def check_parameter(self, arg):
        """
        Is the parameter defined, or not None

        Raises an exception if
        1. the parameter is undefined
        :param arg: The parameter to check
        :return: None
        """
        if arg is None:
            raise ReferenceError("Parameter is None, did you miss a comma?")

    def check_register(self, arg):
        """
        Is the parameter a register in the form of 'R<d>',
        and if so is it within the bounds of registers defined

        Raises an exception if
        1. The parameter is not in the form of 'R<d>'
        2. <d> is outside the range of registers defined in the init value
            registers or _max_registers
        :param arg: The parameter to check
        :return: The number of the register
        """
        self.check_parameter(arg)
        match = re.search(self.REGISTER_REGEX, arg)
        if match is None:
            raise ReferenceError("Parameter {} is not a register".format(arg))
        r_num = int(match.groups()[0])
        if r_num > self._max_registers:
            raise ReferenceError("Register {} is greater than defined registers of {}".format(arg, self._max_registers))

        return r_num

    def check_immediate(self, arg):
        """
        Is the parameter an immediate in the form of '#<d>',

        Raises an exception if
        1. The parameter is not in the form of '#<d>'
        :param arg: The parameter to check
        :return: The value of the immediate
        """
        self.check_parameter(arg)
        match = re.search(self.IMMEDIATE_REGEX, arg)
        if match is None:
            raise ReferenceError("Parameter {} is not an immediate".format(arg))
        return int(match.groups()[0])

    def check_immediate_unsigned_value(self, arg, bit):
        """
        Is the immediate within the unsigned value of 2**bit - 1

        Raises an exception if
        1. The immediate value is > 2**bit - 1
        :param arg: The parameter to check
        :param bit: The number of bits to use in 2**bit
        :return: The value of the immediate
        """
        i_num = self.check_immediate(arg)
        if (i_num > (2**bit - 1)) or(i_num < 0):
            raise ReferenceError("Immediate {} is not an unsigned {} bit value".format(arg, bit))
        return i_num

    def check_immediate_value(self, arg, _max, _min=0):
        """
        Is the immediate within the range of [_min, _max]

        Raises an exception if
        1. The immediate value is < _min or > _max
        :param arg: The parameter to check
        :param _max: The maximum value
        :param _min: The minimum value, optional, default is zero
        :return: The immediate value
        """
        i_num = self.check_immediate(arg)
        if (i_num > _max) or(i_num < _min):
            raise ReferenceError("Immediate {} is not within the range of [{}, {}]".format(arg, _min, _max))
        return i_num

    # Rules
    def rule_low_registers(self, arg):
        r_num = self.check_register(arg)
        if r_num > 7:
            raise ReferenceError("Using a high register in low register position for parameter {}".format(arg))

    def rule_high_registers(self, arg):
        self.check_register(arg)

    def rule_imm3(self, arg):
        """
        Is the argument an immediate that is in the range of [0,7]
        :param arg: An immediate in the form of '#d'
        :return: None
        """
        self.check_immediate_unsigned_value(arg, 3)

    def rule_imm5(self, arg):
        """
        Is the argument an immediate that is in the range of [0,31]
        :param arg: An immediate in the form of '#d'
        :return: None
        """
        self.check_immediate_unsigned_value(arg, 5)

    def rule_imm5_counting(self, arg):
        self.check_immediate_value(arg, 2**5 - 1, 1)

    def rule_imm6_2(self, arg):
        i_num = self.check_immediate_unsigned_value(arg, 6)
        if (i_num % 2) != 0:
            raise ReferenceError("Immediate {} is not a multiple of 2".format(arg))

    def rule_imm7_4(self, arg):
        i_num = self.check_immediate_unsigned_value(arg, 7)
        if (i_num % 4) != 0:
            raise ReferenceError("Immediate {} is not a multiple of 4".format(arg))

    def rule_imm8(self, arg):
        self.check_immediate_unsigned_value(arg, 8)

    def rule_immS8_2(self, arg):
        i_num = self.check_immediate_value(arg, 2**8 - 1, -(2**8))
        if (i_num % 2) != 0:
            raise ReferenceError("Immediate {} is not a multiple of 2".format(arg))

    def rule_imm9_4(self, arg):
        i_num = self.check_immediate_unsigned_value(arg, 9)
        if (i_num % 4) != 0:
            raise ReferenceError("Immediate {} is not a multiple of 4".format(arg))

    def rule_imm10_4(self, arg):
        i_num = self.check_immediate_unsigned_value(arg, 10)
        if (i_num % 4) != 0:
            raise ReferenceError("Immediate {} is not a multiple of 4".format(arg))

    def rule_immS25_4(self, arg):
        i_num = self.check_immediate_value(arg, 2**25, -2**25)
        if (i_num % 4) != 0:
            raise ReferenceError("Immediate {} is not a multiple of 4".format(arg))

    # Instructions
    def MOV(self, Rx, Ry):
        self.check_arguments(high_registers=(Rx, Ry))
        self.register[Rx] = self.get_register_value(Ry)

    def MOVS(self, Ra, Rb):
        if Rb is None:
            raise ReferenceError("Parameter is None, did you miss a comma?")
        if self.is_immediate(Rb):
            self.check_arguments(low_registers=[Ra], imm8=[Rb])
            self.register[Ra] = int(Rb[1:])
        else:
            self.check_arguments(low_registers=(Ra, Rb))
            self.register[Ra] = self.get_register_value(Rb)

    def ADD(self, Rx, Ry, Rz):
        # TODO implement ADD Rx, Rt, #imm10_4
        # TODO implement ADD Sp, SP, #imm9_4
        self.check_arguments(high_registers=(Rx, Ry, Rz))
        self.register[Rx] = self.get_register_value(Ry) + self.get_register_value(Rz)

    def evaluate(self, code):
        parsed = self.parse_lines(code)
        for i in parsed:
            if not any(i[0]):
                continue  # We have a blank line

            op = self.ops[i[0][1]]
            op(*i[0][2:len(inspect.signature(op).parameters) + 2])

            if i[0][0]:
                self.labels[i[0][0]] = len(self.program)
            self.program.append(i)

if __name__ == '__main__':
    interp = Arm(32, 15, 1024)








