import pytest
from cmdtree import INT
from cmdtree import command, argument, option


@argument("host", help="server listen address")
@option("reload", is_flag=True, help="if auto-reload on")
@option("port", help="server port", type=INT, default=8888)
@command(help="run a http server on given address")
def run_server(host, reload, port):
    return host, port, reload


@command(help="run a http server on given address")
@argument("host", help="server listen address")
@option("port", help="server port", type=INT, default=8888)
def order(port, host):
    return host, port


def test_should_return_given_argument():
    from cmdtree import entry
    result = entry(
        ["run_server", "host", "--reload", "--port", "8888"]
    )
    assert result == ("host", 8888, True)


def test_should_reverse_decorator_order_has_no_side_effect():
    from cmdtree import entry
    result = entry(
        ["order", "host", "--port", "8888"]
    )
    assert result == ("host", 8888)