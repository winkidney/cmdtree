import mock
import pytest

from cmdtree import shortcuts


@pytest.fixture()
def do_nothing():

    def func():
        pass

    return func


@pytest.fixture()
def mocked_parser():
    return mock.Mock()


@pytest.fixture()
def mocked_meta_cmd():
    meta_cmd = mock.Mock()
    return meta_cmd


@pytest.mark.parametrize(
    "path_prefix, cmd_name, expected",
    (
        (
            ["parent", "child"],
            "execute",
            ["parent", "child", "execute"]
        ),
        (None, "execute", ["execute"]),
    )
)
def test_get_cmd_path(path_prefix, cmd_name, expected):
    assert shortcuts._get_cmd_path(
        path_prefix, cmd_name
    ) == expected


class TestMkGroup:
    def test_should_return_group_with_group(self, do_nothing):

        assert isinstance(
            shortcuts._mk_group("hello")(do_nothing),
            shortcuts.Group
        )

    def test_should_raise_value_error_if_group_inited(
            self, do_nothing, mocked_parser
    ):

        group = shortcuts.Group(do_nothing, "test", mocked_parser)

        with pytest.raises(ValueError):
            shortcuts._mk_group("test")(group)

    def test_should_get_func_name_called_if_no_name_given(
            self, do_nothing
    ):
        with mock.patch.object(
                shortcuts, "_get_func_name"
        ) as mocked_get_name:
            shortcuts._mk_group(None)(do_nothing)
            assert mocked_get_name.called

    def test_should_call_apply2parser_for_meta_cmd(
            self, do_nothing
    ):

        with mock.patch.object(
                shortcuts, "_apply2parser",
        ) as apply2parser:
            cmd_proxy = shortcuts.CmdProxy(do_nothing)
            shortcuts._mk_group("name")(cmd_proxy)
            assert apply2parser.called
