import sys

from copy import deepcopy

from cmdtree import echo
from cmdtree.echo import error
from cmdtree.exceptions import (
    ParserError, ArgumentRepeatedRegister,
    ArgumentTypeError,
    ArgumentError,
    OptionError,
    NodeDoesExist,
    NoSuchCommand,
    InvalidCommand
)
from cmdtree.decorators import format_error

from cmdtree.format import format_arg_help
from cmdtree.registry import env
from cmdtree.templates import E_MISSING_ARGUMENT
from cmdtree.types import ParamTypeFactory, STRING


def _normalize_arg_name(arg_name):
    name_list = list(arg_name)
    new_name_list = []
    for index, ele in enumerate(name_list):
        prev_index = index -1 if index != 0 else index
        prev_ele = name_list[prev_index]
        if prev_ele == ele == "-":
            continue
        new_name_list.append(ele)
    arg_name = "".join(new_name_list)
    return arg_name.replace("-", "_")


def _assert_type_valid(name, type_):
    if not isinstance(type_, ParamTypeFactory):
        raise ArgumentTypeError(
            (
                "Invalid type of argument {}, "
                "should be instance of {}"
            ).format(
                name,
                ParamTypeFactory,
            )
        )


class Argument(object):
    def __init__(self, name, type_, help=None):
        self.name = name
        self.type = type_
        self.help = help

    def get_value(self, value):
        return self.type.convert(value)


class Option(object):
    def __init__(self, name, help=None, is_flag=False, default=None, type_=None):
        self.name = name
        self.default = default
        if is_flag:
            self.default = bool(default)
        self.is_flag = is_flag
        self.help = help
        self.type = type_
        # TODO: implement is_flag parse

    def get_value(self, value):
        return self.type.convert(value)


class ArgumentMgr(object):

    def __init__(self):
        self.arg_names = []
        self.arg_map = {}
        self.parsed_values = {}

    def assert_filled(self):
        if self.num_args > len(self.parsed_values):
            missed_args = [
                name
                for name in self.arg_names
                if name not in self.parsed_values
            ]
            msg = E_MISSING_ARGUMENT.format(
                args=", ".join(missed_args)
            )
            return False, msg
        return True, None

    def add(self, name, type_=None, help=None):
        type_ = type_ or STRING
        if name in self.arg_names:
            raise ArgumentRepeatedRegister(
                "Argument {} registered more than once.".format(
                    name
                )
            )
        _assert_type_valid(name, type_)
        self.arg_names.append(name)
        self.arg_map[name] = Argument(
            name=name,
            type_=type_,
            help=help,
        )

    def format_help(self):
        return format_arg_help(
            "Positional arguments:",
            tuple(
                self.arg_map[name]
                for name in self.arg_names
            ),
        )

    @property
    def num_args(self):
        return len(self.arg_names)

    def add_value(self, index, value):
        self.parsed_values[self.arg_names[index]] = value

    @property
    def kwargs(self):
        kwargs = {}
        for name, value in self.parsed_values.items():
            argument = self.arg_map[name]
            new_name = _normalize_arg_name(name)
            kwargs[new_name] = argument.get_value(value)
        return kwargs


class OptionMgr(object):
    def __init__(self):
        self.opts_names = []
        self.opts_map = {}
        self.parsed_values = {}

    def add(self, name, help=None, is_flag=False, default=None, type_=None):
        type_ = type_ or STRING
        if name in self.opts_names:
            raise ArgumentRepeatedRegister(
                "Argument {} registered more than once.".format(
                    name
                )
            )
        _assert_type_valid(name, type_)
        self.opts_names.append(name)
        self.opts_map[name] = Option(
            name=name,
            type_=type_,
            help=help,
            is_flag=is_flag,
            default=default
        )

    def get_option_or_none(self, name):
        """
        :rtype: Option
        """
        return self.opts_map.get(name)

    def add_value(self, name, value):
        self.parsed_values[name] = value

    def format_help(self):
        return format_arg_help(
            "Optional arguments:",
            tuple(
                self.opts_map[name]
                for name in self.opts_names
            ),
        )

    @property
    def kwargs(self):
        kwargs = {}
        for name, opt in self.opts_map.items():
            new_name = _normalize_arg_name(name)
            kwargs[new_name] = opt.default

        for name, value in self.parsed_values.items():
            argument = self.opts_map[name]
            new_name = _normalize_arg_name(name)
            kwargs[new_name] = argument.get_value(value)
        return kwargs


class CommandNode(object):
    """
    Arg-parse wrapper for sub command and convenient arg parse.
    """
    def __init__(self, cmd_path, help=None, func=None, is_root=False):
        self.is_root = is_root
        self.name = cmd_path[-1]
        self.cmd_path = cmd_path
        if is_root:
            self.abs_path = []
        self.help = help
        self.arg_mgr = ArgumentMgr()
        self.opt_mgr = OptionMgr()
        self.func = func

    def format_help(self):
        msg = ""
        arg_help = self.arg_mgr.format_help()
        opt_help = self.opt_mgr.format_help()
        if arg_help is not None:
            msg += "%s" % arg_help
        if opt_help is not None:
            msg += "\n\n%s" % opt_help
        return msg

    @property
    def kwargs(self):
        kwargs = {}
        kwargs.update(self.arg_mgr.kwargs)
        kwargs.update(self.opt_mgr.kwargs)
        return kwargs

    @classmethod
    def _is_option(cls, arg_str):
        return arg_str.startswith("-")

    def parse_args(self, possible_args):
        count = 0
        index = -1
        args_len = len(possible_args)
        while True:
            index += 1
            if index >= args_len:
                break
            current_arg = possible_args[index]
            if self._is_option(current_arg):
                option = self.opt_mgr.get_option_or_none(
                    current_arg
                )
                if option is None:
                    raise OptionError(
                        "No such option '%s'" % current_arg,
                        node=self,
                    )
                if option.is_flag:
                    self.opt_mgr.add_value(
                        name=option.name,
                        value=not option.default,
                    )
                    continue
                try:
                    self.opt_mgr.add_value(
                        name=option.name,
                        value=possible_args[index + 1],
                    )
                except IndexError:
                    raise ArgumentError(
                        "No value for argument %s" % option.name,
                        node=self,
                    )
                index += 1
                continue
            count += 1
            if count > self.arg_mgr.num_args:
                index -= 1
                break
            self.arg_mgr.add_value(
                count - 1,
                value=current_arg
            )
        filled, msg = self.arg_mgr.assert_filled()
        if not filled:
            raise ArgumentError(
                msg,
                node=self,
            )
        left_args = possible_args[index + 1:]
        eaten_length = args_len - len(left_args)
        return eaten_length, left_args

    def callable(self):
        return self.func is not None

    def run(self, kwargs):
        if self.callable():
            return self.func(**kwargs)

    def exit(self, status=0, message=None):
        if message:
            error(message)
        if env.silent_exit:
            sys.exit(status)
        else:
            raise ParserError(message)

    def argument(self, name, help=None, type=None):
        if name.startswith("-"):
            raise ValueError(
                "positional argument [{0}] can not contains `-` in".format(name)
            )

        return self.arg_mgr.add(
            name=name,
            help=help,
            type_=type,
        )

    def option(self, name, help=None, is_flag=False, default=None, type=None):
        _name = name
        if not name.startswith("-"):
            _name = "--" + name
        return self.opt_mgr.add(
            _name,
            help=help,
            is_flag=is_flag,
            default=default,
            type_=type,
        )


class RawArgsParser(object):

    def __init__(self, args, tree):
        """
        :type args: list[str]
        :type tree: cmdtree.tree.CmdTree
        """
        self.raw_args = args
        self.tree = tree
        self.cmd_nodes = []

    def parse2cmd(self, raw_args, tree):
        cmd_nodes = []
        full_cmd_path = []
        left_args = deepcopy(raw_args)
        cmd_start_index = 0
        node = None
        while True:
            cmd2find = left_args[cmd_start_index:cmd_start_index + 1]
            cmd_path2find = full_cmd_path + cmd2find
            try:
                node = tree.get_node_by_path(cmd_path2find)
            except NodeDoesExist:
                error_parent = node if node is not None else tree.root
                raise NoSuchCommand(
                    "Command %s does not exist."
                    % (
                        str(
                            cmd_path2find[-1]
                            if cmd_path2find
                            else sys.argv[0]
                        ),
                    ),
                    node=error_parent['cmd'],
                )
            cmd = node['cmd']
            left_args = left_args[cmd_start_index + 1:]
            index_offset, left_args = cmd.parse_args(
                left_args,
            )
            full_cmd_path = cmd_path2find
            cmd_nodes.append(node)
            if len(left_args) <= 0:
                break
        return cmd_nodes, full_cmd_path

    @format_error
    def run(self):
        self.cmd_nodes, cmd_path = self.parse2cmd(
            self.raw_args,
            self.tree,
        )
        kwargs = {}
        for node in self.cmd_nodes:
            kwargs.update(
                node['cmd'].kwargs
            )
        node = self.cmd_nodes[-1]
        cmd = node['cmd']
        if not cmd.callable():
            raise InvalidCommand(
                "%s is a command-group" % node['name'],
                node=node['cmd']
            )
        return cmd.run(kwargs)


