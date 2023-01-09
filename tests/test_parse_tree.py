import pytest

from pylfg import LFGParseTree, LFGParseTreeNode

def test_parse_tree_node():
    # Test the creation of a parse tree node
    node = LFGParseTreeNode('NP', 'cat')
    assert node.label == 'NP'
    assert node.token == 'cat'
    assert not node.is_leaf()
    
    # Test the creation of a leaf node
    leaf_node = LFGParseTreeNode('N', 'cat')
    assert leaf_node.is_leaf()
    
    # Test the creation of a parse tree with a single node
    tree = LFGParseTree(node)
    assert tree.root == node
    assert not tree.is_valid()  # The tree should not be considered valid yet
    
    # Test the addition of children to the node
    node.add_child(leaf_node)
    assert tree.is_valid()  # The tree should now be considered valid

def test_parse_tree_from_string(test_sentences):
    # Test the creation of a parse tree from a string representation
    for sentence, string in test_sentences:
        tree = LFGParseTree.from_string(string)
        assert tree.to_string() == string
        
def test_parse_tree_to_string(test_sentences):
    # Test the conversion of a parse tree to a string representation
    for sentence, string in test_sentences:
