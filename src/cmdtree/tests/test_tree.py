from copy import deepcopy

import pytest
from mock import mock


@pytest.fixture
def cmd_node():
    return {
        "name": "new_cmd",
        "cmd": "cmd_obj",
        "children": {}
    }


@pytest.fixture
def cmd_node2():
    return {
        "name": "child_cmd",
        "cmd": "cmd_obj",
        "children": {}
    }


@pytest.fixture
def cmd_tree(mocked_resource):
    from cmdtree.tree import CmdTree
    return CmdTree(mocked_resource)


@pytest.fixture
def mocked_resource():
    return mock.Mock()


@pytest.fixture
def cmd_tree_with_tree(cmd_tree, cmd_node, cmd_node2):
    cmd_tree._add_node(cmd_node, ['new_cmd'])
    cmd_tree._add_node(cmd_node2, ['new_cmd', 'child_cmd'])
    return cmd_tree


class TestCmdTree:
    def test_should_cmd_tree_gen_right_node(
            self
    ):
        from cmdtree.tree import _mk_cmd_node
        ret = _mk_cmd_node("cmd", "cmd_obj")
        assert ret == {
            "name": "cmd",
            "cmd": "cmd_obj",
            "children": {}
        }

    def test_should_cmd_tree_add_node_create_right_index(
            self, cmd_tree, mocked_resource, cmd_node, cmd_node2
    ):
        cmd_tree._add_node(cmd_node, ['new_cmd'])
        assert cmd_tree.tree == {
            "name": "root",
            "cmd": mocked_resource,
            "children": {"new_cmd": cmd_node}
        }

        cmd_tree._add_node(cmd_node2, ['new_cmd', 'child_cmd'])
        expected_cmd_node = deepcopy(cmd_node)
        expected_cmd_node['children']['child_cmd'] = cmd_node2
        assert cmd_tree.tree == {
            "name": "root",
            "cmd": mocked_resource,
            "children": {"new_cmd": expected_cmd_node}
        }

    def test_should_cmd_tree_get_cmd_by_path_get_parent(
            self, cmd_tree_with_tree, cmd_node, cmd_node2
    ):
        tree = cmd_tree_with_tree
        ret = tree.get_cmd_by_path(['new_cmd'])
        expected_cmd_node = deepcopy(cmd_node)
        expected_cmd_node['children']['child_cmd'] = cmd_node2
        assert ret == expected_cmd_node

    def test_should_cmd_tree_get_cmd_by_path_get_child(
            self, cmd_tree_with_tree, cmd_node2
    ):
        tree = cmd_tree_with_tree
        ret = tree.get_cmd_by_path(['new_cmd', 'child_cmd'])
        assert ret == cmd_node2

    @pytest.mark.parametrize(
        "full_path, end_index, result",
        (
                (
                        [1, 2, 3],
                        1,
                        ([2, 3], [1, ]),
                ),
                (
                        [1, 2, 3],
                        None,
                        ([], [1, 2, 3]),
                ),
        )
    )
    def test_get_paths_should_work_as_expected(self, full_path, end_index, result, cmd_tree):
        assert cmd_tree._get_paths(full_path, end_index) == result

    def test_should_cmd_tree_index_in_tree_get_right_index(
            self, cmd_tree_with_tree
    ):
        tree = cmd_tree_with_tree
        ret = tree.index_in_tree(['new_cmd', 'child_cmd'])
        assert ret is None
        assert tree.index_in_tree(['new_cmd']) is None
        ret = tree.index_in_tree(['new_cmd', 'hello'])
        assert ret == 1
        assert tree.index_in_tree(['child_cmd']) == 0
        assert tree.index_in_tree(['another_cmd_not_exist']) == 0

    def test_should_cmd_tree_add_parent_commands_return_the_last(
            self,
            cmd_tree
    ):
        cmd_tree.add_parent_commands(['new_cmd', 'hello'])
        assert "hello" in \
               cmd_tree.tree['children']['new_cmd']['children']
        assert {} == \
               cmd_tree.tree['children']['new_cmd']['children']["hello"]['children']

    def test_should_cmd_tree_get_cmd_by_path_got_obj(
            self, cmd_tree_with_tree
    ):
        assert cmd_tree_with_tree.get_cmd_by_path(['new_cmd']) is not None
        assert cmd_tree_with_tree.get_cmd_by_path(
            ['new_cmd', "child_cmd"]) is not None
        with pytest.raises(ValueError) as excinfo:
            cmd_tree_with_tree.get_cmd_by_path(['new_cmd', "fuck"])
        msg = "Given key [fuck] in path ['new_cmd', 'fuck'] does not exist in tree."
        assert str(excinfo.value) == msg

    def test_should_add_parent_cmd_not_repeat_add(self, cmd_tree_with_tree):
        orig_node = cmd_tree_with_tree.add_parent_commands(['test_nested', 'child'])
        new_node = cmd_tree_with_tree.add_parent_commands(['test_nested', 'child'])
        assert id(orig_node['cmd']) == id(new_node['cmd'])