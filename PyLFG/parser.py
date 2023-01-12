"""
PyLFG is a package for parsing sentences using Lexical Functional Grammar (LFG).
This module provides an implementation of the Earley parsing algorithm for building parse trees
from sentences and grammar rules specified in LFG.

The primary entry point for the module is the `build_parse_trees` function, which takes a sentence string
and a set of grammar rules and lexicon and returns a list of parse trees for the sentence.

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
                    rule_lhs, rule_rhs, rule_c_constraints, rule_f_constraints = parse_rule(rule)
                    if i < len(tokens) and tokens[i] in lexicon:
                        lexicon_entry = lexicon[tokens[i]]
                        lexicon_entry_c, lexicon_entry_f = parse_lexicon_entry(lexicon_entry)
                        if match_c_constraints(rule_c_constraints, tokens, i) and match_f_constraints(rule_f_constraints, lexicon_entry_f):
                            children = []
                            for child in rule_rhs:
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
    impose_constraints_in_tree(all_trees)
    remove_unused_constraints(all_trees)
    return all_trees

class Grammar:
    def __init__(self, grammar_format: str, grammar: dict):
        self.grammar_format = grammar_format
        self.grammar = grammar

    def parse(self):
        if self.grammar_format == "XLFG":
            return XlfgGrammar(self.grammar).parse()
        elif self.grammar_format == "XLE":
            return XleGrammar(self.grammar).parse()
        else:
            raise ValueError(f"Unsupported grammar format: {self.grammar_format}")


class Lexicon:
    def __init__(self, lexicon_format: str, lexicon: dict):
        self.lexicon_format = lexicon_format
        self.lexicon = lexicon

    def parse(self):
        if self.lexicon_format == "XLFG":
            return XlfgLexicon(self.lexicon).parse()
        elif self.lexicon_format == "XLE":
            return XleLexicon(self.lexicon).parse()
        else:
            raise ValueError(f"Unsupported lexicon format: {self.lexicon_format}")

class XlfgGrammar:
    def __init__(self, grammar_file: str):
        self.grammar = self.parse_grammar(grammar_file)
    
    @staticmethod
    def parse_grammar(grammar_file: str) -> dict:
        """
        Given a file containing XLFG grammar rules, returns a dictionary
        with the nonterminals as keys and lists of rules as values.

        :param grammar_file: the file containing XLFG grammar rules
        :return: a dictionary with the nonterminals as keys and lists of rules as values
        """
        
        return parse_grammar(grammar_file)


class XlfgLexicon:
    def __init__(self, lexicon_file: str):
        self.lexicon = self.parse_lexicon(lexicon_file)
    
    @staticmethod
    def parse_lexicon(lexicon_file: str) -> dict:
        """
        Given a file containing XLFG lexicon entries, returns a dictionary
        with the words as keys and lexicon entries as values.

        :param lexicon_file: the file containing XLFG lexicon entries
        :return: a dictionary with the words as keys and lexicon entries as values
        """
        
        return parse_lexicon(lexicon_file)


def parse_rule(rule: str) -> Tuple[str, List[str]]:
    """
    Given a string representation of a XLFG phrase structure rule, returns a tuple of 
    the rule in the format "LHS → RHS" and a list of c-structure constraints.

    :param rule: the string representation of a XLFG phrase structure rule
    :return: a tuple of the rule in the format "LHS → RHS" and a list of c-structure constraints
    """
    c_structure_constraints = re.findall(r"{.*?}", rule)
    rule = rule.replace(" ".join(c_structure_constraints),"").strip()
    lhs, rhs = rule.split("→")
    lhs = lhs.strip()
    rhs = [x.strip() for x in rhs.split()]
    return lhs, rhs, c_structure_constraints

def parse_lexicon_entry(lexicon_entry: str) -> dict:
    """
    Given a string representation of a XLFG lexicon entry, returns a dictionary of
    functional labels and their values.

    :param lexicon_entry: the string representation of a XLFG lexicon entry
    :return: a dictionary of functional labels and their values
    """
    functional_labels = {}
    lexicon_entry = lexicon_entry.replace("[", "").replace("]", "").replace(";", "")
    labels = lexicon_entry.split()
    for label in labels:
        parts = label.split('=')
        if len(parts) == 2:
            functional_labels[parts[0].strip()] = parts[1].strip()
    return functional_labels

def match_constraints(rule: str, lexicon_entry: dict) -> bool:
    # Extract the functional constraints from the rule
    match = re.search(f"\\{{(.*?)\\}}", rule)
    if match:
        constraints = match.group(1)
    else:
        # If there are no constraints specified in the rule, return True
        return True

def match_c_constraints(rule, tokens, i):
    c_structure_constraints = rule.c_structure_constraints
    for constraint in c_structure_constraints:
        match = re.search(constraint, tokens[i])
        if not match:
            return False
    return True

def match_f_constraints(rule, lexicon_entry):
    f_structure_constraints = rule[2]
    for constraint in f_structure_constraints:
        if not constraint.is_valid(lexicon_entry):
            return False
    return True

def impose_constraints_in_tree(tree: LFGParseTreeNodeF, constraints: dict):
    """
    Impose the constraints on the parse tree.
    :param tree: the root node of the parse tree
    :param constraints: the constraints, in the form of a dictionary where the keys are the functional labels and the values are the corresponding label values
    """
    for label, value in constraints.items():
        tree.add_functional_label(label, value)
    for child in tree.children:
        if isinstance(child, LFGParseTreeNodeF):
            impose_constraints_in_tree(child, constraints)

def remove_unused_constraints(node: LFGParseTreeNodeF):
    """
    remove unused constraint labels from a parse tree node and its children
    """
    # first remove constraints from the current node
    labels_to_remove = set(node.get_all_functional_labels().keys())
    for child in node.children:
        if isinstance(child, LFGParseTreeNodeF):
            labels_to_remove -= set(child.get_all_functional_labels().keys())
    for label in labels_to_remove:
        node.remove_functional_label(label)
    
    # then recursively remove constraints from children nodes
    for child in node.children:
        if isinstance(child, LFGParseTreeNodeF):
            remove_unused_constraints(child)

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

def parse_xlfg_rule(rule: str) -> Tuple[str, List[str], Dict[str, str], Dict[str, Dict[str, str]]]:
    """
    Given a string representation of a XLFG phrase structure rule, returns a tuple of 
    the rule in the format "LHS → RHS", c-structure constraints, and f-structure constraints.
    """

    # Split the rule by '{' and '}' to separate the rule and the constraints
    rule_parts = re.split(r'[{}]', rule)
    # Assign the first part to lhs and rhs
    lhs, rhs = rule_parts[0].strip().split("→")
    # Assign the second part to c-structure constraints
    c_constraints = {}
    if len(rule_parts) > 1:
        c_constraints = parse_c_constraints(rule_parts[1])
    # Assign the third part to f-structure constraints
    f_constraints = {}
    if len(rule_parts) > 2:
        f_constraints = parse_f_constraints(rule_parts[2])
    rhs = [x.strip() for x in rhs.split()]
    return lhs.strip(), rhs

def parse_grammar(file: str) -> Dict[str, List[Tuple[str, List[str], Dict[str, str], Dict[str, Dict[str, str]]]]]:
    grammar = {}
    with open(file) as f:
        rules = f.read().split('\n')
        for rule in rules:
            rule_lhs, rule_rhs, rule_c_constraints, rule_f_constraints = parse_xlfg_rule(rule)
            if rule_lhs in grammar:
                grammar[rule_lhs].append((rule_rhs, rule_c_constraints, rule_f_constraints))
            else:
                grammar[rule_lhs] = [(rule_rhs, rule_c_constraints, rule_f_constraints)]
    return grammar
