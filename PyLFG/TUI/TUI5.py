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

# Export Grammar and Lexicon
export_button = textual.Button("Export Grammar and Lexicon")
parse_tree_section.add(export_button)

# Add all sections to the main view
main_view.add(interactive_prompt_section, production_rule_section, lexicon_entry_section, parse_tree_section)

# Set global styling
textual.set_global_style(textual.Style(
    background_color=textual.colors.WHITE,
    text_color=textual.colors.BLACK,
    selected_background_color=textual.colors.LIGHT_GREY,
    selected_text_color=textual.colors.BLACK
))

# Add event handlers for buttons and input fields
add_rule_button.on_click(lambda: parse_rule(rule_input.value) and rule_list.add_item(rule_input.value))
edit_rule_button.on_click(lambda: parse_rule(rule_input.value) and rule_list.update_selected_item(rule_input.value))
delete_rule_button.on_click(lambda: rule_list.remove_selected_item())
add_lexicon_button.on_click(lambda: parse_lexicon_entry(lexicon_input.value
add_lexicon_button.on_click(lambda: parse_lexicon_entry(lexicon_input.value) and lexicon_list.add_item(lexicon_input.value))
edit_lexicon_button.on_click(lambda: parse_lexicon_entry(lexicon_input.value) and lexicon_list.update_selected_item(lexicon_input.value))
delete_lexicon_button.on_click(lambda: lexicon_list.remove_selected_item())

add_constraint_button.on_click(lambda: match_constraints(constraint_input.value) and constraint_list.add_item(constraint_input.value))
edit_constraint_button.on_click(lambda: match_constraints(constraint_input.value) and constraint_list.update_selected_item(constraint_input.value))
delete_constraint_button.on_click(lambda: constraint_list.remove_selected_item())

export_button.on_click(lambda: export_grammar_and_lexicon())

interactive_prompt.on_submit(lambda: handle_interactive_prompt(interactive_prompt.value))

# Run the app
app.run()

