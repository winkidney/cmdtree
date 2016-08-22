from cmdtree.parser import AParser
from cmdtree.registry import env
from cmdtree.magic import (
    argument,
    option,
    command,
    group,
)

__all__ = (
    "entry",
    "env",
    "argument",
    "option",
    "command",
    "group",
)

env.parser = AParser()
entry = env.entry

