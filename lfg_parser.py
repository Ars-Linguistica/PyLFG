import re
from typing import Dict, List

class LFGParseTreeNode:
    def __init__(self, type, value=None, children=None, c_structure=None, f_structure=None):
        self.type = type
        self.value = value
        self.children = children or []
        self.c_structure = c_structure
        self.f_structure = f_structure

class LFGParseTree:
    def __init__(self, root):
        self.root = root

def build_parse_tree(tokens):
    def build_subtree(parent):
        while tokens:
            token = tokens.pop(0)
            if token == "(":
                node_type = tokens.pop(0)
                subtree = build_subtree(LFGParseTreeNode(node_type))
                parent.children.append(subtree)
            elif token == ")":
                return parent
            else:
                parent.children.append(LFGParseTreeNode("word", value=token))
        return parent

    root_type = tokens.pop(0)
    return LFGParseTree(build_subtree(LFGParseTreeNode(root_type)))

def parse_lfg(s):
    tokens = re.findall(r"\(|\)|[\w'-]+", s)
    return build_parse_tree(tokens)

def parse_sentence(sentence: str, lexicon: Dict[str, str], grammar: Dict[str, List[str]]) -> LFGParseTree:
    # Use the POS tagger to get the tagged sentence
    tagged_sentence = pos_tagger(sentence, lexicon)
    print(f"Tagged sentence: {tagged_sentence}")

    # Parse the tagged sentence using the LFG parser
    parse_tree = parse_lfg(tagged_sentence)
    print_parse_tree(parse_tree.root)

    # Validate the parse tree using the grammar
    validate_parse_tree(parse_tree.root, grammar)

    # Generate the c-structure and f-structure for the parse tree
    generate_c_structure(parse_tree.root, lexicon)
    generate_f_structure(parse_tree.root, lexicon)

    return parse_tree

def validate_parse_tree(node, grammar: Dict[str, List[str]]):
    # If this node is a terminal symbol (i.e. a word), check that it is in the lexicon
    if node.type == "word":
        if node.value not in lexicon:
            raise ValueError(f
