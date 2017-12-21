import pytest

from cmdtree import utils


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
    assert utils.get_cmd_path(
        path_prefix, cmd_name
    ) == expected
