

class ENV(object):
    __slots__ = (
        "silent_exit",
        "entry",
    )

    def __init__(self):
        self.silent_exit = True

env = ENV()