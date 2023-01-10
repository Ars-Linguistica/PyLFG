"""
This module provides classes to represent and visualize LFG parse trees.
The LFGParseTree class provides a visualization of the tree structure of the sentence, as well as functional annotations in the lexical items.
"""

import networkx as nx
import matplotlib.pyplot as plt


class LFGParseTreeNode:
    def __init__(self, label: str, token: str, functional_labels=None, children=None):
        """
        Construct a new LFG parse tree node.
        Parameters:
        - label (str): The label of the node, typically a non-terminal symbol or a terminal symbol.
        - token (str): The token the node represents, if any.
        - functional_labels (Dict[str, str]): functional labels of the lexical item
        - children (List[LFGParseTreeNode]): The children of the node.
    """
        self.label = label
        self.token = token
        self.functional_labels = functional_labels if functional_labels is not None else {}
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)

    def add_functional_label(self, label: str, value: str):
        self.functional_labels[label] = value

    def get_functional_label(self, label: str):
        return self.functional_labels.get(label)

    def remove_functional_label(self, label: str):
        self.functional_labels.pop(label, None)

    def get_all_functional_labels(self):
        return self.functional_labels

    def has_functional_label(self, label: str):
        return label in self.functional_labels
    
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
        return f"LFGParseTreeNode(label={self.label}, token={self.token}, functional_labels={self.functional_labels}, children={self.children})"


class LFGParseTree:
    def __init__(self, root: LFGParseTreeNode):
        self.root = root
        self.sentence = ""

    def set_sentence(self, sentence: str):
        self.sentence = sentence

    def is_leaf(self):
        return not self.children

    def to_string(self) -> str:
        if self.is_leaf():
            return self.token

        child_strings = [child.to_string() for child in self.children]
        return f"({self.label} {' '.join(child_strings)})"
    
    def to_networkx(self):
        graph = nx.DiGraph()
        stack = [(self.root, None)]
        while stack:
            node, parent = stack.pop()
            graph.add_edge(parent, node.label)
            for child in node.children:
                stack.append((child, node.label))
        return graph

    def draw(self, show_labels=True, show_annotations=False, labels=None, font_size=12, font_color='black'):
        graph = self.to_networkx()
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos, node_size=1000, node_color='lightblue', alpha=0.8)
        nx.draw_networkx_edges(graph, pos, edge_color='gray')
        if show_labels:
            if labels:
                nx.draw_networkx_labels(graph, pos, labels, font_size=font_size, font_color=font_color)
            else:
                nx.draw_networkx_labels(graph, pos, font_size=font_size, font_color=font_color)
        if show_annotations:
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=self.get_annotations())
        plt.show()

    def get_annotations(self):
        annotations = {}
        stack = [(self.root, None)]
        while stack:
            node, parent = stack.pop()
            for label, value in node.get_all_functional_labels().items():
                annotations[(parent, node.label)] = f"{label}={value}"
            for child in node.children:
                stack.append((child, node.label))
        return annotations

