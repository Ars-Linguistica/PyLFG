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


def build_parse_tree(sentence, grammar):
    # Initialize a list to store all valid parse trees
    all_trees = []

    # Initialize the stack
    stack = ["0", "S"]
    lexicon = load_lexicon(language)
    tokens = sentence.split()
    i = 0

    while stack:
        print(stack)
        # Get the top item from the stack
        top = stack[-1]

        # If the top item is a non-terminal symbol
        if top in grammar:
            # If the next token is in the lexicon
            if i < len(tokens) and tokens[i] in lexicon:
                # Add the token to the stack
                stack.append(tokens[i])
                i += 1
            else:
                # Otherwise, try to expand the non-terminal symbol
                found = False
                for rule in grammar[top]:
                    if i < len(tokens) and tokens[i] in lexicon and lexicon[tokens[i]] in rule[1:]:
                        # Create a new parse tree node for the non-terminal symbol
                        children = []
                        for child in rule[1:]:
                            children.append(LFGParseTreeNode(child, None))
                        non_term_node = LFGParseTreeNode(top, None, children=children)

                        # Remove the non-terminal symbol from the stack
                        stack.pop()
                        # Add the children of the non-terminal to the stack in reverse order
                        for child in reversed(children):
                            stack.append(child.label)
                        # Add the non-terminal node to the stack
                        stack.append(non_term_node)

                        found = True
                        break
                if not found:
                    stack.pop()
        else:
            # If the top item is a token
            if top in lexicon:
                # Create a new parse tree node for the token
                leaf_node = LFGParseTreeNode(lexicon[top], top)
                # Remove the token from the stack
                stack.pop()
                # Add the token node to the stack
                stack.append(leaf_node)
            # If the top item is a parse tree node
            elif isinstance(top, LFGParseTreeNode):
                # remove the parse tree node from the stack
                node = stack.pop()
                # if the stack is empty, this is the root node, create a new parse tree and append it to the list of all parse trees
                if not stack:
                    tree = LFGParseTree(node)
                    tree.set_sentence(sentence)
                    all_trees.append(tree)
                # Otherwise, add the node to its parent's children list
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
    parse_tree = parse_sentence(sentence, grammar, lexicon)
    print(parse_tree)
