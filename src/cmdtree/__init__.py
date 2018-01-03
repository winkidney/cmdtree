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
entry = env.entry

__all__ = (
    "argument",
    "option",
    "command",
    "group",
    "STRING",
    "INT",
    "FLOAT",
    "BOOL",
    "UUID",
    "Choices",
    "IntRange",
    "File",
    "entry",
)
