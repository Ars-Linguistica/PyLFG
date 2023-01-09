import pytest

from PyLFG import parser
from PyLFG.parse_tree import LFGParseTree
from PyLFG.EN import grammar, lexicon
from test_sentences import test_sentences

# Test build_parse_tree()
def test_build_parse_tree():
    for sentence, expected_parse_tree_str in test_sentences:
        # Tokenize the sentence
        tokens = sentence.split()
        
        # Build the parse tree
        tree = parser.build_parse_tree(tokens, grammar)
        
        # Check that the tree is correct
        assert str(tree) == expected_parse_tree_str

# Test validate_parse_tree()
def test_validate_parse_tree():
    for sentence, expected_parse_tree_str in test_sentences:
        # Tokenize the sentence
        tokens = sentence.split()
        
        # Build the parse tree
        tree = parser.build_parse_tree(tokens, grammar)
        
        # Check that the tree is valid
        assert parser.validate_parse_tree(tree, grammar)

# Test cyk_parse()
def test_cyk_parse():
    for sentence, expected_parse_tree_str in test_sentences:
        # Parse the sentence
        trees = parser.cyk_parse(sentence, grammar)
        
        # Check that the correct number of trees is returned
        assert len(trees) == 1
        
        # Check that the parse tree is correct
        assert str
