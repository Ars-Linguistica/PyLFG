import re
from typing import List, Dict
from .parse_tree import LFGParseTree, LFGParseTreeNode

def build_parse_tree(tokens: List[str], grammar: Dict[str, List[str]], lexicon: Dict[str, Dict[str, Dict[str,str]]]) -> LFGParseTree:
    """
    Build a parse tree for a given list of tokens using the specified grammar rules and lexicon.
    This implementation uses the Earley parsing algorithm, which is a top-down, chart-based parsing
    algorithm that is capable of handling a wide range of context-free grammars.
    
    Args:
    - tokens: list of strings, representing the words in the sentence to parse
    - grammar: dictionary containing the grammar rules, where keys are non-terminal symbols and values
    are lists of strings or tuples representing the productions for that non-terminal symbol
    - lexicon: dictionary containing the lexicon, where keys are words and values are dictionaries
    with grammatical information. The structure is {word: {pos: {grammatical_info: value}}} 
    (e.g. {"cat": {"N": {"SG": True, "NUM": "SG", "GEND": "FEM"}})
   
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
    ...


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
