from cmdtree.templates import E_NO_CMD_GIVEN_TPL

try:
    from textwrap import indent
except ImportError:
    import textwrap
    def indent(text, indent_with):
        wrapper = textwrap.TextWrapper(
            initial_indent=indent_with,
            subsequent_indent=indent_with
        )
        return wrapper.fill(text)


INDENT_1 = " " * 4


def _format_arg_help(argument):
    """
    :type argument: cmdtree.parser.Argument
    """
    tpl = "{name}: {help}"
    _help = argument.help
    if argument.help is None:
        _help = "argument"
    return tpl.format(
        name=argument.name,
        help=_help,
    )


def _format_cmd_help(cmd_node):
    tpl = "{name}: {help}"
    _help = cmd_node.help
    if cmd_node.help is None:
        _help = cmd_node.name
    return tpl.format(
        name=cmd_node.name,
        help=_help,
    )


def _format_cmd_choice(parent_name, cmd_node_list):
    help_msg = "\n".join(
        _format_cmd_help(ele)
        for ele in cmd_node_list
    )
    return E_NO_CMD_GIVEN_TPL.format(
        name=parent_name,
        cmds=indent(help_msg, INDENT_1)
    )


def format_node_help(tree_node):
    """
    :type tree_node: dict
    """
    node = tree_node
    _help = ""
    if not node['cmd'].callable():
        if node['cmd'].help is not None:
            _help += node['cmd'].help
        cmds = tuple(
            value['cmd']
            for value in node['children'].values()
        )
        if len(cmds) >= 0:
            _help += _format_cmd_choice(node['name'], cmds)
    return _help if len(_help) > 0 else None


def format_arg_help(title, arguments):
    """
    :type arguments: iterable[cmdtree.parser.Argument]
    :type title: str
    """
    if len(arguments) == 0:
        return
    details = tuple(
        _format_arg_help(arg)
        for arg in arguments
    )
    details = indent("\n".join(details), INDENT_1)
    return (
        "{title}\n"
        "{details}"
    ).format(title=title, details=details)
