import sys


class ENV(object):
    __slots__ = (
        "silent_exit",
        "parser",
        "_tree",
    )

    def __init__(self):
        """
        :type parser: cmdtree.parser.CommandNode
        """
        self.silent_exit = True
        self._tree = None

    def entry(self, args=None):
        from cmdtree.parser import RawArgsParser

        if args is None:
            args = sys.argv[1:]
        parser = RawArgsParser(args, self.tree)
        return parser.run()

    @property
    def tree(self):
        """
        :rtype: cmdtree.tree.CmdTree
        """
        from cmdtree.tree import CmdTree
        if self._tree is None:
            self._tree = CmdTree()
        return self._tree

    @property
    def root(self):
        return self.tree.root

env = ENV()