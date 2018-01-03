import sys

from cmdtree.exceptions import NodeDoesExist
from cmdtree.parser import CommandNode


def _mk_cmd_node(cmd_name, cmd_obj):
    return {
        "name": cmd_name,
        "cmd": cmd_obj,
        "children": {}
    }


class CmdTree(object):
    """
    A tree that manages the command references by cmd path like
    ['parent_cmd', 'child_cmd'].
    """

    def __init__(self, root_parser=None):
        """
        :type root_parser: cmdtree.parser.CommandNode
        """
        if root_parser is not None:
            root = root_parser
        else:
            root = CommandNode(
                cmd_path=sys.argv[:1]
            )
        self.root = {
            "name": root.name,
            "cmd": root,
            "children": {}
        }

    def get_cmd_by_path(self, existed_cmd_path):
        """
        :rtype: CommandNode
        """
        node = self.get_node_by_path(existed_cmd_path)
        return node['cmd']

    def get_node_by_path(self, existed_cmd_path):
        """
        :return:
        {
            "name": cmd_name,
            "cmd": Resource instance,
            "children": {}
        }
        """
        parent = self.root
        if len(existed_cmd_path) == 0:
            return self.root
        for cmd_name in existed_cmd_path:
            try:
                parent = parent['children'][cmd_name]
            except KeyError:
                raise NodeDoesExist(
                    "Given key [%s] in path %s does not exist in tree."
                    % (cmd_name, existed_cmd_path)
                )
        return parent

    def _add_node(self, cmd_node, cmd_path):
        """
        :type cmd_path: list or tuple
        """
        parent = self.root
        for cmd_key in cmd_path:
            if cmd_key not in parent['children']:
                break
            parent = parent['children'][cmd_key]
        parent["children"][cmd_node['name']] = cmd_node
        return cmd_node

    @staticmethod
    def _get_paths(full_path, end_index):
        if end_index is None:
            new_path, existed_path = [], full_path
        else:
            new_path, existed_path = full_path[end_index:], full_path[:end_index]
        return new_path, existed_path

    def add_commands(self, cmd_path, func, help=None):
        sub_command = CommandNode(
            cmd_path=cmd_path,
            func=func,
            help=help
        )
        node = _mk_cmd_node(sub_command.name, sub_command)
        self._add_node(node, cmd_path=cmd_path)
        return sub_command

    def add_parent_commands(self, cmd_path, help=None):
        """
        Create parent command object in cmd tree then return
        the last parent command object.
        :rtype: dict
        """
        existed_cmd_end_index = self.index_in_tree(cmd_path)
        new_path, existed_path = self._get_paths(
            cmd_path,
            existed_cmd_end_index,
        )
        parent_node = self.get_node_by_path(existed_path)

        last_one_index = 1
        new_path_len = len(new_path)
        _kwargs = {}
        for index, _ in enumerate(new_path):
            current_path = existed_path + new_path[:index + 1]
            parent_path = existed_path + new_path[:index]
            if last_one_index >= new_path_len:
                _kwargs['help'] = help
            sub_cmd = CommandNode(
                cmd_path=current_path,
                **_kwargs
            )
            parent_node = _mk_cmd_node(sub_cmd.name, sub_cmd)
            self._add_node(
                parent_node,
                parent_path,
            )
            last_one_index += 1
        return parent_node

    def index_in_tree(self, cmd_path):
        """
        Return the start index of which the element is not in cmd tree.
        :type cmd_path: list or tuple
        :return: None if cmd_path already indexed in tree.
        """
        current_tree = self.root
        for key in cmd_path:
            if key in current_tree['children']:
                current_tree = current_tree['children'][key]
            else:
                return cmd_path.index(key)
        return None
