from cmdtree import group, argument, entry


@group("docker")
@argument("ip")
def docker():
    pass


# nested command
@docker.command("run")
@argument("container-name")
def run(ip, container_name):
    print(
        "container [{name}] on host [{ip}]".format(
            ip=ip,
            name=container_name,
        )
    )


# nested command group
@docker.group("image")
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