from cmdtree import command, argument, INT, entry, Choices


@command("run")
@argument("host", type=Choices(("host1", "host2", "host3")))
@argument("port", type=INT)
def run_docker(host, port):
    print(
        "docker daemon api runs on {ip}:{port}".format(
            ip=host,
            port=port,
        )
    )


if __name__ == "__main__":
    entry()