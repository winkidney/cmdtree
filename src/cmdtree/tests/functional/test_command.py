import pytest
from cmdtree import INT, entry
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


def test_should_option_order_not_cause_argument_miss():

    from cmdtree import entry

    @command("test_miss")
    @option("kline")
    @argument("script_path", help="file path of python _script")
    def run_test(script_path, kline):
        return script_path, kline

    assert entry(
        ["test_miss", "path", "--kline", "fake"]
    ) == ("path", "fake")


def test_should_double_option_order_do_not_cause_calling_error():

    @command("test_order")
    @option("feed")
    @option("config", help="config file path for kline database")
    def hello(feed, config):
        return feed

    assert entry(
        ["test_order", "--feed", "fake"]
    ) == "fake"