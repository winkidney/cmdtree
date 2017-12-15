class ParserError(ValueError):
    pass


class DevelopmentError(ValueError):
    pass


class ArgumentRepeatedRegister(DevelopmentError):
    pass


class ArgumentTypeError(DevelopmentError):
    pass


class CmdRepeatedRegister(DevelopmentError):
    pass


class NodeDoesExist(DevelopmentError):
    pass


class NoSuchCommand(ParserError):
    pass


class InvalidCommand(ParserError):
    pass


class ArgumentError(ParserError):
    pass


class OptionError(ParserError):
    pass
