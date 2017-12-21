from cmdtree import env
from cmdtree.utils import _get_func_name, _get_cmd_path


CMD_META_NAME = "meta"


class CmdMeta(object):
    __slots__ = (
        "full_path",
        "name",
        "parser",
    )

    def __init__(self, name=None, full_path=None, parser=None):
        """
        :param full_path: should always be tuple to avoid
        unexpected changes from outside.
        """
        self.full_path = tuple(full_path) if full_path else tuple()
        self.name = name
        self.parser = parser


class ParserProxy(object):
    __slots__ = (
        "options",
        "arguments",
    )

    def __init__(self):
        self.options = []
        self.arguments = []

    def option(self, *args, **kwargs):
        self.options.append((args, kwargs))

    def argument(self, *args, **kwargs):
        self.arguments.append((args, kwargs))


class CmdProxy(object):
    """
    Used to store original cmd info for cmd build proxy.
    """
    __slots__ = (
        "func",
        "meta",
    )

    def __init__(self, func):
        self.func = func
        self.meta = CmdMeta(parser=ParserProxy())


class Group(object):
    def __init__(self, func, name, parser, help=None, full_path=None):
        """
        :type func: callable
        :type name: str
        :type parser: cmdtree.parser.CommandNode
        :type help: str
        :type full_path: tuple or list
        """
        self.func = func
        self.meta = CmdMeta(
            name=name,
            full_path=full_path,
            parser=parser,
        )
        self.help = help

    def __call__(self, *args, **kwargs):
        # TODO(winkidney): This func will not work in
        # any case now.Be left now for possible call.
        return self.func(*args, **kwargs)

    def command(self, name=None, help=None):
        return _mk_cmd(name, help=help, path_prefix=self.meta.full_path)

    def group(self, name=None, help=None):
        return _mk_group(name, help=help, path_prefix=self.meta.full_path)


class Cmd(object):
    def __init__(self, func, name, parser, help=None, full_path=None):
        self.func = func
        self.meta = CmdMeta(
            name=name,
            full_path=full_path,
            parser=parser,
        )
        self.help = help

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def _apply2parser(arguments, options, parser):
    """
    :return the parser itself
    :type arguments: list[list[T], dict[str, T]]
    :type options: list[list[T], dict[str, T]]
    :type parser: cmdtree.parser.CommandNode
    :rtype: cmdtree.parser.CommandNode
    """
    for args, kwargs in options:
        parser.option(*args, **kwargs)
    for args, kwargs in arguments:
        parser.argument(*args, **kwargs)
    return parser


def apply2parser(cmd_proxy, parser):
    """
    Apply a CmdProxy's arguments and options
    to a parser of argparse.
    :type cmd_proxy: callable or cmdtree.proxy.CmdProxy
    :type parser: cmdtree.parser.CommandNode
    :rtype: cmdtree.parser.CommandNode
    """
    if isinstance(cmd_proxy, CmdProxy):
        parser_proxy = cmd_proxy.meta.parser
        _apply2parser(
            parser_proxy.arguments,
            parser_proxy.options,
            parser,
        )
    return parser


def _mk_group(name, help=None, path_prefix=None):

    def wrapper(func):
        if isinstance(func, Group):
            raise ValueError(
                "You can not register group `{name}` more than once".format(
                    name=name
                )
            )
        _name = name
        _func = func

        if isinstance(func, CmdProxy):
            _func = func.func

        if name is None:
            _name = _get_func_name(_func)

        full_path = _get_cmd_path(path_prefix, _name)

        tree = env.tree
        parser = tree.add_parent_commands(full_path, help=help)['cmd']
        _group = Group(
            _func,
            _name,
            parser,
            help=help,
            full_path=full_path,
        )
        apply2parser(func, parser)
        return _group
    return wrapper


def _mk_cmd(name, help=None, path_prefix=None):
    def wrapper(func):
        if isinstance(func, Cmd):
            raise ValueError(
                "You can not register a command more than once: {0}".format(
                    func
                )
            )
        _func = func

        if isinstance(func, CmdProxy):
            _func = func.func

        _name = name
        if name is None:
            _name = _get_func_name(_func)

        full_path = _get_cmd_path(path_prefix, _name)
        tree = env.tree
        parser = tree.add_commands(full_path, _func, help=help)
        _cmd = Cmd(
            _func,
            _name,
            parser,
            help=help,
            full_path=full_path,
        )
        apply2parser(func, parser)

        return _cmd
    return wrapper