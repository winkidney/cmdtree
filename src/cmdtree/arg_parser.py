from copy import deepcopy
import sys

from cmdtree.exceptions import NodeDoesExist, NoSuchCommand
from cmdtree.tree import get_help


class RawArgsParser(object):

    def __init__(self, args, tree):
        """
        :type args: list[str]
        :type tree: cmdtree.tree.CmdTree
        """
        self.raw_args = args
        self.tree = tree
        self.cmd_nodes = []

    @staticmethod
    def parse2cmd(raw_args, tree):
        cmd_nodes = []
        full_cmd_path = []
        left_args = deepcopy(raw_args)
        cmd_start_index = 0
        while True:
            cmd2find = left_args[cmd_start_index:cmd_start_index + 1]
            cmd_path2find = full_cmd_path + cmd2find
            try:
                node = tree.get_node_by_path(cmd_path2find)
            except NodeDoesExist:
                raise NoSuchCommand(
                    "Command %s does not exist."
                    % str(
                        full_cmd_path[0]
                        if full_cmd_path
                        else sys.argv[0]
                    )
                )
            cmd = node['cmd']
            left_args = left_args[cmd_start_index + 1:]
            index_offset, left_args = cmd.parse_args(
                left_args,
            )
            full_cmd_path = cmd_path2find
            cmd_nodes.append(node)
            if len(left_args) <= 0:
                break
        return cmd_nodes, full_cmd_path

    def run(self):
        self.cmd_nodes, cmd_path = self.parse2cmd(self.raw_args, self.tree)
        kwargs = {}
        for node in self.cmd_nodes:
            kwargs.update(
                node['cmd'].kwargs
            )
        node = self.cmd_nodes[-1]
        cmd = node['cmd']
        if cmd.callable():
            cmd.run(kwargs)
        get_help(node)

