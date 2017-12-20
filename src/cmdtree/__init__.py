from cmdtree.parser import CommandNode
from cmdtree.registry import env
from cmdtree.shortcuts import (
    argument,
    option,
    command,
    group,
)

# parameter type support
from cmdtree.types import (
    STRING,
    INT,
    FLOAT,
    BOOL,
    UUID,
    Choices,
    IntRange,
    File,
)

# globals and entry point
# env.parser = CommandNode()
entry = env.entry

