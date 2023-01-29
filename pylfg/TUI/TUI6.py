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

# Constraint Input
constraint_input = textual.TextField(placeholder="Enter constraint (e.g. NP.c-structure = NP.f-structure)")
add_constraint_button = textual.Button("Add Constraint")
edit_constraint_button = textual.Button("Edit Constraint")
delete_constraint_button = textual.Button("Delete Constraint")

# Constraint List
constraint_list = textual.ListBox()

# Add all sections to the main view
main_view.add(interactive_prompt_section, production_rule_section, lexicon_entry_section, parse_tree_section)

# Set global styling
textual.set_global_style(textual.Style(
    background_color=textual.colors.WHITE,
    text_color=textual.colors.BLACK,
    primary_color=textual.colors.BLUE
))

# Handle user input
@interactive_prompt.on("submit")
def handle_input(text):
    if text.startswith("$"):
        # Handle command input
        command_handler = CommandHandler(text[1:])
        command_handler.handle()
    else:
        # Handle sentence input
        parse_tree = parse_sentence(text)
        tree_view.draw(parse_tree)
        f_structure_view.set_text("F-Structure: " + parse_tree.f_structure.to_string())
        e_structure_view.set_text("E-Structure: " + json.dumps(parse_tree.e_structure, indent=2))

@add_rule_button.on("click")
def handle_add_rule_button():
    rule_text = rule_input.get_text()
    parsed_rule = parse_rule(rule_text)
    if parsed_rule:
        rule_list.add_item(rule_text)
        rule_input.clear()
    else:
        # Show error message
        pass

@edit_rule_button.on("click")
def handle_edit_rule_button():
    selected_index = rule_list.get_selected_index()
    if selected_index is not None:
        rule_text = rule_input.get_text()
        parsed_rule = parse_rule(rule_text)
        if parsed_rule:
            rule_list.edit_item(selected_index, rule_text)
            rule_input.clear()
        else:
            # Show error message
            pass

@delete_rule_button.on("click")
def handle_delete_rule_button():
    selected_index = rule_list.get_selected_index()
    if selected_index is not None:
        rule_list.remove_item(selected_index)

