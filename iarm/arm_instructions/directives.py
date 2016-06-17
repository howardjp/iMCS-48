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
        warnings.warn("This directive is not yet implemented")

    def directive_END(self, label, params):
        # TODO This should stick an end function into the program that always raises an error and raise a warning here
        raise iarm.exceptions.EndOfProgram("You have reached the end of the program")

    def directive_DCD(self, lable, params):
        warnings.warn("This directive is not yet implemented")
