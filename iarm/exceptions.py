
class IarmError(Exception):
    pass


class IarmWarning(Warning):
    pass


class RuleError(IarmError):
    pass


class ParsingError(IarmError):
    pass