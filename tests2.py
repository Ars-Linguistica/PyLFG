import re

from parser import parse_lfg
from pos_tagger import pos_tagger, parse_lexicon
from test_sentences import test_sentences

def parse_sentence(sentence: str) -> LFGParseTree:
    # Tokenize the sentence
    tokens = re.findall(r"\(|\)|[\w'-]+", sentence)

    # Build the parse tree
    return parse_lfg(tokens)

def test_lfg_parser():
    # Load the lexicon
    lexicon = parse_lexicon("lexicon.txt")

    for sentence, expected_parse in test_sentences:
        # Tag the sentence
        tagged_sentence = pos_tagger(sentence, lexicon)

        # Parse the tagged sentence
        parse_tree = parse_sentence(tagged_sentence)

        # Ensure that the parse tree matches the expected parse
        assert parse_tree == expected_parse, f"Error parsing sentence: {sentence}"

test_lfg_parser()
