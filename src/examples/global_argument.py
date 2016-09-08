from cmdtree import command

from cmdtree import entry, env
env.root.argument("host", help="server listen address")


@command(help="run a http server on given address")
def run_server(host):
    print(
        "Your server running on {host}".format(
            host=host,
        )
    )

if __name__ == "__main__":

    entry()