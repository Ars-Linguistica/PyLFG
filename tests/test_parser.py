import pytest

from PyLFG import parser

@pytest.mark.parametrize("sentence,expected_parse", test_sentences)
def test_parse(sentence, expected_parse):
    grammar = parser.load_grammar('EN/grammar.txt')
    lexicon = parser.load_lexicon('EN/lexicon.txt')
    parse_trees = parser.cyk_parse(sentence, grammar, lexicon)
    assert len(parse_trees) == 1
    assert str(parse_trees[0]) == expected_parse

def test_parse_error():
    grammar = parser.load_grammar('EN/grammar.txt')
    lexicon = parser.load_lexicon('EN/lexicon.txt')
    with pytest.raises(ValueError):
        parser.cyk_parse("This is not a valid sentence", grammar, lexicon)
