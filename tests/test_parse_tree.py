import pytest
from PyLFG.parse_tree import LFGParseTreeNode, LFGParseTree, FStructure
from PyLFG import parser, parse_tree

def test_LFGParseTreeNode_init():
    tree = LFGParseTreeNode("label", "token", {"key": "value"}, [])
    assert tree.label == "label"
    assert tree.token == "token"
    assert tree.functional_labels == {"key": "value"}
    assert tree.children == []
    
def test_LFGParseTreeNode_add_child():
    tree = LFGParseTreeNode("label", "token", {"key": "value"}, [])
    child = LFGParseTreeNode("child", "child_token", {"child_key": "child_value"}, [])
    tree.add_child(child)
    assert tree.children == [child]

def test_LFGParseTreeNode_add_functional_label():
    tree = LFGParseTreeNode("label", "token", {"key": "value"}, [])
    tree.add_functional_label("new_key", "new_value")
    assert tree.functional_labels == {"key": "value", "new_key": "new_value"}

def test_LFGParseTreeNode_get_functional_label():
    tree = LFGParseTreeNode("label", "token", {"key": "value"}, [])
    assert tree.get_functional_label("key") == "value"
    assert tree.get_functional_label("non_existing_key") == None

def test_LFGParseTreeNode_remove_functional_label():
    tree = LFGParseTreeNode("label", "token", {"key": "value"}, [])
    tree.remove_functional_label("key")
    assert tree.functional_labels == {}

def test_LFGParseTreeNode_get_all_functional_labels():
    tree = LFGParseTreeNode("label", "token", {"key": "value"}, [])
    assert tree.get_all_functional_labels() == {"key": "value"}

def test_LFGParseTreeNode_has_functional_label():
    tree = LFGParseTreeNode("label", "token", {"key": "value"}, [])
    assert tree.has_functional_label("key") == True
    assert tree.has_functional_label("non_existing_key") == False

def test_LFGParseTreeNodeF_attributes():
    node = parse_tree.LFGParseTreeNodeF("NP", "cat", {"NOUN": "cat"})
    assert node.label == "NP"
    assert node.token == "cat"
    assert node.get_functional_label("NOUN") == "cat"
    assert node.has_functional_label("NOUN") == True
    assert node.get_all_functional_labels() == {"NOUN": "cat"}
    node.add_functional_label("TEST", "test")
    assert node.get_functional_label("TEST") == "test"
    assert node.has_functional_label("TEST") == True
    assert node.get_all_functional_labels() == {"NOUN": "cat", "TEST": "test"}
    node.remove_functional_label("NOUN")
    assert node.has_functional_label("NOUN") == False
    assert node.get_all_functional_labels() == {"TEST": "test"}

def test_LFGParseTreeNodeF_f_structure():
    node = parse_tree.LFGParseTreeNodeF("NP", "cat")
    assert node.get_all_f_structure() == {}
    node.add_to_f_structure("NOUN", "cat")
    assert node.get_from_f_structure("NOUN") == "cat"
    assert node.has_in_f_structure("NOUN") == True
    assert node.get_all_f_structure() == {"NOUN": "cat"}
    node.remove_from_f_structure("NOUN")
    assert node.has_in_f_structure("NOUN") == False
    assert node.get_all_f_structure() == {}
    
    
def test_LFGParseTreeNodeF_parse():
    grammar = parser.load_grammar("/EN/grammar.txt")
    lexicon = parser.load_lexicon("/EN/lexicon.txt")
    parse_trees = parser.build_parse_trees("The cat sleeps on the book.", grammar, lexicon)
    assert len(parse_trees) == 1
    root = parse_trees[0].root
    assert root.label == "S"
    assert len(root.children) == 2
    np, vp = root.children
    assert np.label == "NP"
    assert np.token == None
    assert np.get_functional_label("NOUN") == "cat"

def test_is_leaf():
    leaf_node = LFGParseTreeNode("Noun", "book", {})
    leaf_tree = LFGParseTree(leaf_node)
    assert leaf_tree.is_leaf() == True
    non_leaf_node = LFGParseTreeNode("S", "", {}, [leaf_node, LFGParseTreeNode("Verb", "read", {})])
    non_leaf_tree = LFGParseTree(non_leaf_node)
    assert non_leaf_tree.is_leaf() == False

def test_to_string():
    leaf_node = LFGParseTreeNode("Noun", "book", {})
    leaf_tree = LFGParseTree(leaf_node)
    assert leaf_tree.to_string() == "book"
    non_leaf_node = LFGParseTreeNode("S", "", {}, [leaf_node, LFGParseTreeNode("Verb", "read", {})])
    non_leaf_tree = LFGParseTree(non_leaf_node)
    assert non_leaf_tree.to_string() == "(S (Noun book) (Verb read))"

def test_f_structure_matrix():
    # Test with a leaf node
    leaf_node = LFGParseTreeNode("Noun", "book", {"PRED": "book"})
    leaf_tree = LFGParseTree(leaf_node)
    assert leaf_tree.f_structure_matrix() == {"PRED": {"Noun": {"book": "book"}} }
    
    # Test with non-leaf node
    np_node = LFGParseTreeNode("NP", "", {"NOUN": "cat"}, [LFGParseTreeNode("Determiner", "the", {"PRED":"the"}), leaf_node])
    vp_node = LFGParseTreeNode("VP", "", {"PRED":"run<SUBJ.run_1stArg>"}, [LFGParseTreeNode("Verb", "run", {"TENSED": "-", "ASPECT": "IMPERFECTIVE"})])
    s_node = LFGParseTreeNode("S", "", {"↑": "↓1", "SUBJ": "↓1", "PRED":"↓2"}, [np_node, vp_node])
    tree = LFGParseTree(s_node)
    assert tree.f_structure_matrix() == {"↑": {"S": "↓1"}, "SUBJ": {"S": "↓1"}, "PRED":{"S": "↓2", "NP": {"NOUN": "cat"}, "VP": {"PRED":"run<SUBJ.run_1stArg>"} }

def test_f_structure_class():
    # Test adding attributes to f_structure
    f_structure = FStructure()
    f_structure.add("PRED", "VP PP")
    f_structure.add("MOD", "Adv")

    # Test getting an attribute from f_structure
    assert f_structure.get("PRED") == "VP PP"
    assert f_structure.get("MOD") == "Adv"
    
    # Test removing an attribute from f_structure
    f_structure.remove("MOD")
    assert f_structure.get("MOD") is None
    
    # Test getting all attributes from f_structure
    f_structure.add("TENSED", "-")
    f_structure.add("ASPECT", "IMPERFECTIVE")
    all_attributes = f_structure.get_all()
    assert all_attributes == {"PRED": "VP PP", "TENSED": "-", "ASPECT": "IMPERFECTIVE"}
    
    # Test if an attribute is present in f_structure
    assert f_structure.has("PRED") is True
    assert f_structure.has("MOD") is False
    
    # Test exception when trying to get a non-existent attribute
    with pytest.raises(AttributeError):
        f_structure.get("NON_EXISTENT_ATTRIBUTE")
