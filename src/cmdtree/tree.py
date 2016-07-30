
class Node(object):
    def __init__(self, name, cmd, children):
        self.name = name
        self.cmd = cmd
        self.children = children

    def as_dict(self):
        return {
            "name": self.name,
            "cmd": self.cmd,
            "children": self.children
        }


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

    def __init__(self, root_parser):
        """
        :type root_parser: cmdtree.parser.AParser
        """
        self.root = root_parser
        self.tree = {
            "name": "root",
            "cmd": self.root,
            "children": {}
        }

    def get_cmd_by_path(self, existed_cmd_path):
        """
        :return:
        {
            "name": cmd_name,
            "cmd": Resource instance,
            "children": {}
        }
        """
        parent = self.tree
        for cmd_name in existed_cmd_path:
            try:
                parent = parent['children'][cmd_name]
            except KeyError:
                raise ValueError(
                    "Given key [%s] in path %s does not exist in tree."
                    % (cmd_name, existed_cmd_path)
                )
        return parent

    def _add_node(self, cmd_node, cmd_path):
        """
        :type cmd_path: list or tuple
        """
        parent = self.tree
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

    def add_commands(self, cmd_path, func):
        parent = self._add_parent_commands(cmd_path[:-1])
        return parent['cmd'].add_cmd(name=cmd_path[-1], func=func)

    def _add_parent_commands(self, cmd_path):
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
        parent_node = self.get_cmd_by_path(existed_path)
        for cmd_name in new_path:
            sub_cmd = parent_node['cmd'].add_cmd(
                cmd_name, cmd_name
            )
            parent_node = _mk_cmd_node(cmd_name, sub_cmd)
            self._add_node(
                parent_node,
                existed_path + new_path[:new_path.index(cmd_name)]
            )
        return parent_node

    def index_in_tree(self, cmd_path):
        """
        Return the start index of which the element is not in cmd tree.
        :type cmd_path: list or tuple
        :return: None if cmd_path already indexed in tree.
        """
        current_tree = self.tree
        for key in cmd_path:
            if key in current_tree['children']:
                current_tree = current_tree['children'][key]
            else:
                return cmd_path.index(key)
        return None
