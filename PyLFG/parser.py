"""
PyLFG is a package for parsing sentences using Lexical Functional Grammar (LFG).
This module provides an implementation of the Earley parsing algorithm for building parse trees
from sentences and grammar rules specified in LFG.

The primary entry point for the module is the `build_parse_trees` function, which takes a sentence string and
a set of grammar rules and lexicon and returns a list of parse trees for the sentence.

The package also provides helper functions for loading grammar rules and lexicon from files,
and a `LFGParseTree` and `LFGParseTreeNode` class for representing and visualizing parse trees,
as well as a FStructure class to represent the f-structure of the analyzed sentence.
"""

import re
from typing import List, Dict
from .parse_tree import LFGParseTree, LFGParseTreeNode, LFGParseTreeNodeF


def build_parse_trees(sentence, grammar, lexicon):
    all_trees = []
    stack = ["0", "S"]
    tokens = sentence.split()
    i = 0
    while stack:
        top = stack[-1]
        if top in grammar:
            if i < len(tokens) and tokens[i] in lexicon:
                stack.append(tokens[i])
                i += 1
            else:
                found = False
                for rule in grammar[top]:
                    if i < len(tokens) and tokens[i] in lexicon and lexicon[tokens[i]] in rule[1:]:
                        children = []
                        for child in rule[1:]:
                            children.append(LFGParseTreeNodeF(child, None))
                        non_term_node = LFGParseTreeNodeF(top, None, children=children)
                        stack.pop()
                        for child in reversed(children):
                            stack.append(child.label)
                        stack.append(non_term_node)
                        found = True
                        break
                if not found:
                    stack.pop()
        else:
            if top in lexicon:
                leaf_node = LFGParseTreeNodeF(lexicon[top], top)
                stack.pop()
                stack.append(leaf_node)
            elif isinstance(top, LFGParseTreeNodeF):
                node = stack.pop()
                if not stack:
                    tree = LFGParseTree(node)
                    tree.set_sentence(sentence)
                    all_trees.append(tree)
                else:
                    parent = stack[-1]
                    parent.add_child(node)
    return all_trees


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
    parse_tree = build_parse_trees(sentence, grammar, lexicon)[0]
    print(parse_tree)
