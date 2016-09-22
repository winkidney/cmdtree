from cmdtree import group, argument, entry


@group("fake-docker", "fake-docker command binds")
def fake_docker():
    pass


@group("docker", "docker command binds")
@argument("ip", help="docker daemon ip addr")
def docker():
    pass


# nested command
@docker.command("run", help="run docker command")
@argument("container-name")
def run(ip, container_name):
    print(
        "container [{name}] on host [{ip}]".format(
            ip=ip,
            name=container_name,
        )
    )


# nested command group
@docker.group("image", help="image operation")
def image():
    pass


@image.command("create")
@argument("name")
def image_create(ip, name):
    print(
        "iamge {name} on {ip} created.".format(
            ip=ip,
            name=name,
        )
    )


if __name__ == "__main__":
    entry()