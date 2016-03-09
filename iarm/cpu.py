import inspect
import random


class Cpu(object):
    def __init__(self, bit_width, registers, memory_size, generate_random=False):
        """
        Inittialize the Cpu

        :param bit_width: What is the size of the registers
        :param registers: How many registers are there
        :param memory_size: What is the size of memory
        :param generate_random: If a register or memory address is undefined, should a random value be generated for it?
        :return:
        """
        self._bit_width = bit_width
        self._max_registers = registers
        self._memory_size = memory_size
        self._generate_random = generate_random

        self.register = Register(self._bit_width, self._generate_random)  # Holder for the register values
        self.memory = {}  # Holder for memory
        self.program = []  # Hold the current program, used for jumps
        self.labels = {}  # A label to program location lookup
        self.ops = {}  # What operations are defined

        self._rules = {}  # Holder for parameter rules

        for obj in inspect.getmembers(self, predicate=inspect.ismethod):
            # Is returned in the form of (method name, method)
            name = obj[0]
            method = obj[1]

            # Instructions are defined by being all uppercase
            if str.isupper(name):
                self.ops[name] = method
            # Rules are defined with starting with 'rule_'
            elif str.startswith(name, 'rule_'):
                self._rules[name[len('rule_'):]] = method

    def check_arguments(self, **kwargs):
        """
        Determine if the parameters meet the specifications
        kwargs contains lists goruped by their parameter
        rules are defined by methods starting with 'rule_'
        :param kwargs:
        :return:
        """
        for key in kwargs:
            if key in self._rules:
                for val in kwargs[key]:
                    self._rules[key](val)
            else:
                raise LookupError("Rule for {} does not exist. Make sure the rule starts with 'rule_'".format(key))

    def get_register_value(self, R):
        """
        Get the register value of R

        If R has not been defined yet,
        then either 0 or a random number will be returned
        depending on the flag _generate_random
        :param R: The register to get the value
        :return: The integer value of the register
        """
        if self._generate_random:
            if self.register.get(R, None) is None:
                val = random.randint(0, 2**self._bit_width - 1)
                self.register[R] = val
        return self.register.get(R, 0)

    def evaluate(self, code):
        # must be implemented on inheriting classes
        raise NotImplementedError("The class cant determine how to run the code")


class Register(dict):
    def __init__(self, bit_width, generate_random=False, *args, **kwargs):
        self._generate_random = generate_random
        self._bit_width = bit_width
        super().__init__(*args, **kwargs)

    def __getitem__(self, item):
        """
        Get the register value of item

        If item has not been defined yet,
        then either 0 or a random number will be returned
        depending on the flag _generate_random
        :param item: The register to get the value
        :return: The integer value of the register
        """
        if self._generate_random:
            if super().get(item, None) is None:
                val = random.randint(0, 2**self._bit_width - 1)
                self[item] = val
        return super().get(item, 0)
