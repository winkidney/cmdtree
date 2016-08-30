from cmdtree.tree import CmdTree

tree = CmdTree()


def index():
    print("Hi, you have 10 disks in your computer...")


def show(disk_id):
    print("This is disk %s" % disk_id)


def delete(disk_id):
    print("disk %s deleted" % disk_id)


# Add list command
tree.add_commands(["computer", "list"], index)

# get the parser in any place, any time
tree.add_commands(["computer", "show"], show)
tree_node = tree.get_cmd_by_path(["computer", "show"])
show_parser = tree_node['cmd']
show_parser.argument("disk_id")

# Add delete command
delete3 = tree.add_commands(["computer", "delete"], delete)
delete3.argument("disk_id")

# run your tree
tree.root.run()