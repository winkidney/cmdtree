def _get_cmd_path(path_prefix, cmd_name):
    if path_prefix is None:
        full_path = (cmd_name, )
    else:
        full_path = tuple(path_prefix) + (cmd_name, )
    return full_path


def _get_func_name(func):
    assert callable(func)
    return func.__name__