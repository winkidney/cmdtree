def test_get_tree_always_get_the_same_one():
    from cmdtree.registry import env
    from cmdtree.tree import CmdTree
    tree1 = env.tree
    tree2 = env.tree
    assert isinstance(tree1, CmdTree)
    assert tree1 is tree2