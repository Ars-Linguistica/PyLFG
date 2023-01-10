import re
from typing import List, Dict
from .parse_tree import LFGParseTree, LFGParseTreeNode

def build_parse_tree(tokens: List[str], grammar: Dict[str, List[str]], lexicon: Dict[str, Dict[str, str]]) -> LFGParseTree:
    """
    Build a parse tree for a given list of tokens using the specified Earley parser, grammar rules and lexicon.

    Args:
    - tokens: list of strings, representing the words in the sentence to parse
    - grammar: dictionary containing the grammar rules, where keys are non-terminal symbols and values
    are lists of strings representing the productions for that non-terminal symbol
    - lexicon: dictionary containing the lexicon, where keys are words and values are dictionaries with
    grammatical information (e.g. {"cat": {"a": "SG", "NUM": "SG", "GEND": "FEM"}})

    Returns:
    - LFGParseTree: object representing the parse tree for the input sentence

    """
    chart = [[] for _ in range(len(tokens)+1)]
    chart[0].append((0, "S", 0))
    for i in range(len(tokens)):
        for state in chart[i]:
            j, X, k = state
            if X in grammar:
                for production in grammar[X]:
                    if isinstance(production, str) and production in lexicon and tokens[i] in lexicon[production]:
                        functional_annotations = lexicon[production][tokens[i]]
                        next_state = (j, production, k+1, i, tokens[i], functional_annotations)
                        chart[k+1].append(next_state)
                    elif isinstance(production, tuple) and len(production) == 2:
                        annotation, rhs = production
                        if rhs in lexicon and tokens[i] in lexicon[rhs]:
                            functional_annotations = lexicon[rhs][tokens[i]]
                            next_state = (j, rhs, k+1, i, tokens[i], functional_annotations)
                            chart[k+1].append(next_state)
            else:
                for state2 in chart[j]:
                    j2, Y, k2 = state2
                    if X == Y:
                        next_state = (j2, Y, k2, i, X, "")
                        chart[k].append(next_state)
    parse_tree_nodes = []
    for state in chart[-1]:
        j, X, k, i, value, functional_annotations = state
        parse_tree_nodes.append(LFGParseTreeNode(X, value, functional_annotations))
    parse_tree_nodes.append(LFGParseTreeNode(None, None))
    for i in range(len(chart)-1, 0, -1):
        for state in chart[i]:
            j, X, k, i, value, functional_annotations = state
            for state2 in chart[j]:
                if state2[1] == X:
                    parse_tree_nodes[state2[2]-1].children.append(parse_tree_nodes[i])
    return LFGParseTree(parse_tree_nodes[0])

def cyk_parse(sentence, grammar):
"""
Parse a sentence using the CYK algorithm.
Parameters:
sentence (str): The sentence to parse.
grammar (dict): A dictionary of production rules, where the keys are the left-hand sides of the rules and the values are lists of right-hand sides.

Returns:
list[LFGParseTree]: A list of parse trees, one for each valid parse of the sentence. If the sentence is not in the language defined by the grammar, an empty list is returned.
"""

# Tokenize the input
words = sentence.split()
n = len(words)

# Initialize the parse table
table = [[set() for i in range(n - j)] for j in range(n)]

# Fill in the base cases
for i in range(n):
    for production in grammar.values():
        for rhs in production:
            if rhs == words[i]:
                table[0][i].add(rhs)

# Fill in the rest of the table
for j in range(1, n):
    for i in range(n - j):
        for k in range(j):
            for symbol1 in table[k][i]:
                for symbol2 in table[j - k - 1][i + k + 1]:
                    for lhs, rhs in grammar.items():
                        if (symbol1, symbol2) in rhs:
                            table[j][i].add(lhs)

# Generate the parse trees
parse_trees = []
for lhs in table[-1][0]:
    parse_tree = build_parse_tree(words, table, lhs, 0, n - 1, grammar)
    if parse_tree is not None:
        parse_trees.append(parse_tree)

return parse_trees



def parse_lfg(sentence: str, grammar: dict, memo: dict = {}) -> Iterator[LFGParseTree]:
    """
    Parse the given sentence using the given context-free grammar.
    Yields all valid parse trees as LFGParseTree objects.
    Uses memoization to avoid recomputing parse trees for the same input.
    """
    if sentence in memo:
        yield from memo[sentence]
    elif not sentence:
        yield LFGParseTree(symbol="ROOT")
    else:
        for i, word in enumerate(sentence.split()):
            if word in grammar:
                for production in grammar[word]:
                    for parse in parse_lfg(sentence[i + 1:], grammar, memo):
                        yield LFGParseTree(symbol=production, children=(LFGParseTree(symbol=word), parse))
        memo[sentence] = list(parse_lfg(sentence, grammar, memo))


def parse_sentence(sentence: str, lexicon: dict, grammar: dict) -> List[LFGParseTree]:
    """
    Parse a given sentence and return a list of all possible valid parse trees.
    If the sentence is invalid or there are no valid parse trees, return an empty list.
    
    Parameters:
    sentence (str): The sentence to parse.
    lexicon (dict): The lexicon for the parser, mapping words to a list of possible parts of speech.
    grammar (dict): The grammar rules for the parser, mapping parts of speech to a list of possible production rules.
    
    Returns:
    List[LFGParseTree]: A list of all valid parse trees for the given sentence.
    """
    
    # Tag the sentence with parts of speech
    tagged_sentence = pos_tagger(sentence, lexicon)
    
    # Parse the tagged sentence using our LFG parser
    parse_trees = parse_lfg(tagged_sentence, grammar)
    
    # Validate all parse trees to ensure they are valid
    valid_trees = []
    for tree in parse_trees:
        if validate_parse_tree(tree, grammar):
            valid_trees.append(tree)
    
    # Return the list of valid parse trees
    return valid_trees



def pos_tagger(sentence: str, lexicon: dict) -> str:
    """
    Generate all possible parses for the given sentence by considering all possible parts of speech for each word.

    Args:
    - sentence: the sentence to parse, a string
    - lexicon: a dictionary with words as keys and a list of parts of speech tags as values

    Returns:
    - a generator yielding all possible parses for the sentence, as LFG parse trees
    """
    words = sentence.split()
    tags = []
    for word in words:
        if word in lexicon:
            tags.append((word, lexicon[word]))
        else:
            # Default to noun if unknown word
            tags.append((word, "N"))

    def generate_parses(tags, index=0):
        if index == len(tags):
            yield "(S)"
        else:
            word, possibles = tags[index]
            for pos in possibles:
                for parse in generate_parses(tags, index + 1):
                    yield f"(S ({pos} {word}){parse}"

    return generate_parses(tags)

def parse_lexicon(filename: str) -> Dict[str, List[str]]:
    """
    Load the lexicon from the given file and return it as a dictionary.
    
    The file is expected to contain one word and its part of speech tag per line, separated by a colon.
    Lines starting with '#' and empty lines are ignored.
    
    If a word appears multiple times in the file, all its tags are stored in a list in the dictionary.
    
    Args:
        filename (str): The name of the file to load the lexicon from.
    
    Returns:
        Dict[str, List[str]]: The lexicon as a dictionary.
    
    Examples:
        >>> parse_lexicon('lexicon.txt')
        {'the': ['D'], 'cat': ['N'], 'sat': ['V'], 'on': ['P'], 'mat': ['N'], 'fish': ['V', 'N']}
    """
    lexicon = {}
    with open(filename, 'r') as f:
        for line in f:
            # Ignore empty lines and lines starting with '#'
            if not line.strip() or line.startswith('#'):
                continue

            word, pos = line.split(':')
            word = word.strip()
            pos = pos.strip()

            if word in lexicon:
                lexicon[word].append(pos)
            else:
                lexicon[word] = [pos]
    return lexicon

def parse_grammar(filename):
    grammar = {}
    with open(filename, 'r') as f:
        for line in f:
            # Ignore empty lines and lines starting with '#'
            if not line.strip() or line.startswith('#'):
                continue

            lhs, rhs = line.split('->')
            lhs = lhs.strip()
            rhs = rhs.strip()

            if lhs in grammar:
                grammar[lhs].append(rhs)
            else:
                grammar[lhs] = [rhs]
    return grammar
