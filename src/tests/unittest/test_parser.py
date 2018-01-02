import pytest
import six

from cmdtree.parser import CommandNode
from cmdtree.constants import ROOT_NODE_NAME


def mk_obj(property_dict):
    class TestObject(object):
        pass
    obj = TestObject()
    for key, value in six.iteritems(property_dict):
        setattr(obj, key, value)
    return obj


@pytest.fixture()
def cmd_node():
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


class TestCmdNode:
    def test_should_execute_func(self, test_func):
        cmd_node = CommandNode(
            ROOT_NODE_NAME,
            cmd_path=[ROOT_NODE_NAME, ],
            func=test_func,
        )
        assert cmd_node.run({}) == "result"
