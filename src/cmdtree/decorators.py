from functools import wraps

from cmdtree import echo
from cmdtree.exceptions import ParserError
from cmdtree.format import format_node_help


def format_error(func):

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ParserError as e:
            assert hasattr(args[0], "tree")
            node_dict = args[0].tree.get_node_by_path(
                e.node.cmd_path
            )
            node_help = format_node_help(node_dict)
            echo.error("Error: %s" % str(e.format_error(node_help)))
            exit(1)

    return wrapped
