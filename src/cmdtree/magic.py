from cmdtree.tree import CmdTree
from cmdtree.registry import env


CMD_META_NAME = "meta"


def _mk_group(name, help=None, path_prefix=None):

    def wrapper(func):
        _name = name
        if name is None:
            _name = _get_func_name(func)

        full_path = path_prefix
        if path_prefix is None:
            full_path = []
        full_path.append(name)

        tree = _get_tree()
        parser = tree.add_parent_commands(full_path)
        _group = Group(func, _name, help=help, full_path=full_path, parser=parser)
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
        name_ = name
        if name is None:
            name_ = _get_func_name(func)

        tree = _get_tree()
        parser = tree.add_commands([name], func)
        return Cmd(
            func,
            name=name_,
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

    def __init__(self, name, full_path=None, parser=None):
        self.full_path = full_path or []
        self.name = name
        self.parser = parser


class Group(object):
    def __init__(self, func, name, parser, help=None, full_path=None):
        """
        :type func: callable
        :type name: str
        :type parser: cmdtree.parser.CmdTree
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

    def argument(self):
        pass

    def option(self):
        pass


class CommandCollection(object):
    def __init__(self, sources):
        assert isinstance(sources, (tuple, list))
        self.sources = sources


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


def argument(name, help=None):

    def wrapper(func):
        assert isinstance(func, (Group, Cmd))
        parser = func.meta.parser
        parser.argument(name, help=help)
        return func
    return wrapper


def option(name, help=None, is_flag=False):

    def wrapper(func):
        assert isinstance(func, (Group, Cmd))
        parser = func.meta.parser
        parser.option(name=name, help=help, is_flag=is_flag)
        return func
    return wrapper