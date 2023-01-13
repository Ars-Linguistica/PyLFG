import textual
import json
from xlfg import parse_rule, parse_lexicon_entry, match_constraints, impose_constraints_in_tree, remove_unused_constraints
import d3
from command import CommandHandler

# Create a Textual App and a MainView
app = textual.Application("PyLFG")
main_view = textual.MainView()

# Group UI elements
interactive_prompt_section = textual.Section("Interactive Prompt")
production_rule_section = textual.Section("Production Rules")
lexicon_entry_section = textual.Section("Lexicon Entries")

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

# Default Styling
textual.set_global_style(textual.Style(
    background_color="#F5F5F5",
    text_color="#333333",
    accent_color="#0078D7",
    font="Open Sans",
    font_size=14,
    padding=10,
    spacing=10,
    border_radius=5
))

# Interactive prompt section styling
interactive_prompt_section.style.background_color = "#FFFFFF"
interactive_prompt_section.style.text_color = "#333333"
interactive_prompt_section.style.border_radius = 10
interactive_prompt_section.style.padding = 20

# Production Rule Input styling
rule_input.style.width = "70%"
rule_input.style.margin_right = "5%"
add_rule_button.style.width = "15%"
edit_rule_button.style.width = "15%"
delete_rule_button.style.width = "15%"

# Production Rule List styling
rule_list.style.height = "200px"
rule_list.style.overflow_y = "scroll"

# Lexicon Entry Input styling
lexicon_input.style.width = "70%"
lexicon_input.style.margin_right = "5%"
add_lexicon_button.style.width = "15%"
edit_lexicon_button.style.width = "15%"
delete_lexicon_button.style.width = "15%"

# Lexicon Entry List styling
lexicon_list.style.height = "200px"
lexicon_list.style.overflow_y = "scroll"

# Parse Tree View styling
tree_view.style.height = "500px"
tree_view.style.width = "100%"

