
class ParserError(ValueError):
    DEFAULT_TPL = (
        "{error}\n\n"
        "{cmd_ref}"
        "{help}"
        "{sub_cmd_help}"
    )

    def __init__(self, *args, **kwargs):
        super(ParserError, self).__init__(*args)
        self.node = kwargs.pop("node", None)

    def format_error(self, sub_cmd_help=None):
        cmd_ref = "Help message for '{name}':\n\n"
        node_help = ""
        _cmd_ref = ""
        if sub_cmd_help is not None:
            sub_cmd_help = sub_cmd_help + "\n"
        else:
            sub_cmd_help = ""
        if self.node is not None:
            node_help = self.node.format_help()
            if node_help:
                node_help += "\n\n"
            _cmd_ref = cmd_ref.format(
                name=self.node.name
            )
        return self.DEFAULT_TPL.format(
            error=str(self),
            cmd_ref=_cmd_ref,
            sub_cmd_help=sub_cmd_help,
            help=node_help,
        )


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
