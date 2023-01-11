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


def build_parse_trees(sentence: str, grammar: dict, lexicon: dict) -> list:
    """
    Builds parse trees for the given sentence using the provided grammar and lexicon.
    Extracts information from the annotations and use them in PyLFG
    
    Args:
        sentence (str): The sentence to parse.
        grammar (dict): The grammar to use, represented as a dictionary.
        lexicon (dict): The lexicon to use, represented as a dictionary.
    
    Returns:
        list: A list of LFG parse trees for the sentence.
    
    Examples:
        >>> build_parse_trees("Jim yearns for Fred", {'S': [['N', 'VP'], ['PRO', 'VP']], 'VP': [['V2', '[NP]', '[S2]']]}, {'Jim': 'N', 'yearns': 'V', 'Fred': 'N'})
        [LFGParseTree(S (N (Jim)) (VP (V2 (yearns)) (NP (Fred))))]
    """

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
                    if i < len(tokens) and tokens[i] in lexicon:
                        match = re.search(f"{lexicon[tokens[i]]}\\[(.*?)\\]", rule)
                        if match:
                            annotation = match.group(1)
                            annotation_dict = dict(item.split(':') for item in annotation.split(','))
                            children = []
                            for child in rule.split():
                                if child in lexicon:
                                    children.append(LFGParseTreeNodeF(child, None, annotation_dict))
                                else:
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
                annotation_dict = {}
                for tag in lexicon[top]:
                    match = re.search("\\[(.*?)\\]", tag)
                    if match:
                        annotation = match.group(1)
                        annotation_dict = dict(item.split(':') for item in annotation.split(','))
                leaf_node = LFGParseTreeNodeF(lexicon[top], top, annotation_dict)
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
    """
    lexicon = {}
    with open(filename, 'r') as f:
        for line in f:
            # Ignore empty lines and lines starting with '#'
            if not line.strip() or line.startswith('#'):
                continue

            word, pos_annotations = re.split("\s", line, 1)
            word = word.strip()
            pos_annotations = pos_annotations.strip()
            if word in lexicon:
                lexicon[word].append(pos_annotations)
            else:
                lexicon[word] = [pos_annotations]
    return lexicon

def parse_grammar(filename):
    grammar = {}
    with open(filename, 'r') as f:
        for line in f:
            # Ignore empty lines and lines starting with '#'
            if not line.strip() or line.startswith('#'):
                continue
                
            lhs, rhs_annotations = line.split('{')
            lhs = lhs.strip()
            rhs, annotations = rhs_annotations.split('}')
            rhs = rhs.strip()
            annotations = annotations.strip()
            
            rule = (rhs, annotations)
            if lhs in grammar:
                grammar[lhs].append(rule)
            else:
                grammar[lhs] = [rule]
    return grammar

if __name__ == '__main__':
    sentence = "the cat slept on the mat"
    # Set the current language to English
    language = "EN"
    
    # Load the default grammar
    grammar = parse_grammar("{language}/grammar.txt")
    
    # Load the default lexicon
    lexicon = parse_lexicon("{language}/lexicon.txt")
    parse_tree = build_parse_trees(sentence, grammar, lexicon)[0]
    print(parse_tree)
