import re
import iarm.exceptions
import iarm.cpu


class _Meta(iarm.cpu.Cpu):
    """
    Give helper functions to the instructions
    """
    REGISTER_REGEX = r'R(\d*)'
    IMMEDIATE_REGEX = r'#(\d*)'

    def parse_lines(self, code):
        """
        Return a list of the parsed code

        For each line, return a three-tuple containing:
        1. The label
        2. The instruction
        3. Any arguments or parameters

        An element in the tuple may be None or '' if it did not find anything
        :param code: The code to parse
        :return: A list of tuples in the form of (label, instruction, parameters)
        """
        parser = re.compile(r'^(\w*)?\s*(\w*)\s*(.*)$', re.MULTILINE)
        return parser.findall(code)

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
        1. The parameter is undefined
        :param arg: The parameter to check
        :return: None
        """
        if arg is None or arg == '':
            raise iarm.exceptions.RuleError("Parameter is None, did you miss a comma?")

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
            raise iarm.exceptions.RuleError("Parameter {} is not a register".format(arg))
        r_num = int(match.groups()[0])
        if r_num > self._max_registers:
            raise iarm.exceptions.RuleError(
                "Register {} is greater than defined registers of {}".format(arg, self._max_registers))

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
            raise iarm.exceptions.RuleError("Parameter {} is not an immediate".format(arg))
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
        if (i_num > (2 ** bit - 1)) or (i_num < 0):
            raise iarm.exceptions.RuleError("Immediate {} is not an unsigned {} bit value".format(arg, bit))
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
        if (i_num > _max) or (i_num < _min):
            raise iarm.exceptions.RuleError("Immediate {} is not within the range of [{}, {}]".format(arg, _min, _max))
        return i_num

    def check_multiple_of(self, value, multiple_of):
        if (value % multiple_of) != 0:
            raise iarm.exceptions.RuleError("Immediate {} is not a multiple of {}".format(value, multiple_of))

    # Rules
    def rule_low_registers(self, arg):
        r_num = self.check_register(arg)
        if r_num > 7:
            raise iarm.exceptions.RuleError(
                "Using a high register in low register position for parameter {}".format(arg))

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
        self.check_immediate_value(arg, 2 ** 5 - 1, 1)

    def rule_imm6_2(self, arg):
        i_num = self.check_immediate_unsigned_value(arg, 6)
        self.check_multiple_of(i_num, 2)

    def rule_imm7_4(self, arg):
        i_num = self.check_immediate_unsigned_value(arg, 7)
        self.check_multiple_of(i_num, 4)

    def rule_imm8(self, arg):
        self.check_immediate_unsigned_value(arg, 8)

    def rule_immS8_2(self, arg):
        i_num = self.check_immediate_value(arg, 2 ** 8 - 1, -(2 ** 8))
        self.check_multiple_of(i_num, 2)

    def rule_imm9_4(self, arg):
        i_num = self.check_immediate_unsigned_value(arg, 9)
        self.check_multiple_of(i_num, 4)

    def rule_imm10_4(self, arg):
        i_num = self.check_immediate_unsigned_value(arg, 10)
        self.check_multiple_of(i_num, 4)

    def rule_immS25_4(self, arg):
        i_num = self.check_immediate_value(arg, 2 ** 25, -2 ** 25)
        self.check_multiple_of(i_num, 4)

    def get_parameters(self, regex_exp, parameters):
        """
        Given a regex expression and the string with the paramers,
        either return a regex match object or raise an exception if the regex
        did not find a match
        :param regex_exp:
        :param parameters:
        :return:
        """
        match = re.match(regex_exp, parameters)
        if not match:
            raise iarm.exceptions.ParsingError("Parameters are None, did you miss a comma?")
        return match

    def get_two_parameters(self, regex_exp, parameters):
        """
        Get two parameters from a given regex expression

        Raise an exception if more than two were found
        :param regex_exp:
        :param parameters:
        :return:
        """
        match = self.get_parameters(regex_exp, parameters)
        Rx, Ry, other = match.groups()
        if other:
            raise iarm.exceptions.ParsingError("Extra arguments found: {}".format(other))
        if Rx and Ry:
            return Rx, Ry
        elif not Rx:
            raise iarm.exceptions.ParsingError("Missing first positional argument")
        else:
            raise iarm.exceptions.ParsingError("Missing second positional argument")

    def get_three_parameters(self, regex_exp, parameters):
        """
        Get three parameters from a given regex expression

        Raise an exception if more than three were found
        :param regex_exp:
        :param parameters:
        :return:
        """
        match = self.get_parameters(regex_exp, parameters)
        Rx, Ry, Rz, other = match.groups()
        if other:
            raise iarm.exceptions.ParsingError("Extra arguments found: {}".format(other))
        return Rx, Ry, Rz
