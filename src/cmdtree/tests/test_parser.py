import pytest
import six

from cmdtree import parser
from cmdtree.exceptions import ArgumentParseError


def mk_obj(property_dict):
    class TestObject(object):
        pass
    obj = TestObject()
    for key, value in six.iteritems(property_dict):
        setattr(obj, key, value)
    return obj


@pytest.fixture()
def aparser():
    from cmdtree.parser import AParser
    return AParser()


@pytest.fixture()
def test_func():
    def func():
        return "result"
    return func


@pytest.mark.parametrize(
    "p_dict, expected",
    (
            ({"_k": "v", "k": "v"}, {"k": "v"}),
            ({"__k": "v", "k": "v"}, {"k": "v"}),
            ({"k1": "v", "k": "v"}, {"k": "v", "k1": "v"}),
    )
)
def test_vars_should_return_right_dict(p_dict, expected):
    obj = mk_obj(p_dict)
    assert parser.vars_(
        obj
    ) == expected


class TestAParser:
    def test_should_execute_func(self, aparser, test_func):
        aparser.add_cmd("test", func=test_func)
        assert aparser.run(["test"]) == "result"

    def test_should_execute_child_cmd(self, aparser, test_func):
        parent = aparser.add_cmd("parent")
        parent.add_cmd("child", func=test_func)
        assert aparser.run(['parent', 'child']) == "result"

    @pytest.mark.parametrize(
        "silent_exit, exception",
        (
                (False, ArgumentParseError),
                (True, SystemExit)
        )
    )
    def test_should_parent_cmd_exit_or_raise_error(self, silent_exit, exception, test_func, aparser):
        from cmdtree.env import env
        env.silent_exit = silent_exit
        parent = aparser.add_cmd("parent")
        parent.add_cmd("child", func=test_func)
        with pytest.raises(exception):
            aparser.run(['parent'])