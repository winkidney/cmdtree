# coding: utf-8
from argparse import ArgumentTypeError

import mock
import pytest

from cmdtree import types


class TestParamTypeFactory:

    def setup_method(self, method):
        self.instance = types.ParamTypeFactory()

    def test_should_call_return_argparse_kwargs(self):
        assert self.instance() == {"type": self.instance.convert}

    def test_should_subclass_raise_not_implement_error(self):
        with pytest.raises(NotImplementedError):
            self.instance.convert("value")

    def test_should_fail_raise_argument_type_error(self):
        with pytest.raises(ArgumentTypeError) as e:
            self.instance.fail("msg")
        assert str(e.value) == "msg"


@pytest.mark.parametrize(
    "value, expected",
    (
        (True, True),
        ("value", "value"),
        (1, 1),
    )
)
def test_should_unprocessed_return_unprocessed_param(
        value, expected
):
    assert types.UnprocessedParamType().convert(value) == expected


@pytest.mark.parametrize(
    "value, expected, argv_encode, fs_encode",
    (
        (True, True, None, None),
        ("value", "value", None, None),
        (1, 1, None, None),
        (b"value", "value", None, None),
        (u"value", "value", None, None),
        (u"中文".encode("utf-8"), u"中文", None, None),
        (u"中文".encode("gbk"), u"中文", "gbk", "gbk"),
        (u"中文".encode("gbk"), u"中文", "utf-8", "gbk"),
        (u"中文".encode("gbk"), u"中文", "utf-8", "gb2312"),
    )
)
def test_should_string_param_return_always_unicode_if_is_string(
        value, expected, argv_encode, fs_encode
):
    if argv_encode is None:
        argv_encode = "utf-8"
    if fs_encode is None:
        fs_encode = "utf-8"
    mocked_argv = mock.Mock()
    mocked_fs = mock.Mock()
    mocked_argv.return_value = argv_encode
    mocked_fs.return_value = fs_encode
    pathcer1 = mock.patch.object(types, "_get_argv_encoding", mocked_argv)
    pathcer2 = mock.patch.object(types, "get_filesystem_encoding", mocked_fs)
    pathcer1.start()
    pathcer2.start()
    assert types.StringParamType().convert(value) == expected
    pathcer1.stop()
    pathcer2.stop()


class TestIntParamType:
    @pytest.mark.parametrize(
        "value, expected",
        (
            (1, 1),
            ("1", 1),
            (True, 1),
            (False, 0),
        )
    )
    def test_should_get_int(self, value, expected):
        assert types.INT.convert(value) == expected

    @pytest.mark.parametrize(
        "value",
        (
                "1.1",
                "hello",
        )
    )
    def test_should_fail_called(self, value):
        with mock.patch.object(
                types.INT, "fail"
        ) as mocked_fail:
            types.INT.convert(value)
            assert mocked_fail.called


class TestIntRange:
    @pytest.mark.parametrize(
        "value, min, max, clamp, expected",
        (
            (5, 1, 10, False, 5),
            (1, 1, 10, False, 1),
            (10, 1, 10, False, 10),
            (10, 1, None, False, 10),
            (0, None, 10, False, 0),
            (11, 1, 10, True, 10),
            (0, 1, 10, True, 1),
        )
    )
    def test_should_return_value(self, value, min, max, clamp, expected):
        instance = types.IntRange(min=min, max=max, clamp=clamp)
        assert instance.convert(value) == expected

    @pytest.mark.parametrize(
        "value, min, max, clamp",
        (
                (11, 1, 10, False),
                (0, 1, 10, False),
                (11, None, 10, False),
                (0, 1, None, False),
        )
    )
    def test_should_fail(self, value, min, max, clamp):
        instance = types.IntRange(min=min, max=max, clamp=clamp)
        with mock.patch.object(
            instance, "fail"
        ) as mocked_fail:
            instance.convert(value)
            assert mocked_fail.called


class TestBoolParamType:
    @pytest.mark.parametrize(
        "value, expected",
        (
            ('True', True),
            ('true', True),
            ('yes', True),
            ('y', True),
            ('1', True),
            ('false', False),
            ('0', False),
            ('no', False),
            ('n', False),
            (True, True),
            (False, False),
        )
    )
    def test_should_return_bool(self, value, expected):
        assert types.BOOL.convert(value) == expected

    @pytest.mark.parametrize(
        "value",
        (
            "Failed",
        )
    )
    def test_should_fail(self, value):
        with mock.patch.object(
                types.BOOL, "fail"
        ) as mocked_fail:
            types.BOOL.convert(value)
            assert mocked_fail.called


class TestFloatParamType:

    @pytest.mark.parametrize(
        "value, expected",
        (
            ("1.1", 1.1),
            ("1", 1),
            (".1", 0.1),
        )
    )
    def test_should_return_float(self, value, expected):
        assert types.FLOAT.convert(value) == expected

    @pytest.mark.parametrize(
        "value, expected",
        (
                ("2.x", 1.222),
                ("hi", 0.1),
        )
    )
    def test_should_fail(self, value, expected):
        with mock.patch.object(
                types.FLOAT, "fail"
        ) as mocked_fail:
            types.FLOAT.convert(value)
            assert mocked_fail.called


def test_should_convert_return_file_type():
    f = types.File(mode="w")
    assert hasattr(f.convert("/tmp/tmp.log"), "read")


class TestChoices:

    @pytest.mark.parametrize(
        "choices, type_",
        (
            (["hello", 1, "hello"], None),
            ([3, 1, 2], types.INT)
        )
    )
    def test_should_return_keyword_argument(self, choices, type_):
        instance = types.Choices(choices, type=type_)

        assert instance() == {
            "type": type_ or instance.convert,
            "choices": choices
        }