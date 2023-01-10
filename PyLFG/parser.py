"""
PyLFG is a package for parsing sentences using Lexical Functional Grammar (LFG).
This module provides an implementation of the Earley parsing algorithm for building parse trees
from sentences and grammar rules specified in LFG.

The primary entry point for the module is the `parse_sentence` function, which takes a sentence string and
a set of grammar rules and lexicon and returns a parse tree for the sentence.
The package also provides helper functions for loading grammar rules and lexicon from files,
and a `LFGParseTree` and `LFGParseTreeNode` class for representing and visualizing parse trees.
"""

import re
from typing import List, Dict
from .parse_tree import LFGParseTree, LFGParseTreeNode

def parse_sentence(sentence: str, grammar: Dict[str, List[str]], lexicon: Dict[str, Dict[str, Dict[str,str]]]) -> LFGParseTree:
    """
    Parse a sentence and return the corresponding parse tree using a given grammar and lexicon.
    
    Args:
    - sentence (str): The sentence to parse
    - grammar: dictionary containing the grammar rules, where keys are non-terminal symbols and values
    are lists of strings or tuples representing the productions for that non-terminal symbol
    - lexicon: dictionary containing the lexicon, where keys are words and values are dictionaries
    with grammatical information. The structure is {word: {pos: {grammatical_info: value}}} 
    (e.g. {"cat": {"N": {"SG": True, "NUM": "SG", "GEND": "FEM"}})
   
    Returns:
    - Yields LFGParseTree: object representing the parse tree for the input sentence
    """
    tokens = re.findall(r"[\w']+", sentence)
    yield from build_parse_tree(tokens, grammar, lexicon)

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
    - A generator of LFGParseTree: object representing the parse tree for the input sentence
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
                        for state2 in chart[j]:
                            j2, Y, k2, i2, token2, annotations2 = state2
                            if Y == rhs and (not annotation or check_annotations(annotations2, annotation)):
                                next_state = (j2, rhs, k2, i2, token2, annotations2)
                                chart[k].append(next_state)
    complete_states = [state for state in chart[-1] if state[2] == len(tokens) and state[1] == "S"]
    parse_trees = []
    for complete_state in complete_states:
        parse_tree = extract_tree(complete_state, chart)
        parse_trees.append(parse_tree)
    yield parse_trees


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

if __name__ == '__main__':
    sentence = "the cat slept on the mat"
    grammar = {
        "S": ["NP VP"],
        "NP": ["D N", "D N PP"],
        "VP": ["V", "V NP"]
    }
    lexicon = {
        "the": {"D": {"DEF": True}},
        "cat": {"N": {"SG": True, "NUM": "SG", "GEND": "FEM"}},
        "slept": {"V": {"TENSE": "PAST"}},
        "on": {"P": {"LOC": True}},
        "mat": {"N": {"SG": True, "NUM": "SG", "GEND": "NEUT"}}
    }
    parse_tree = parse_sentence(sentence, grammar, lexicon)
    print(parse_tree)
