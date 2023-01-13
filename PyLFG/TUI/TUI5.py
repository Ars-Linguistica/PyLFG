import textual
import json
from xlfg import parse_rule, parse_lexicon_entry, match_constraints, impose_constraints_in_tree, remove_unused_constraints
import d3
from command import CommandHandler

# Create a Textual App and a MainView
app = textual.Application("PyLFG", theme=textual.Themes.DARK)
main_view = textual.MainView()

# Group UI elements
interactive_prompt_section = textual.Section("Interactive Prompt", layout=textual.layouts.GRID)
production_rule_section = textual.Section("Production Rules", layout=textual.layouts.GRID)
lexicon_entry_section = textual.Section("Lexicon Entries", layout=textual.layouts.GRID)

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
tree_view = d3.ParseTreeView()

# Add all sections to the main view
main_view.add(interactive_prompt_section, production_rule_section, lexicon_entry_section, tree_view)

# Set global styling
textual.set_global_style(textual.Style(
    background_color="#F5F5F5",
    text_color="#1A1A1A",
    font_family="Arial",
    font_size=16,
    padding=10,
    button_height=30,
    button_width=150,
    button_radius=5,
    button_background_color="#4CAF50",
    button_text_color="#F5F5F5",
    button_hover_background_color="#3E8E41",
    button_active_background_color="#3E8E41",
    textfield_height=30,
    textfield_width=500,
    textfield_radius=5,
    textfield_background_color="#F5F5F5",
    textfield_text_color="#1A1A1A",
    textfield_placeholder_color="#C0C0C0",
    listbox_height=200,
    listbox_width=500,
    listbox_background_color="#F5F5F5",
    listbox_text_color="#1A1A1A",
    listbox_selected_background_color="#4CAF50",
    listbox_selected_text_color="#F5F5F5",
))

