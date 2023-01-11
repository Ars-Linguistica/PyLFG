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
                                if '<' in child.label:
                                    func_label = child.label.split('<')[1][:-1]
                                    for func in func_label.split('.'):
                                        func_items = func.split('_')
                                        child.add_functional_label(func_items[0], func_items[1])
                                stack.append(child)
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

def parse_lexicon(file):
    entries = {}
    with open(file) as f:
        for line in f:
            if line.startswith("//"):
                continue
            if line.startswith("_"):
                entry_type, fields = line.strip().split(" ")
                entries[entry_type] = fields
                continue
            if "|" in line:
                entries_raw = line.strip().split("|")
                for e in entries_raw:
                    word, category_raw, f_struct = e.strip().split(" ")
                    word = word.replace("\"", "")
                    category = category_raw.strip("[").strip("]")
                    f_struct = f_struct.strip("[").strip("]")
                    f_struct = f_struct.split(",")
                    f_struct = {f.split(":")[0].strip(): f.split(":")[1].strip() for f in f_struct}
                    if word in entries:
                        entries[word].append({"category": category, "f_struct": f_struct})
                    else:
                        entries[word] = [{"category": category, "f_struct": f_struct}]
            else:
                word, category_raw, f_struct = line.strip().split(" ")
                word = word.replace("\"", "")
                category = category_raw.strip("[").strip("]")
                f_struct = f_struct.strip("[").strip("]")
                f_struct = f_struct.split(",")
                f_struct = {f.split(":")[0].strip(): f.split(":")[1].strip() for f in f_struct}
                entries[word] = [{"category": category, "f_struct": f_struct}]
    return entries

def parse_grammar(file_name):
    """
    Parse a file that contains a context-free grammar in the XLFG format and
    return a dictionary that maps each non-terminal to a list of its possible
    expansions.

    :param file_name: The name of the file that contains the grammar.
    :return: A dictionary that maps each non-terminal to a list of its possible
    expansions.
    """
    with open(file_name) as f:
        lines = f.readlines()

    # remove comments and blank lines
    lines = [line.strip() for line in lines if not line.strip().startswith("//") and line.strip()]
    # join all the lines of the file in a single string
    grammar_string = " ".join(lines)

    grammar_dict = {}
    for rule in grammar_string.split(";"):
        # Split the rule into its components
        lhs, rhs, constraints = re.split(r"\s*->\s*|{", rule)
        rhs = rhs.strip()
        constraints = constraints.strip("}")
        # Add the rule to the dictionary
        if lhs not in grammar_dict:
            grammar_dict[lhs] = []
        grammar_dict[lhs].append((rhs, constraints))

    return grammar_dict
