import mock
import pytest

from cmdtree import shortcuts


@pytest.fixture()
def do_nothing():

    def func(*args, **kwargs):
        return "do_nothing"

    return func


@pytest.fixture()
def mocked_parser():
    return mock.Mock()


@pytest.fixture()
def parser_proxy():
    return shortcuts.ParserProxy()


@pytest.fixture()
def group(mocked_parser, do_nothing):
    return shortcuts.Group(
        do_nothing,
        "do_nothing",
        mocked_parser,
        full_path=["do_nothing", ]
    )


@pytest.fixture()
def cmd(mocked_parser, do_nothing):
    return shortcuts.Cmd(
        do_nothing,
        "do_nothing",
        mocked_parser,
        full_path=["do_nothing", ]
    )


@pytest.mark.parametrize(
    "path_prefix, cmd_name, expected",
    (
        (
            ("parent", "child"),
            "execute",
            ("parent", "child", "execute")
        ),
        (
            ["parent", "child"],
            "execute",
            ("parent", "child", "execute")
        ),
        (None, "execute", ("execute", )),
    )
)
def test_get_cmd_path(path_prefix, cmd_name, expected):
    assert shortcuts._get_cmd_path(
        path_prefix, cmd_name
    ) == expected


def test_should_apply2user_called_correctly(mocked_parser):
    option = mocked_parser.option = mock.Mock()
    argument = mocked_parser.argument = mock.Mock()
    shortcuts._apply2parser(
        [["cmd1", {}], ],
        [["cmd1", {}], ["cmd1", {}], ],
        mocked_parser
    )
    assert option.call_count == 2
    assert argument.call_count == 1


@pytest.mark.parametrize(
    "cmd_proxy, expected",
    (
        (shortcuts.CmdProxy(lambda x: x), True),
        (lambda x: x, False),
    )
)
def test_should_apply2parser_be_called_with_cmd_proxy(
        cmd_proxy, expected, mocked_parser,
):
    with mock.patch.object(
            shortcuts, "_apply2parser"
    ) as mocked_apply:
        shortcuts.apply2parser(cmd_proxy, mocked_parser)
        assert mocked_apply.called is expected


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
                shortcuts, "apply2parser",
        ) as apply2parser:
            cmd_proxy = shortcuts.CmdProxy(do_nothing)
            shortcuts._mk_group("name")(cmd_proxy)
            assert apply2parser.called


class TestMkCmd:
    def test_should_return_cmd_with_cmd(self, do_nothing):

        assert isinstance(
            shortcuts._mk_cmd("hello")(do_nothing),
            shortcuts.Cmd
        )

    def test_should_raise_value_error_if_cmd_inited(
            self, do_nothing, mocked_parser
    ):

        cmd = shortcuts.Cmd(do_nothing, "test", mocked_parser)

        with pytest.raises(ValueError):
            shortcuts._mk_cmd("test")(cmd)

    def test_should_get_func_name_called_if_no_name_given(
            self, do_nothing
    ):
        with mock.patch.object(
                shortcuts, "_get_func_name"
        ) as mocked_get_name:
            shortcuts._mk_cmd(None)(do_nothing)
            assert mocked_get_name.called

    def test_should_call_apply2parser_for_meta_cmd(
            self, do_nothing
    ):

        with mock.patch.object(
                shortcuts, "apply2parser",
        ) as apply2parser:
            cmd_proxy = shortcuts.CmdProxy(do_nothing)
            shortcuts._mk_cmd("name")(cmd_proxy)
            assert apply2parser.called


def test_cmd_meta_should_handle_none_value_of_path_to_tuple():
    cmd_meta = shortcuts.CmdMeta()
    assert cmd_meta.full_path == tuple()


class TestParserProxy:
    def test_should_option_add_options(self, parser_proxy):
        parser_proxy.option("name", help="help")
        assert parser_proxy.options == [(
            ("name", ), {"help": "help"}
        )]

    def test_should_argument_add_options(self, parser_proxy):
        parser_proxy.argument("name", help="help")
        assert parser_proxy.arguments == [(
            ("name", ), {"help": "help"}
        )]


class TestGroup:
    def test_should_group_instance_call_func(self, group):
        assert group() == "do_nothing"

    def test_should_full_path_be_none_if_path_is_none(self, group):
        assert group.meta.full_path == ("do_nothing", )

    def test_should_command_call_mk_command(self, group):
        with mock.patch.object(
                shortcuts, "_mk_cmd"
        ) as mocked_mk:
            group.command("name")
            mocked_mk.assert_called_with(
                "name",
                help=None,
                path_prefix=("do_nothing", )
            )

    def test_should_group_call_mk_group(self, group):
        with mock.patch.object(
                shortcuts, "_mk_group"
        ) as mocked_mk:
            group.group("name")
            mocked_mk.assert_called_with(
                "name",
                help=None,
                path_prefix=("do_nothing", )
            )


class TestCmd:
    def test_should_cmd_instance_call_func(self, cmd):
        assert cmd() == "do_nothing"

    def test_should_full_path_be_none_if_path_is_none(self, cmd):
        assert cmd.meta.full_path == ("do_nothing", )


def test_get_func_name(do_nothing):
    assert shortcuts._get_func_name(do_nothing) == "func"