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

import os
import re
from typing import List, Dict, Tuple
from .parse_tree import LFGParseTree, LFGParseTreeNode, LFGParseTreeNodeF
from .parser_gen import CompiledLfgParser
import xlfg.parse_grammar
import xlfg.parse_lexicon
import xle.parse_grammar
import xle.parse_lexicon


class LfgParser:
    """
    The main class of PyLFG (Lexical Functional Grammar) module, which provides functionality for parsing sentences using LFG grammars.
    It is the parent class for XlfgParser and XleParser, which inherit its functionality and extend it for specific uses.
    The main method of this class is build_parse_trees which takes a sentence as input and returns a list of parse trees for the sentence.
    The class also has an __init__ method which takes in a grammar_format parameter, which determines which method to call for building parse trees.
    
    :param grammar_format: str. The format of the grammar to be used for parsing. 
    :ivar grammar_format: str. The format of the grammar being used by the parser.
    """
    def __init__(self, grammar_format):
        self.grammar_format = grammar_format
    
    def parse(sentence: str) -> list:
        """
        Parses a given sentence using the specified grammar format and returns a list of parse trees.
        :param sentence: str. The sentence to be parsed.
        :return: list of LFGParseTree objects representing the possible parse trees for the sentence.
        """
        pass


class XlfgParser(LfgParser):
    """
    XlfgParser is a class that inherits from LfgParser and implements a parser for the XLFG format.
    XLFG is a fast, accurate deep parser for LFG grammar. These outputs are phrase structures, predicate-argument structures and predicate-thematic relationships.
    It takes in a grammar in the form of a dictionary and a lexicon object as input and uses them to build parse trees for a given sentence.
    :param grammar: dict. A dictionary containing the X-bar LFG grammar rules in the form of a string.
    :param lexicon: Lexicon. A lexicon object containing the lexical entries for the words in the language.
    :ivar grammar: dict. A dictionary containing the X-bar LFG grammar rules in the form of a string.
    :ivar lexicon: Lexicon. A lexicon object containing the lexical entries for the words in the language.
    :method build_parse_trees(sentence: str) -> list:
    Builds a parse tree for a given sentence using the grammar and lexicon provided in the class.
        :param sentence: str. Sentence to be parsed.
        :return: list. A list of LFGParseTree objects representing the possible parse trees for the given sentence."

    """
    def __init__(self, grammar: dict, lexicon: Lexicon):
        self.grammar = grammar
        self.lexicon = lexicon

    
    def build_parse_trees(sentence: str) -> list:
        """
        Builds parse trees for a given sentence using the grammar and lexicon provided to the XlfgParser object.
        :param sentence: string. The sentence to be parsed.
        :return: list. A list of LFGParseTree objects representing the possible parse trees for the sentence.
        """
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
    """
    Initialize the XleParser with the necessary resources.
        
    :param template_file: str
        file path of the template file.
    :param features_file: str
        file path of the features file.
    :param grammar_file: str
        file path of the grammar file.
    :param lexicon_file: str
        file path of the lexicon file.
    :param fst_dir: str
        directory containing the finite state transducers (FSTs) for disambiguation.
        """
    def __init__(self, template_file, features_file, grammar_file, lexicon_file, fst_dir):
        self.templates = load_templates(template_file)
        self.features = load_features(features_file)
        self.grammar = parse_grammar(grammar_file)
        self.lexicon = load_lexicon(lexicon_file)
        self.fst_dir = fst_dir

    def build_parse_trees(self, sentence):
        """
        Use the resources from the lexicon, grammar, and FSTs to build parse trees for the given sentence.
        :param sentence: str
            Sentence to parse.
        :return: List[str]
            List of parse trees for the given sentence.
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
    """
    A class representing a lexical functional grammar.
    """
    def __init__(self, grammar_format: str, grammar: dict):
        """
        Initializes the Grammar object with the given format and grammar.
        
        :param grammar_format: str. The format of the grammar, must be either "XLFG" or "XLE".
        :param grammar: dict. The grammar represented as a dictionary.
        """
        self.grammar_format = grammar_format
        self.grammar = grammar

    def parse(self):
        """
        Parses the grammar based on the format specified in the constructor.
        
        :returns: A parsed representation of the grammar.
        :raises ValueError: If the grammar format is not supported.
        """
        if self.grammar_format == "XLFG":
            return XlfgGrammar(self.grammar).parse_grammar()
        elif self.grammar_format == "XLE":
            return XleGrammar(self.grammar).parse_grammar()
        else:
            raise ValueError(f"Unsupported grammar format: {self.grammar_format}")


class Lexicon:
    """
    A class representing a lexical functional grammar lexicon.
    """
    def __init__(self, lexicon_format: str, lexicon: dict):
        """
        Initializes the Lexicon object with the given format and lexicon.
        
        :param lexicon_format: str. The format of the lexicon, must be either "XLFG" or "XLE".
        :param lexicon: dict. The lexicon represented as a dictionary.
        """
        self.lexicon_format = lexicon_format
        self.lexicon = lexicon

    def parse(self):
        """
        Parses the lexicon based on the format specified in the constructor.
        
        :returns: A parsed representation of the lexicon.
        :raises ValueError: If the lexicon format is not supported.
        """
        if self.lexicon_format == "XLFG":
            return XlfgLexicon(self.lexicon).parse_lexicon()
        elif self.lexicon_format == "XLE":
            return XleLexicon(self.lexicon).parse_lexicon()
        else:
            raise ValueError(f"Unsupported lexicon format: {self.lexicon_format}")


class XlfgGrammar:
    """
    A class for parsing and storing XLFG grammar rules.
    
    :param grammar_file: str. the file containing XLFG grammar rules
    :ivar grammar: dict. A dictionary with the nonterminals as keys and lists of rules as values.
    """
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
    """
    A class for parsing and storing XLFG lexicon entries.
    
    :param lexicon_file: str. the file containing XLFG lexicon entries
    :ivar lexicon: dict. A dictionary with the words as keys and lexicon entries as values.
    """
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
    """
    A class for parsing and storing XLE grammar rules.
    
    :param grammar_file: str. the file containing XLE grammar rules
    :ivar grammar: dict. A dictionary with the nonterminals as keys and lists of rules as values.
    """
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
    """
    A class for parsing and storing XLE lexicon entries.
    
    :param lexicon_file: str. the file containing XLE lexicon entries
    :ivar lexicon: dict. A dictionary with the words as keys and lexicon entries as values.
    """
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
