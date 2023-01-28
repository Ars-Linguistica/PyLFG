import textual
import json
from xlfg import parse_rule, parse_lexicon_entry, match_constraints, impose_constraints_in_tree, remove_unused_constraints
from parse_tree import LFGParseTreeNode, LFGParseTreeNodeF
from d3 import D3ParseTreeView
from command import CommandHandler

# Create a Textual App and a MainView with Material theme
app = textual.Application("PyLFG", theme=textual.Themes.MATERIAL)
main_view = textual.MainView()

# Group UI elements
interactive_prompt_section = textual.Section("Interactive Prompt", layout=textual.layouts.GRID)
production_rule_section = textual.Section("Production Rules", layout=textual.layouts.GRID)
lexicon_entry_section = textual.Section("Lexicon Entries", layout=textual.layouts.GRID)
parse_tree_section = textual.Section("Parse Tree", layout=textual.layouts.GRID)

# Add clear labels and instructions
interactive_prompt_section.add(textual.Label("Enter sentence to be analyzed or command preceded by $ symbol"))
production_rule_section.add(textual.Label("Enter production rule (e.g. NP → Det N {c-structure constraints})"))
lexicon_entry_section.add(textual.Label("Enter lexicon entry (e.g. cat.n {c-structure constraints})"))

# Interactive prompt
interactive_prompt = textual.TextField(placeholder="Enter sentence or command")
interactive_prompt_section.add(interactive_prompt)

# Production Rule Input
rule_input = textual.TextField(placeholder="Enter production rule (e.g. NP → Det N {c-structure constraints})")
add_rule_button = textual.Button("Add Rule")
edit_rule_button = textual.Button("Edit Rule")
delete_rule_button = textual.Button("Delete Rule")
production_rule_section.add(rule_input, add_rule_button, edit_rule_button, delete_rule_button)

# Production Rule List
rule_list = textual.ListBox()
production_rule_section.add(rule_list)

# Lexicon Entry Input
lexicon_input = textual.TextField(placeholder="Enter lexicon entry (e.g. cat.n {c-structure constraints})")
add_lexicon_button = textual.Button("Add Entry")
edit_lexicon_button = textual.Button("Edit Entry")
delete_lexicon_button = textual.Button("Delete Entry")
lexicon_entry_section.add(lexicon_input, add_lexicon_button, edit_lexicon_button, delete_lexicon_button)

# Lexicon Entry List
lexicon_list = textual.ListBox()
lexicon_entry_section.add(lexicon_list)

# Parse Tree View
tree_view = D3ParseTreeView()
parse_tree_section.add(tree_view)

# F-Structure and E-Structure View
f_structure_view = textual.Label("F-Structure: ")
e_structure_view = textual.Label("E-Structure: ")
parse_tree_section.add(f_structure_view, e_structure_view)

# Constraint Input
constraint_input = textual.TextField(placeholder="Enter constraint (e.g. NP.c-structure = NP.f-structure)")
add_constraint_button = textual.Button("Add Constraint")
edit_constraint_button = textual.Button("Edit Constraint")
delete_constraint_button = textual.Button("Delete Constraint")
parse_tree_section.add(constraint_input, add_constraint_button, edit_constraint_button, delete_constraint_button)

# Constraint List
constraint_list = textual.ListBox()
parse_tree_section.add(constraint_list)

# Add all sections to the main view
main_view.add(interactive_prompt_section, production_rule_section, lexicon_entry_section, parse_tree_section)

# Set global styling
textual.set_global_style(textual.Style(
    background_color=textual.colors.WHITE,
    text_color=textual.colors.BLACK
))

# Define command handler
cmd_handler = CommandHandler(interactive_prompt, rule_input, rule_list, lexicon_input, lexicon_list, tree_view, f_structure_view, e_structure_view, constraint_input, constraint_list)

# Bind buttons to command handler functions
add_rule_button.bind(cmd_handler.add_rule)
edit_rule_button.bind(cmd_handler.edit_rule)
delete_rule_button.bind(cmd_handler.delete_rule)
add_lexicon_button.bind(cmd_handler.add_lexicon_entry)
edit_lexicon_button.bind(cmd_handler.edit_lexicon_entry)
delete_lexicon_button.bind(cmd_handler.delete_lexicon_entry)
add_constraint_button.bind(cmd_handler.add_constraint)
edit_constraint_button.bind(cmd_handler.edit_constraint)
delete_constraint_button.bind(cmd_handler.delete_constraint)

# Run the app
app.run(main_view)
