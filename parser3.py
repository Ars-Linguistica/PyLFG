import re
import pos_tagger

class LFGParseTreeNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []

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

def parse_sentences(sentences):
    lexicon = pos_tagger.parse_lexicon("lexicon.txt")
    parse_trees = []
    for sentence in sentences:
        pos_tagged_sentence = pos_tagger.pos_tagger(sentence, lexicon)
        parse_tree = parse_lfg(pos_tagged_sentence)
        parse_trees.append(parse_tree)
    return parse_trees

# Test the parser

sentences = ["The cat sat on the mat", "I saw the man with the telescope"]
parse_trees = parse_sentences(sentences)

def print_parse_tree(node, indent=0):
    print(" " * indent + node.type)
    if node.value:
        print(" " * (indent + 2) + node.value)
    for child in node.children:
        print_parse_tree(child, indent + 2)

for parse_tree in parse_trees:
    print_parse_tree(parse_tree.root)
