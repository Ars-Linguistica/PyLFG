import pytest
from PyLFG.parser import build_parse_tree, validate_parse_tree, cyk_parse

# Test data
from PyLFG.tests.test_sentences import test_sentences

# Load grammar and lexicon
with open("EN/grammar.txt") as f:
    grammar_str = f.read()
grammar = {}
for line in grammar_str.strip().split("\n"):
    nonterminal, productions = line.split(" -> ")
    grammar[nonterminal] = productions.split(" | ")

with open("EN/lexicon.txt") as f:
    lexicon_str = f.read()
lexicon = {}
for line in lexicon_str.strip().split("\n"):
    word, pos = line.split(": ")
    lexicon[word] = pos

# Test build_parse_tree
@pytest.mark.parametrize("sentence, expected_tree", test_sentences)
def test_build_parse_tree(sentence, expected_tree):
    tokens = sentence.split()
    tree = build_parse_tree(tokens, grammar)
    assert str(tree) == expected_tree

# Test validate_parse_tree
@pytest.mark.parametrize("sentence, tree", test_sentences)
def test_validate_parse_tree(sentence, tree):
    tree = LFGParseTree.from_string(tree)
    assert validate_parse_tree(tree, grammar)

# Test cyk_parse
@pytest.mark.parametrize("sentence, expected_tree", test_sentences)
def test_cyk_parse(sentence, expected_tree):
    trees = cyk_parse(sentence, grammar)
    assert any(str(tree) == expected_tree for tree in trees)
