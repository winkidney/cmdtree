from cmdtree import group, argument, entry


@group("docker")
@argument("ip")
def docker():
    pass


@docker.command("run")
@argument("container-name")
def run(ip, container_name):
    print(
        "container [{name}] on host [{ip}]".format(
            ip=ip,
            name=container_name,
        )
    )

if __name__ == "__main__":
    entry()