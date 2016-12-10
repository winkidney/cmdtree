from cmdtree import Choices
from cmdtree import command
from cmdtree import group, argument, entry
from cmdtree import option


@group("docker")
@argument("ip")
def docker():
    pass


@docker.group("image")
def image():
    pass


@image.command("create")
@argument("name")
def image_create(ip, name):
    return ip, name


@docker.command("run")
@argument("container-name")
def run(ip, container_name):
    return ip, container_name


def test_docker_run():
    assert entry(
        ["docker", "0.0.0.0", "run", "container1"]
    ) == ("0.0.0.0", "container1")


def test_nested_group_works():
    assert entry(
        ["docker", "0.0.0.0", "image", "create", "test_image"]
    ) == ("0.0.0.0", "test_image")


def test_should_double_option_order_do_not_cause_calling_error():

    @command("test_order")
    @option("feed", type=Choices(("kline", "fake")), default="fake")
    @option("config", help="config file path for kline database")
    def hello(feed, config):
        return feed

    assert entry(
        ["test_order", "--feed", "fake"]
    ) == "fake"
