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
import xlfg.parse_grammar
import xlfg.parse_lexicon


def build_parse_trees(sentence: str, grammar: Grammar, lexicon: Lexicon) -> list:
    grammar = grammar.parse()
    lexicon = lexicon.parse()
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
            return XlfgGrammar(self.grammar).parse_grammar()
        elif self.grammar_format == "XLE":
            return XleGrammar(self.grammar).parse_grammar()
        else:
            raise ValueError(f"Unsupported grammar format: {self.grammar_format}")


class Lexicon:
    def __init__(self, lexicon_format: str, lexicon: dict):
        self.lexicon_format = lexicon_format
        self.lexicon = lexicon

    def parse(self):
        if self.lexicon_format == "XLFG":
            return XlfgLexicon(self.lexicon).parse_lexicon()
        elif self.lexicon_format == "XLE":
            return XleLexicon(self.lexicon).parse_lexicon()
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
        
        return xlfg.parse_grammar(grammar_file)


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
        
        return xlfg.parse_lexicon(lexicon_file)
