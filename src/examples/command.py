from cmdtree import INT
from cmdtree import command, argument, option


@argument("host", help="server listen address")
@option("reload", is_flag=True, help="if auto-reload on")
@option("port", help="server port", type=INT, default=8888)
@command(help="run a http server on given address")
def run_server(host, reload, port):
    print(
        "Your server running on {host}:{port}, auto-reload is {reload}".format(
            host=host,
            port=port,
            reload=reload
        )
    )

if __name__ == "__main__":
    from cmdtree import entry
    entry()