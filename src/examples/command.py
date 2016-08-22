from cmdtree import command, argument, option


@argument("name", help="your name here")
@option("like-apple", is_flag=True, help="whether you like apple")
@command("hello")
def output(name, like_apple):
    print("Hello {0}, be happy to use CmdTree:)".format(name))
    print("You tells me that whether you like apple is {0}".format(like_apple))

if __name__ == "__main__":
    from cmdtree import entry
    entry()