from argparse import ArgumentParser
import sys

import six

from cmdtree.exceptions import ArgumentParseError
from cmdtree.env import env


def vars_(object=None):
    """
    Clean all of the property starts with "_" then
    return result of vars(object).
    """
    filtered_vars = {}
    vars_dict = vars(object)
    for key, value in six.iteritems(vars_dict):
        if key.startswith("_"):
            continue
        filtered_vars[key] = value
    return filtered_vars


class AParser(ArgumentParser):
    """
    Arg-parse wrapper for sub command and convenient arg parse.
    """
    def __init__(self, *args, **kwargs):
        self.subparsers = None
        super(AParser, self).__init__(*args, **kwargs)

    def add_cmd(self, name, help="", func=None):
        """
        :rtype: AParser
        """
        if self.subparsers is None:
            self.subparsers = self.add_subparsers(
                help=help or 'sub-commands',
            )

        parser = self.subparsers.add_parser(
            name,
            help=help,
        )
        if func is not None:
            parser.set_defaults(_func=func)
        return parser

    def run(self, args=None, namespace=None):
        args = self.parse_args(args, namespace)
        if args._func:
            return args._func(**vars_(args))
        else:
            return args

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stderr)
        if env.silent_exit:
            sys.exit(status)
        else:
            raise ArgumentParseError(message)
