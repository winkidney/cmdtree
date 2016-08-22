class ENV(object):
    __slots__ = (
        "silent_exit",
        "parser",
        "entry",
        "tree"
    )

    def __init__(self):
        """
        :type parser: cmdtree.parser.AParser
        """
        self.silent_exit = True
        self.tree = None
        self.entry = lambda *args, **kwargs: self.tree.root.run(*args, **kwargs)

env = ENV()