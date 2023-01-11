"""
This module provides classes to represent and visualize LFG parse trees.
The LFGParseTree class provides a visualization of the tree structure of the sentence,
as well as functional annotations in the lexical items.
"""

import networkx as nx
import matplotlib.pyplot as plt


class LFGParseTreeNode:
    def __init__(self, label: str, token: str, functional_labels: dict = None, children=None):
        """
        Construct a new LFG parse tree node.
        Parameters:
        - label (str): The label of the node, typically a non-terminal symbol or a terminal symbol.
        - token (str): The token the node represents, if any.
        - functional_labels (Dict[str, str]): functional labels of the lexical item in the XLFG standard format, where keys are the functional labels and values are the corresponding label values
        - children (List[LFGParseTreeNode]): The children of the node.
        """
        self.label = label
        self.token = token
        self.functional_labels = functional_labels if functional_labels is not None else {}
        self.children = children or []

    def add_child(self, child):
        self.children.append(child)

    def add_functional_label(self, label: str, value: str):
        """
        Add a new functional label
        :param label: (str) functional label
        :param value: (str) corresponding label value
        """
        self.functional_labels[label] = value

    def get_functional_label(self, label: str):
        """
        get the value of the functional label specified
        :param label: (str) functional label
        :return: (str) corresponding label value
        """
        return self.functional_labels.get(label)

    def remove_functional_label(self, label: str):
        """
        remove the specified functional label from the functional_labels
        :param label: (str) functional label
        """
        self.functional_labels.pop(label, None)

    def get_all_functional_labels(self):
        """
        get all functional labels
        :return: dict of functional labels in the XLFG standard format
        """
        return self.functional_labels
    
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


class LFGParseTreeNodeF(LFGParseTreeNode):
    def __init__(self, label: str, token: str, functional_labels: dict = None, children=None):
        super().__init__(label, token, functional_labels, children)
        self.f_structure = FStructure()

    def add_to_f_structure(self, attribute: str, value: str):
        self.f_structure.add(attribute, value)

    def set_in_f_structure(self, attribute: str, value: str):
        self.f_structure.set(attribute, value)

    def get_from_f_structure(self, attribute: str):
        return self.f_structure.get(attribute)

    def remove_from_f_structure(self, attribute: str):
        self


class LFGParseTreeNodeF(LFGParseTreeNode):
    def __init__(self, label: str, token: str, functional_labels=None, children=None):
        super().__init__(label, token, functional_labels, children)
        self.f_structure = FStructure()
    def add_to_f_structure(self, attribute: str, value: str):
        self.f_structure.add(attribute, value)
        
    def set_in_f_structure(self, attribute: str, value: str):
        self.f_structure.set(attribute, value)
        
    def get_from_f_structure(self, attribute: str):
        return self.f_structure.get(attribute)
        
    def remove_from_f_structure(self, attribute: str):
        self.f_structure.remove(attribute)
        
    def get_all_f_structure(self):
        return self.f_structure.get_all()
        
    def has_in_f_structure(self, attribute: str):
        return self.f_structure.has(attribute)

    def display_f_structure(self):
        return self.f_structure.display()


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
    
    def f_structure_matrix(self):
        """
        Returns the f-structure represented as an attribute-value matrix.
        """
        # Initialize the matrix
        matrix = []
        
        # Recursive function to traverse the parse tree
        def traverse(node):
            # Get the functional labels of the current node
            labels = node.get_all_functional_labels()
            
            # If the node has children, recursively traverse them
            if node.children:
                for child in node.children:
                    traverse(child)
                    
            # If the node is a leaf, add its functional labels to the matrix
            else:
                row = []
                for key, value in labels.items():
                    row.append((key, value))
                matrix.append(row)

        # Start traversing the tree
        traverse(self.root)
        
        # Return the matrix
        return matrix
    
    def to_latex(self, filepath: str):
        f_structure_latex = self._to_latex_helper(self.root)
        c_structure_latex = self._to_c_structure_latex_helper(self.root)
        caption = "C-structure tree and F-structure representation of the parse tree"
        label = "parse_tree"

        latex_code = f"""
        \\documentclass{{article}}
        \\usepackage{{tikz-qtree}}
        \\usepackage{{tabularx}}
        \\usepackage[active,tightpage]{{preview}}
        \\usepackage{{graphicx}}
        \\PreviewEnvironment{{center}}
        \\begin{{document}}
        \\begin{{figure}}[h]
        \\centering
        \\begin{{tabularx}}{{1.5\\textwidth}}{{X l}}
        {c_structure_latex} & {f_structure_latex}\\\\
        \\end{{tabularx}}
        \\caption{{{caption}}}
        \\label{{{label}}}
        \\end{{figure}}
        \\end{{document}}
        """
        with open(filepath, "w") as f:
            f.write(latex_code)

    def _to_c_structure_latex_helper(self, node):
        children = " ".join([self._to_c_structure_latex
        
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

    
class FStructure:
    def __init__(self):
        """
        Construct a new FStructure object.
        """
        self.attributes = {}

    def add(self, attribute: str, value: str):
        """
        Add an attribute-value pair to the FStructure.
        :param attribute: (str) attribute name
        :param value: (str) attribute value
        """
        self.attributes[attribute] = value

    def set(self, attribute: str, value: str):
        """
        set an attribute-value pair to the FStructure, replacing any existing value with the new value
        :param attribute: (str) attribute name
        :param value: (str) attribute value
        """
        self.attributes[attribute] = value

    def get(self, attribute: str):
        """
        get the value of the attribute
        :param attribute: (str) attribute name
        :return: (str) value of the attribute
        """
        return self.attributes.get(attribute)

    def remove(self, attribute: str):
        """
        remove the specified attribute from the f-structure
        :param attribute: (str) attribute name
        """
        self.attributes.pop(attribute, None)

    def get_all(self):
        """
        get all the attributes
        :return: dict of attributes in the XLFG standard format
        """
        return self.attributes

    def has_attribute(self, attribute: str):
        """
        check if the f-structure has the specified attribute
        :param attribute: (str) attribute name
        :return: (bool) True if has the attribute, False otherwise
        """
        return attribute in self.attributes

    def add_functional_label(self, label: str, value: str):
        """
        Add a new functional label
        :param label: (str) functional label
        :param value: (str) corresponding label value
        """
        self.attributes[label] = value

    def get_functional_label(self, label: str):
        """
        get the value of the functional label specified
        :param label: (str) functional label
        :return: (str) corresponding label value
        """
        return self.attributes.get(label)

    def remove_functional_label(self, label: str):
        """
        remove the specified functional label from the f-structure
        :param label: (str) functional label
        """
        self.attributes.pop(label, None)

    def get_all_functional_labels(self):
        """
        get all functional labels
        :return: dict of functional labels in the XLFG standard format
        """
        return self.attributes
