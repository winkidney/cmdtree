CMD_META_NAME = "meta"


class CmdMeta(object):
    __slots__ = (
        "full_path",
        "name",
        "parser"
    )

    def __init__(self, name, full_path=None, parser=None):
        self.full_path = full_path
        self.name = name
        self.parser = parser


class Group(object):
    def __init__(self, func, name, help=None):
        self.func = func
        self.meta = CmdMeta(name=name)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def command(self, name=None, help=None):
        return _mk_cmd(name=name, help=help, path_prefix=None)

    def argument(self):
        pass

    def option(self):
        pass


class Cmd(object):
    def __init__(self, func, name, help=None):
        self.func = func
        self.meta = CmdMeta(name=name)

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


def set_cmd_name(cmd_meta):
    cmd_meta.name = True


def get_cmd_name(cmd_meta):
    return cmd_meta.name


def _get_func_name(func):
    assert callable(func)
    return func.func_name


def _mk_group(name, help=None):

    def wrapper(func):
        _group = Group(func, name, help=help)
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

        return Cmd(
            func,
            name=name_,
            help=help
        )
    return wrapper


def group(name=None, help=None):
    """
    Group of commands, you can add sub-command/group in this group.
    :rtype : AParser
    """
    return _mk_group(name, help=help)


def command(name=None, help=None):
    return _mk_cmd(name, help=help)