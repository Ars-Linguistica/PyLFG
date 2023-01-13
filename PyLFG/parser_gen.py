# parser_gen.py
import plyplus
from .parse_tree import LFGParseTree, LFGParseTreeNode, LFGParseTreeNodeF

class ParserGenerator:
    def __init__(self, grammar_format):
        self.grammar_format = grammar_format

    def convert_grammar(self, grammar: dict) -> str:
        """Convert the current grammar format to the format required by the parser generator"""
        if self.grammar_format == "xlfg":
            # convert grammar to format required by the parser generator
            return converted_grammar
        elif self.grammar_format == "xle":
            # convert grammar to format required by the parser generator
            return converted_grammar
        else:
            raise ValueError(f"Unsupported grammar format: {self.grammar_format}")

    def convert_lexicon(self, lexicon: dict) -> str:
        """Convert the current lexicon format to the format required by the parser generator"""
        if self.grammar_format == "xlfg":
            # convert lexicon to format required by the parser generator
            return converted_lexicon
        elif self.grammar_format == "xle":
            # convert lexicon to format required by the parser generator
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
    def __init__(self, grammar_format, grammar: dict, lexicon: dict):
        self.grammar_format = grammar_format
        self.grammar = grammar
        self.lexicon = lexicon
        self.parser_generator = ParserGenerator(grammar_format)
    
    def parse(self, sentence: str) -> list:
        parser = self.parser_generator.generate_parser(self.grammar, self.lexicon)
        # use the generated parser to parse the sentence and build parse trees
        parse_trees = []
        for tree in parser.parse(sentence):
            parse_tree = LFGParseTree(tree)
            parse_trees.append(parse_tree)
        return parse_trees
