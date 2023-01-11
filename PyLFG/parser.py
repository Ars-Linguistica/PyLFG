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
from typing import List, Dict, Tuple
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
                    rule = parse_rule(rule)  # parse the rule using XLFG standard syntax
                    if i < len(tokens) and tokens[i] in lexicon:
                        lexicon_entry = lexicon[tokens[i]]
                        lexicon_entry = parse_lexicon_entry(lexicon_entry) # parse the lexicon entry using XLFG standard syntax
                        if match_constraints(rule, lexicon_entry):
                            children = []
                            for child in rule.rhs:
                                child_node = None
                                if child in lexicon:
                                    child_node = LFGParseTreeNodeF(child, None)
                                else:
                                    child_node = LFGParseTreeNodeF(child, None)
                                children.append(child_node)
                            non_term_node = LFGParseTreeNodeF(top, None, children=children)
                            stack.pop()
                            for child in reversed(children):
                                stack.append(child)
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
                non_term_node = top
                children = top.children
                stack.pop()
                if stack and stack[-1] == non_term_node.label:
                    stack.pop()
                    stack.extend(reversed(children))
                    if stack[-1].label == "S":
                        all_trees.append(LFGParseTree(stack[-1]))
    return all_trees

def parse_rule(rule: str) -> str:
    """
    Given a string representation of a XLFG phrase structure rule, returns a string in the format
    "LHS → RHS" where LHS is the left-hand side of the rule and RHS is the right-hand side of the rule.

    :param rule: the string representation of a XLFG phrase structure rule
    :return: the rule in the format "LHS → RHS"
    """
    parts = rule.split('→')
    lhs = parts[0].strip()
    rhs = parts[1].strip()
    rhs = rhs.replace("[", "").replace("]", "").replace(";", "")

    return f"{lhs} → {rhs}"

def parse_lexicon_entry(lexicon_entry: str) -> Tuple:
    parts = lexicon_entry.split()
    category = parts[0]
    f_structure = None
    constraints = None
    for part in parts[1:]:
        if part.startswith("["):
            f_structure = part
        elif part.startswith("{"):
            constraints = part
    if f_structure:
        f_structure = f_structure[1:-1].split(",")
    if constraints:
        constraints = constraints[1:-1].split(";")
    return category, f_structure, constraints

def match_constraints(rule: str, lexicon_entry: dict) -> bool:
    # Extract the functional constraints from the rule
    match = re.search(f"\\{{(.*?)\\}}", rule)
    if match:
        constraints = match.group(1)
    else:
        # If there are no constraints specified in the rule, return True
        return True

    # Check if each constraint in the rule is satisfied by the lexicon entry
    for constraint in constraints.split(';'):
        c = constraint.strip()
        c_parts = c.split("=")
        c_parts[0] = c_parts[0].strip()
        c_parts[1] = c_parts[1].strip()
        if c_parts[0] not in lexicon_entry or lexicon_entry[c_parts[0].strip()] != c_parts[1]:
            return False
    # If all constraints are satisfied return True
    return True


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
