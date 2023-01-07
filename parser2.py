import re

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

# Test the parser

s = "(S (NP (D the) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (N mat)))))"
parse_tree = parse_lfg(s)

def print_parse_tree(node, indent=0):
    print(" " * indent + node.type)
    if node.value:
        print(" " * (indent + 2) + node.value)
    for child in node.children:
        print_parse_tree(child, indent + 2)

print_parse_tree(parse_tree.root)

