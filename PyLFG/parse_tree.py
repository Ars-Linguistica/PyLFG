import networkx as nx
import matplotlib.pyplot as plt


class LFGParseTreeNode:
    def __init__(self, label: str, token: str, functional_annotation=None, children=None):
        """
        Construct a new LFG parse tree node.
        Parameters:
        - label (str): The label of the node, typically a non-terminal symbol or a terminal symbol.
        - token (str): The token the node represents, if any.
        - functional_annotation(str): functional_annotation of the lexical item
        - children (List[LFGParseTreeNode]): The children of the node.
    """
        self.label = label
        self.token = token
        self.functional_annotation = functional_annotation
        self.children = children or []

    def is_leaf(self):
        """
        Determine if the node is a leaf node (i.e., has no children).
        Returns:
        - bool: True if the node is a leaf node, False otherwise.
    """
        return not self.children

    def __repr__(self):
        """
        Return a string representation of the node.
        Returns:
        - str: A string representation of the node.
    """
        return f"LFGParseTreeNode(label={self.label}, token={self.token}, children={self.children})"


class LFGParseTree:
    def __init__(self, root: LFGParseTreeNode):
        """
        Initialize the parse tree with its root node.
        Args:
        - root: a LFGParseTreeNode object
        """
        self.root = root
        self.sentence = ""

    def set_sentence(self, sentence: str):
        """
        Set the original sentence of the parse tree
        Args:
        - sentence (str): original sentence
        """
        self.sentence = sentence

    def is_leaf(self):
        """
        Check if the current parse tree is a leaf node
        Returns:
        - True if the tree is a leaf node, False otherwise.
        """
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
    
    def to_networkx(self):
        """Convert the parse tree into a NetworkX DiGraph object
        Returns:
        - A NetworkX DiGraph object representing the parse tree
        """
        graph = nx.DiGraph()
        queue = [(self.root, None)]
        while queue:
            node, parent = queue.pop(0)
            graph.add_node(node)
            if parent:
                graph.add_edge(parent, node)
            queue.extend([(child, node) for child in node.children])
        return graph


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
            # Add functional annotation information
            if node.functional_annotation:
                ascii_art += " " * (depth * 2) + node.functional_annotation + "\n"
            # Add the ASCII art for each child
            for child in node.children:
                ascii_art += generate_ascii(child, depth + 1)
            return ascii_art
    
        # Generate the ASCII art for the root node
        ascii_art += generate_ascii(self.root, 0)
    
        return ascii_art

    def _visualize_matplotlib(self):
        """
        Visualize the parse tree using matplotlib library.
        The functional annotations of the lexical items are shown in the label of the node.
        """
        # Create a figure and axis
        fig, ax = plt.subplots()

        # Create a tree layout
        pos = nx.drawing.nx_agraph.graphviz_layout(self.to_networkx(), prog='dot')

        # Draw the nodes and edges
        nx.draw_networkx_nodes(self.to_networkx(), pos, ax=ax)
        nx.draw_networkx_edges(self.to_networkx(), pos, ax=ax)

        # Add labels to the nodes
        labels = {}
        for node in self.to_networkx().nodes:
            functional_annotations = ""
            if node.functional_annotation:
                functional_annotations = "\n".join([f"{k}:{v}" for k,v in node.functional_annotation.items()])
                labels[node] = f"{node.label}\n{node.token}\n{functional_annotations}"
            else:
                labels[node] = f"{node.label}\n{node.token}"
        nx.draw_networkx_labels(self.to_networkx(), pos, labels, ax=ax)

        # Show the plot
        plt.show()
