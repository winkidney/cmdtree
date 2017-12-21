import mock
import pytest
import six

from cmdtree import parser
from cmdtree.constants import ROOT_NODE_NAME
from cmdtree.exceptions import ParserError


def mk_obj(property_dict):
    class TestObject(object):
        pass
    obj = TestObject()
    for key, value in six.iteritems(property_dict):
        setattr(obj, key, value)
    return obj


@pytest.fixture()
def cmd_node():
    from cmdtree.parser import CommandNode
    return CommandNode(
        name=ROOT_NODE_NAME
    )


@pytest.fixture()
def test_func():
    def func():
        return "result"
    return func


@pytest.mark.parametrize(
    "arg_name, expected",
    (
        ("hello_world", "hello_world"),
        ("hello-world", "hello_world"),
        ("--hello-world", "hello_world"),
        ("---hello-world", "hello_world"),
        ("-hello-world", "hello_world"),
    )
)
def test_normalize_arg_name(arg_name, expected):
    from cmdtree.parser import _normalize_arg_name
    assert _normalize_arg_name(arg_name) == expected


class Testcmd_node:
    def test_should_execute_func(self, cmd_node, test_func):
        cmd_node.add_cmd("test", func=test_func)
        assert cmd_node.run(["test"]) == "result"

    def test_should_execute_child_cmd(self, cmd_node, test_func):
        parent = cmd_node.add_cmd("parent")
        parent.add_cmd("child", func=test_func)
        assert cmd_node.run(['parent', 'child']) == "result"

    @pytest.mark.parametrize(
        "cmd_func, exception",
        (
            (None, ValueError),
            (lambda *args, **kwargs: "str", None),
        )
    )
    def test_should_execute_without_func(self, cmd_func, exception, cmd_node):
        parent = cmd_node.add_cmd("parent")
        parent.add_cmd("child", func=cmd_func)
        if exception is not None:
            with pytest.raises(exception):
                cmd_node.run(['parent', 'child'])
        else:
            assert cmd_node.run(['parent', 'child']) == "str"

    @pytest.mark.parametrize(
        "silent_exit, exception",
        (
                (False, ParserError),
                (True, SystemExit)
        )
    )
    def test_should_parent_cmd_exit_or_raise_error(self, silent_exit, exception, test_func, cmd_node):
        from cmdtree.registry import env
        env.silent_exit = silent_exit
        parent = cmd_node.add_cmd("parent")
        parent.add_cmd("child", func=test_func)
        with pytest.raises(exception):
            cmd_node.run(['parent'])

    @pytest.mark.parametrize(
        "arg_name, exception",
        (
            ('--name', ValueError),
            ('-name', ValueError),
            ('name', None),
        )
    )
    def test_should_argument_starts_with_valid_string(self, arg_name, exception, test_func, cmd_node):
        cmd = cmd_node.add_cmd("execute", func=test_func)
        with mock.patch.object(cmd, "add_argument") as mocked_add:
            if exception is not None:
                with pytest.raises(exception):
                    cmd.argument(arg_name)
            else:
                cmd.argument(arg_name)
                mocked_add.assert_called_with(arg_name, help=None)

    @pytest.mark.parametrize(
        "arg_name, expected_name",
        (
                ('--name', '--name'),
                ('-name', '-name'),
                ('name', '--name'),
        )
    )
    def test_option_should_starts_with_hyphen(self, arg_name, expected_name, test_func, cmd_node):
        cmd = cmd_node.add_cmd("execute", func=test_func)
        with mock.patch.object(cmd, "add_argument") as mocked_add:
            cmd.option(arg_name)
            mocked_add.assert_called_with(expected_name, help=None)

    @pytest.mark.parametrize(
        "is_flag",
        (
                True,
                False,
        )
    )
    def test_option_should_work_with_is_flag(self, is_flag, test_func, cmd_node):
        cmd = cmd_node.add_cmd("execute", func=test_func)
        with mock.patch.object(cmd, "add_argument") as mocked_add:
            cmd.option("name", is_flag=is_flag)
            if is_flag:
                mocked_add.assert_called_with("--name", help=None, action="store_true")
            else:
                mocked_add.assert_called_with("--name", help=None)

    @pytest.mark.parametrize(
        "default",
        (
                None,
                1,
        )
    )
    def test_option_should_work_with_default_value(self, default, cmd_node):
        cmd = cmd_node.add_cmd("execute", func=test_func)
        with mock.patch.object(cmd, "add_argument") as mocked_add:
            cmd.option("name", default=default)
            if default is None:
                mocked_add.assert_called_with("--name", help=None)
            else:
                mocked_add.assert_called_with("--name", help=None, default=default)

    @pytest.mark.parametrize(
        "type_func, kwargs",
        (
            (mock.Mock(), {"help": None, "type": int}),
            (None, {"help": None}),
        )
    )
    def test_add_argument_work_with_type(
            self, type_func, kwargs, cmd_node
    ):
        if type_func is not None:
            type_func.return_value = {"type": int}
        with mock.patch.object(cmd_node, "add_argument") as mocked_add:
            cmd_node.argument("name", type=type_func)
            if type_func is not None:
                assert type_func.called
            mocked_add.assert_called_with("name", **kwargs)

    @pytest.mark.parametrize(
        "type_func, kwargs",
        (
                (mock.Mock(), {"help": None, "type": int}),
                (None, {"help": None}),
        )
    )
    def test_add_option_work_with_type(
            self, type_func, kwargs, cmd_node
    ):
        if type_func is not None:
            type_func.return_value = {"type": int}
        with mock.patch.object(cmd_node, "add_argument") as mocked_add:
            cmd_node.option("name", type=type_func)
            if type_func is not None:
                assert type_func.called
            mocked_add.assert_called_with("--name", **kwargs)
