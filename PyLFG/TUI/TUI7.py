import textual
import json
from xlfg import parse_rule, parse_lexicon_entry, match_constraints, impose_constraints_in_tree, remove_unused_constraints
from parse_tree import LFGParseTreeNode, LFGParseTreeNodeF
from d3 import D3ParseTreeView
from command import CommandHandler

class Application(textual.Application):
    def __init__(self, name, theme):
        super().__init__(name, theme)
        self.main_view = MainView()
        self.add(self.main_view)

class MainView(textual.MainView):
    def __init__(self):
        super().__init__()
        self.interactive_prompt_section = textual.Section("Interactive Prompt", layout=textual.layouts.GRID)
        self.production_rule_section = textual.Section("Production Rules", layout=textual.layouts.GRID)
        self.lexicon_entry_section = textual.Section("Lexicon Entries", layout=textual.layouts.GRID)
        self.parse_tree_section = textual.Section("Parse Tree", layout=textual.layouts.GRID)

        # Add clear labels and instructions
        self.interactive_prompt_section.add(textual.Label("Enter sentence to be analyzed or command preceded by $ symbol"))
        self.production_rule_section.add(textual.Label("Enter production rule (e.g. NP → Det N {c-structure constraints})"))
        self.lexicon_entry_section.add(textual.Label("Enter lexicon entry (e.g. cat.n {c-structure constraints})"))

        # Interactive prompt
        self.interactive_prompt = textual.TextField(placeholder="Enter sentence or command")
        self.interactive_prompt_section.add(self.interactive_prompt)

        # Production Rule Input
        self.rule_input = textual.TextField(placeholder="Enter production rule (e.g. NP → Det N {c-structure constraints})")
        self.add_rule_button = textual.Button("Add Rule")
        self.edit_rule_button = textual.Button("Edit Rule")
        self.delete_rule_button = textual.Button("Delete Rule")
        self.production_rule_section.add(self.rule_input, self.add_rule_button, self.edit_rule_button, self.delete_rule_button)

        # Production Rule List
        self.rule_list = textual.ListBox()
        self.production_rule_section.add(self.rule_list)

        # Lexicon Entry Input
        self.lexicon_input = textual.TextField(placeholder="Enter lexicon entry (e.g. cat.n {c-structure constraints})")
        self.add_lexicon_button = textual.Button("Add Entry")
        self.edit_lexicon_button = textual.Button("Edit Entry")
        self.delete_lexicon_button = textual.Button("Delete Entry")
        self.lexicon_entry_section.add(self.lexicon_input, self.add_lexicon_button, self.edit_lexicon_button, self.delete_lexicon_button)
            # Lexicon Entry List
        self.lexicon_list = textual.ListBox()
        self.lexicon_entry_section.add(self.lexicon_list)

        # Parse Tree View
        self.tree_view = D3ParseTreeView()
        self.parse_tree_section.add(self.tree_view)

        # F-Structure and E-Structure View
        self.f_structure_view = textual.Label("F-Structure: ")
        self.e_structure_view = textual.Label("E-Structure: ")

        # Constraint Input
        self.constraint_input = textual.TextField(placeholder="Enter constraint (e.g. NP.c-structure = NP.f-structure)")
        self.add_constraint_button = textual.Button("Add Constraint")
        self.edit_constraint_button = textual.Button("Edit Constraint")
        self.delete_constraint_button = textual.Button("Delete Constraint")

        # Constraint List
        self.constraint_list = textual.ListBox()

        # Add all sections to the main view
        self.add(self.interactive_prompt_section, self.production_rule_section, self.lexicon_entry_section, self.parse_tree_section)

        
# Create a Textual App and a MainView with Material theme

app = Application("PyLFG", theme=textual.Themes.MATERIAL)
