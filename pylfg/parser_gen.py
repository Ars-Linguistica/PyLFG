# parser_gen.py
"""
The module parser_gen.py is used to convert the XLFG grammar and lexicon format to the format required by the parser generator and also generates a parser using the converted grammar and lexicon. The module contains two classes: ParserGenerator and CompiledLfgParser.
"""

import plyplus
from .parse_tree import LFGParseTree, LFGParseTreeNode, LFGParseTreeNodeF

class ParserGenerator:
    """
    The ParserGenerator class is used to convert the LFG grammar and lexicon format to the format required by the parser generator.
    It also generates a parser using the converted grammar and lexicon.
    """
    def __init__(self, grammar_format):
        self.grammar_format = grammar_format

    def convert_grammar(self, grammar: dict) -> str:
    """Convert the LFG grammar format to the format required by the parser generator"""
    if self.grammar_format != "xlfg":
        raise ValueError(f"Unsupported grammar format for this method: {self.grammar_format}")
    converted_grammar = ""
    for lhs, rhs_list in grammar.items():
        for rhs in rhs_list:
            c_constraints, f_constraints = rhs[2], rhs[3]
            c_constraints_str = " ".join(c_constraints)
            f_constraints_str = " ".join(f_constraints)
            rule = f"{lhs} -> {rhs[0]} {rhs[1]} [c: {c_constraints_str}] [f: {f_constraints_str}]"
            converted_grammar += rule + "\n"
    return converted_grammar


        def convert_lexicon(self, lexicon: dict) -> str:
        """Convert the current lexicon format to the format required by the parser generator"""
        if self.grammar_format == "xlfg":
            lexicon_str = ""
            for word, entries in lexicon.items():
                for entry in entries:
                    lexicon_str += f"{word}:{entry}\n"
            return lexicon_str
        elif self.grammar_format == "xle":
            # adapt the conversion for the xle format
            return converted_lexicon
        else:
            raise ValueError(f"Unsupported grammar format: {self.grammar_format}")

    
    def generate_parser(self, grammar: str, lexicon: str):
        """Use the parser generator to generate a parser"""
        grammar = self.convert_grammar(grammar)
        lexicon = self.convert_lexicon(lexicon)
        parser = plyplus.Grammar(grammar, lexicon)
        return parser

class CompiledLfgParser:
    """
    The CompiledLfgParser class is used to generate a parser from a given grammar and lexicon, and then use that parser to parse sentences and build parse trees.
    
    Attributes:
    grammar_format (str): The format of the input grammar, should be "xlfg" or "xle".
    grammar (dict): The grammar in the specified format.
    lexicon (dict): The lexicon in the specified format.
    parser_generator (ParserGenerator): An instance of the ParserGenerator class, used to generate the parser.
    
    Methods:
    parse(sentence: str) -> list:
    Uses the generated parser to parse the given sentence and build parse trees.
    Returns a list of LFGParseTree objects.
    """
    def __init__(self, grammar_format, grammar: dict, lexicon: dict):
        self.grammar_format = grammar_format
        self.grammar = grammar
        self.lexicon = lexicon
        self.parser_generator = ParserGenerator(grammar_format)
    
    def parse(self, sentence: str) -> list:
        """
        Takes in a string sentence and returns a list of LFGParseTree objects, generated from the parsed sentence using the pre-compiled grammar and lexicon.
        """
        parser = self.parser_generator.generate_parser(self.grammar, self.lexicon)
        # use the generated parser to parse the sentence and build parse trees
        parse_trees = []
        for tree in parser.parse(sentence):
            parse_tree = LFGParseTree(tree)
            parse_trees.append(parse_tree)
        return parse_trees
