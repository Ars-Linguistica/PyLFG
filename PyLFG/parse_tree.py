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
    def __init__(self, root: LFGParseTreeNode):
        self.root = root
        self.sentence = ""

    def set_sentence(self, sentence: str):
        self.sentence = sentence

    def is_leaf(self):
        return not self.children

    def to_string(self) -> str:
        """Convert the parse tree into a string representation using the original sentence as a template.
        Returns:
        str: The string representation of the parse tree.
        """
        if self.is_leaf():
            return self.token

        child_strings = [child.to_string() for child in self.children]
        return f"({self.label} {' '.join(child_strings)})"

    def visualize(self, mode: str = "ascii"):
        """Visualize the parse tree.
        Args:
        mode (str): The visualization mode. Can be "ascii" or "matplotlib".
        """
        if mode == "ascii":
            self._visualize_ascii()
        elif mode == "matplotlib":
            self._visualize_matplotlib()
        else:
            raise ValueError(f"Invalid visualization mode: {mode}")

    def _visualize_ascii(self):
    """
    Generate an ASCII art representation of the parse tree.
    """
    # Initialize the ASCII art string
    ascii_art = ""
    
    # Recursive function to generate the ASCII art for a subtree
    def generate_ascii(node, depth):
        # Add the label for the current node
        ascii_art = " " * (depth * 2) + node.label + "\n"
        
        # Add the ASCII art for each child
        for child in node.children:
            ascii_art += generate_ascii(child, depth + 1)
        
        return ascii_art
    
    # Generate the ASCII art for the root node
    ascii_art += generate_ascii(self.root, 0)
    
    return ascii_art


    def _visualize_matplotlib(self):
    # Create a figure and axis
    fig, ax = plt.subplots()
    
    # Create a tree layout
    pos = nx.drawing.nx_agraph.graphviz_layout(self.to_networkx(), prog='dot')
    
    # Draw the nodes and edges
    nx.draw_networkx_nodes(self.to_networkx(), pos, ax=ax)
    nx.draw_networkx_edges(self.to_networkx(), pos, ax=ax)
    
    # Add labels to the nodes
    labels = {node: f"{node.label}\n{node.token}" for node in self.to_networkx().nodes}
    nx.draw_networkx_labels(self.to_networkx(), pos, labels, ax=ax)
    
    # Show the plot
    plt.show()
    return
