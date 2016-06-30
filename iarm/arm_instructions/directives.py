import iarm.exceptions
from ._meta import _Meta
import warnings
import inspect


class Directives(_Meta):
    """
    Directives, unline instructions, perform their action immediately
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.equates = {}
        self.directives = {}
        self.space_pointer = 0  # Refers to a place in memory
        self.title = ""

        # Get all instructions and rules
        for obj in inspect.getmembers(self, predicate=inspect.ismethod):
            # Is returned in the form of (method name, method)
            name = obj[0]
            method = obj[1]

            # Directives are defiined by starting with 'directive_'
            if str.startswith(name, 'directive_'):
                self.directives[name[len('directive_'):]] = method

    def directive_TTL(self, label, params):
        self.title = params

    def directive_THUMB(self):
        # TODO should this set something?
        warnings.warn("This directive is not yet implemented")

    def directive_EQU(self, label, params):
        # TODO do a check on params
        # TODO figure out how to do equates
        # TODO can equates work on other things besides parameters (like instructions?)
        # TODO equates can use labels + offsets
        # TODO check if the equate label exists as a label already
        self.equates[label] = params

    def directive_AREA(self, label, params):
        # TODO do something
        warnings.warn("This directive is not yet implemented")

    def directive_EXPORT(self, label, params):
        # TODO do something
        warnings.warn("This directive is not yet implemented")

    def directive_ALIGN(self, label, params):
        warnings.warn("This directive is not yet implemented")

    def directive_ENTRY(self, label, params):
        warnings.warn("This directive is not yet implemented")

    def directive_SPACE(self, label, params):
        self.labels[label] = self.space_pointer
        if params in self.equates:
            params = self.equates[params]
        self.space_pointer += self.convert_to_integer(params)

    def directive_END(self, label, params):
        # TODO This should stick an end function into the program that always raises an error and raise a warning here
        raise iarm.exceptions.EndOfProgram("You have reached the end of the program")

    def directive_DCD(self, label, params):
        # TODO make this read only
        # TODO check for param size
        # TODO can take any length comma separated values (VAL DCD 1, 0x2, 3, 4

        # Align address
        if self.space_pointer % 4 != 0:
            self.space_pointer += self.space_pointer % 4
        self.labels[label] = self.space_pointer
        if params in self.equates:
            params = self.equates[params]
        for i in range(4):
            self.memory[self.space_pointer + i] = (self.convert_to_integer(params) >> (8*i)) & 0xFF
        self.space_pointer += 4

    def directive_DCH(self, label, params):
        # TODO make this read only
        # TODO check for word size

        # Align address
        if self.space_pointer % 2 != 0:
            self.space_pointer += self.space_pointer % 2
        self.labels[label] = self.space_pointer
        if params in self.equates:
            params = self.equates[params]
        for i in range(2):
            self.memory[self.space_pointer + i] = (self.convert_to_integer(params) >> (8 * i)) & 0xFF
        self.space_pointer += 2

    def directive_DCB(self, label, params):
        # TODO make this read only
        # TODO check for byte size
        self.labels[label] = self.space_pointer
        if params in self.equates:
            params = self.equates[params]
        self.memory[self.space_pointer] = self.convert_to_integer(params) & 0xFF
        self.space_pointer += 1
