from cmdtree.proxy import CmdProxy, Group, Cmd, _mk_group, _mk_cmd


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
        if isinstance(func, (Group, Cmd, CmdProxy)):
            parser = func.meta.parser
            parser.argument(name, help=help, type=type)
            return func
        else:
            meta_cmd = CmdProxy(func)
            parser = meta_cmd.meta.parser
            parser.argument(name, help=help, type=type)
            return meta_cmd
    return wrapper


def option(name, help=None, is_flag=False, default=None, type=None):

    def wrapper(func):
        if isinstance(func, (Group, Cmd, CmdProxy)):
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
            meta_cmd = CmdProxy(func)
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
