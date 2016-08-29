from cmdtree.parser import AParser
from cmdtree.tree import CmdTree

tree = CmdTree(AParser())


def func1():
    print("Hi, this is cmd1")


def func2(name):
    print("Hi {0}, this is cmd2".format(name))


def func3(name):
    print("Hi {name}, this is cmd3")


parser1 = tree.add_commands(["root", "cmd1"], func1)
tree.add_commands(["root", "cmd2"], func2)

parser2 = tree.get_cmd_by_path(["root", "cmd2"])['cmd']
parser2.argument("name", help="your name here")

parser3 = tree.add_commands(["root", "child", "cmd3"], func3)
parser3.argument("name", help="your name here")

tree.root.run()