"""
PyLFG is a package for parsing sentences using Lexical Functional Grammar (LFG).
This module provides an implementation of the Earley parsing algorithm for building parse trees
from sentences and grammar rules specified in LFG.

The primary entry point for the module is the `LfgParser` class and it's main methode parse(sentence), which takes a sentence string
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
import xle.parse_grammar
import xle.parse_lexicon

class LfgParser:
    def __init__(self, grammar_format):
        self.grammar_format = grammar_format
    
    def parse(sentence: str) -> list:
        # Calls the required buid_parse_trees method corresponding to grammar_format
        pass

class XlfgParser(LfgParser):
    def __init__(self, grammar: dict, lexicon: Lexicon):
        self.grammar = grammar
        self.lexicon = lexicon

    
    def build_parse_trees(sentence: str) -> list:
        grammar = self.grammar.parse()
        lexicon = self.lexicon.parse()
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
                            stack.pop()
        
        # Integrate Optimality Theory marks
        for i, tree in enumerate(all_trees):
            tree.integrate_optimality_theory_marks()
        
        return all_trees

    

class XleParser(LfgParser):
    def __init__(self, template_file, features_file, grammar_file, lexicon_file, fst_dir):
        self.templates = load_templates(template_file)
        self.features = load_features(features_file)
        self.grammar = parse_grammar(grammar_file)
        self.lexicon = load_lexicon(lexicon_file)
        self.fst_dir = fst_dir

    def build_parse_trees(self, sentence):
        """
        Use the resources from the lexicon, grammar, and FSTs to build parse trees for the given sentence.
        """
        # Tokenize the sentence
        tokens = tokenize(sentence)
        # Look up the lexical entries for each token in the lexicon
        lexical_entries = [self.lexicon[token] for token in tokens]
        # Use the FSTs in the fst_dir directory to disambiguate the lexical entries
        disambiguated_entries = disambiguate_entries(lexical_entries, self.fst_dir)
        # Use the grammar and templates to build the parse trees
        parse_trees = build_trees(disambiguated_entries, self.grammar, self.templates)
        return parse_trees


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


class XleGrammar(Grammar):
    def __init__(self, grammar_file: str):
        super().__init__(grammar_file)

    def parse(self):
        """
        Parse the grammar in XLE format and return a dictionary in the format 
        {non_terminal: List[Tuple[str, List[str], Dict[str, str], Dict[str, str]]]}
        """
        # Code for parsing XLE grammar format and returning the dictionary 
        # in the required format goes here
        return xle.parse_grammar(grammar_file)

class XleLexicon(Lexicon):
    def __init__(self, lexicon_file: str):
        super().__init__(lexicon_file)

    def parse(self):
        """
        Parse the lexicon in XLE format and return a dictionary in the format 
        {token: Tuple[List[Tuple[str, str]], Dict[str, str]]}
        """
        # Code for parsing XLE lexicon format and returning the dictionary 
        # in the required format goes here
        return xle.parse_lexicon(lexicon_file)

import os

def tokenize(sentence, fst_tokenizer_path):
    """
    Tokenize the given sentence using an FST tokenizer if present in the given directory,
    otherwise use a default string split method.
    """
    
    if os.path.exists(fst_tokenizer_path):
        # Use the FST tokenizer to tokenize the sentence
        tokens = fst_tokenize(sentence, fst_tokenizer_path)
    else:
        # Use a default string split method to tokenize the sentence
        tokens = sentence.split()
    return tokens

def fst_tokenize(sentence, fst_path):
    """
    Tokenize the given sentence using the FST at the given path.
    """
    # Load the FST and tokenize the sentence
    tokenizer = fst.Fst.read(fst_path)
    tokenized_sentence = tokenizer.transduce(sentence)
    # Extract the tokens from the tokenized sentence
    tokens = [tokenized_sentence[i].split("\t")[1] for i in range(len(tokenized_sentence))]
    return tokens

def build_trees(disambiguated_entries, grammar, templates):
    """
    Build parse trees from the disambiguated entries using the provided grammar and templates.
    """
    # Initialize an empty list to store the parse trees
    parse_trees = []
    # Iterate through the disambiguated entries
    for entry in disambiguated_entries:
        # Get the non-terminal symbol for the entry
        non_terminal = entry[0]
        # Get the corresponding grammar rule for the non-terminal symbol
        rule = grammar[non_terminal]
        # Get the c-structure and f-structure constraints for the rule
        c_constraints = rule[2]
        f_constraints = rule[3]
        # Initialize an empty string to store the template
        template = ""
        # Iterate through the c-structure constraints
        for constraint in c_constraints:
            # Replace the constraint in the template with the corresponding value from the entry
            template = template.replace("{" + constraint + "}", entry[c_constraints[constraint]])
        # Iterate through the f-structure constraints
        for constraint in f_constraints:
            # Replace the constraint in the template with the corresponding value from the entry
            template = template.replace("{" + constraint + "}", entry[f_constraints[constraint]])
        # Use the template to build the parse tree for the entry
        parse_tree = templates[template]
        # Add the parse tree to the list of parse trees
        parse_trees.append(parse_tree)
    # Return the list of parse trees
    return parse_trees


class LCFRSGrammar:
    def __init__(self):
        self.rules = []
        self.nonterminals = set()
        self.terminals = set()

    def add_rule(self, lhs, rhs, weight=1.0):
        self.rules.append((lhs, rhs, weight))
        self.nonterminals.add(lhs)
        for symbol in rhs:
            if symbol in self.nonterminals:
                self.terminals.add(symbol)

    def parse(self, sentence):
        chart = [[[] for _ in range(len(sentence) + 1)] for _ in range(len(sentence) + 1)]
        for i in range(len(sentence)):
            for lhs, rhs, weight in self.rules:
                if rhs[0] == sentence[i]:
                    chart[i][i+1].append((lhs, weight, []))

        for span in range(2, len(sentence) + 1):
            for start in range(len(sentence) - span + 1):
                end = start + span
                for mid in range(start + 1, end):
                    for lhs1, weight1, children1 in chart[start][mid]:
                        for lhs2, weight2, children2 in chart[mid][end]:
                            for lhs, rhs, weight in self.rules:
                                if rhs == [lhs1, lhs2]:
                                    chart[start][end].append((lhs, weight * weight1 * weight2, [children1, children2]))
        parses = []
        for lhs, weight, children in chart[0][len(sentence)]:
            if lhs == "S":
                parses.append((weight, children))
        return parses

