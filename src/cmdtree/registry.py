class ENV(object):
    __slots__ = (
        "silent_exit",
        "parser",
        "entry",
        "tree",
        "_tree",
        "root",
    )

    def __init__(self):
        """
        :type parser: cmdtree.parser.AParser
        """
        self.silent_exit = True
        self._tree = None
        self.entry = lambda args=None, namespace=None: self.tree.root.run(args, namespace)

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