import parser
import pos_tagger

def parse_sentence(sentence, lexicon, grammar):
    tagged_sentence = pos_tagger.pos_tagger(sentence, lexicon)
    parse_tree = parser.parse_lfg(tagged_sentence)
    return parse_tree

def test_parse_tree(sentence, expected_parse, lexicon, grammar):
    parse_tree = parse_sentence(sentence, lexicon, grammar)
    if str(parse_tree) != expected_parse:
        print(f"Error: {sentence} was not parsed correctly")

def main():
    # Load test sentences
    from test_sentences import test_sentences

    # Load lexicon
    with open("lexicon.txt") as f:
        lexicon = pos_tagger.parse_lexicon(f)

    # Load grammar
    with open("grammar.txt") as f:
        grammar = f.read()

    # Test each sentence
    for sentence, expected_parse in test_sentences:
        test_parse_tree(sentence, expected_parse, lexicon, grammar)

if __name__ == "__main__":
    main()
