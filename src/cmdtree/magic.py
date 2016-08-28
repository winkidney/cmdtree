from cmdtree.tree import CmdTree
from cmdtree.registry import env


CMD_META_NAME = "meta"


def _get_cmd_path(path_prefix, cmd_name):
    full_path = path_prefix
    if path_prefix is None:
        full_path = []
    full_path.append(cmd_name)
    return full_path


def _mk_group(name, help=None, path_prefix=None):

    def wrapper(func):
        _name = name
        _func = func

        def apply2parser(parser):
            pass

        if isinstance(func, MetaCmd):
            _func = func.func
            apply2parser = lambda parser_: func.meta.parser.apply2parser(parser_)

        if name is None:
            _name = _get_func_name(_func)

        full_path = _get_cmd_path(path_prefix, name)

        tree = _get_tree()
        parser = tree.add_parent_commands(full_path)['cmd']
        _group = Group(_func, _name, parser, help=help, full_path=full_path)
        apply2parser(parser)
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

        def apply2parser(parser):
            pass

        if isinstance(func, MetaCmd):
            _func = func.func
            apply2parser = lambda parser_: func.meta.parser.apply2parser(parser_)

        _name = name
        if name is None:
            _name = _get_func_name(_func)

        full_path = _get_cmd_path(path_prefix, _name)
        tree = _get_tree()
        parser = tree.add_commands(full_path, _func)
        apply2parser(parser)

        return Cmd(
            _func,
            name=_name,
            help=help,
            parser=parser
        )
    return wrapper


class CmdMeta(object):
    __slots__ = (
        "full_path",
        "name",
        "parser",
    )

    def __init__(self, name=None, full_path=None, parser=None):
        self.full_path = full_path or []
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

    def apply2parser(self, parser):
        """
        :type parser: cmdtree.parser.AParser
        :rtype: cmdtree.parser.AParser
        """
        for args, kwargs in self.options:
            parser.option(*args, **kwargs)
        for args, kwargs in self.arguments:
            parser.argument(*args, **kwargs)
        return parser


class MetaCmd(object):
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
        :type parser: cmdtree.parser.AParser
        :type help: str
        :type full_path: tuple or list
        """
        self.func = func
        self.meta = CmdMeta(name=name, full_path=full_path, parser=parser)
        self.help = help

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def command(self, name=None, help=None):
        return _mk_cmd(name=name, help=help, path_prefix=self.meta.full_path)

    def group(self, name=None, help=None):
        return _mk_group(name, help=help, path_prefix=self.meta.full_path)


class Cmd(object):
    def __init__(self, func, name, parser, help=None, full_path=None):
        self.func = func
        self.meta = CmdMeta(name=name, full_path=full_path, parser=parser)
        self.help = help

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def _get_tree():
    """
    :rtype: cmdtree.tree.CmdTree
    """
    if env.tree is None:
        env.tree = CmdTree()
    return env.tree


def _get_func_name(func):
    assert callable(func)
    return func.func_name


def group(name=None, help=None):
    """
    Group of commands, you can add sub-command/group in this group.
    :rtype : AParser
    """
    return _mk_group(name, help=help)


def command(name=None, help=None):
    return _mk_cmd(name, help=help)


def argument(name, help=None, type=None):

    def wrapper(func):
        if isinstance(func, (Group, Cmd, MetaCmd)):
            parser = func.meta.parser
            parser.argument(name, help=help, type=type)
            return func
        else:
            meta_cmd = MetaCmd(func)
            parser = meta_cmd.meta.parser
            parser.argument(name, help=help, type=type)
            return meta_cmd
    return wrapper


def option(name, help=None, is_flag=False, default=None, type=None):

    def wrapper(func):
        if isinstance(func, (Group, Cmd)):
            parser = func.meta.parser
            parser.option(
                name,
                help=help,
                is_flag=is_flag,
                default=default,
                type=type,
            )
            return func
        else:
            meta_cmd = MetaCmd(func)
            parser = meta_cmd.meta.parser
            parser.option(
                name,
                help=help,
                is_flag=is_flag,
                default=default,
                type=type,
            )
            return meta_cmd
    return wrapper