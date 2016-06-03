
class IarmError(Exception):
    pass


class IarmWarning(Warning):
    pass


class RuleError(IarmError):
    pass


class ParsingError(IarmError):
    pass


class ValidationError(IarmError):
    pass


class NotImplementedError(IarmError):
    pass


class BrainFart(IarmError):
    """
    Errors internal to the program or for those 3AM programming mistakes
    """
    pass