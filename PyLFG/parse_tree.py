class LFGParseTreeNode:
    """A node in an LFG parse tree.

    Each node has a label, a list of child nodes, and a start and end position
    in the original sentence.

    Attributes:
        label: The label of the node.
        children: The child nodes of the node.
        start: The start position of the node in the original sentence.
        end: The end position of the node in the original sentence.
    """
    def __init__(self, label, children, start, end):
        self.label = label
        self.children = children
        self.start = start
        self.end = end

    def __repr__(self):
        """Return a string representation of the parse tree rooted at this node."""
        return self._repr(0)

    def _repr(self, indent):
        """Helper function for __repr__."""
        s = '  ' * indent + self.label + '\n'
        for child in self.children:
            s += child._repr(indent + 1)
        return s

class LFGParseTree:
    """A tree representing the syntactic structure of a sentence according to LFG.

    Attributes:
        root: The root node of the tree.
    """
    def __init__(self, root):
        self.root = root

    def __repr__(self):
        """Return a string representation of the parse tree."""
        return repr(self.root)
