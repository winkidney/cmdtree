from functools import wraps

from cmdtree import echo
from cmdtree.exceptions import ParserError


def format_error(func):

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ParserError as e:
            echo.error("Error: %s" % str(e.format_error()))

    return wrapped