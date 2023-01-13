import textual
import json
from xlfg import parse_rule, parse_lexicon_entry, match_constraints, impose_constraints_in_tree, remove_unused_constraints
import d3
from command import CommandHandler

# Create a Textual App and a MainView
app = textual.Application("PyLFG", theme=textual.Themes.DARK)
main_view = textual.MainView()

# Interactive Prompt
interactive_prompt_section = textual.Section("Interactive Prompt", layout=textual.layouts.GRID)
interactive_prompt_section.add(textual.Label("Enter sentence to be analyzed or command preceded by $ symbol"))
interactive_prompt = textual.TextField(placeholder="Enter sentence or command", id="interactive-prompt", hx-post="/analyze", hx-target="#result")
interactive_prompt_section.add(interactive_prompt)
result = textual.Label("", id="result")
interactive_prompt_section.add(result)
main_view.add(interactive_prompt_section)

# Production Rules
production_rule_section = textual.Section("Production Rules", layout=textual.layouts.GRID)

# Add/Edit Production Rule
add_edit_rule_section = textual.Section("Add/Edit Production Rule")
rule_input = textual.TextField(placeholder="Enter production rule (e.g. NP → Det N {c-structure constraints})", id="rule-input", hx-post="/add_rule", hx-target="#rule_list")
add_rule_button = textual.Button("Add Rule", id="add-rule-button", hx-post="/add_rule", hx-target="#rule_list")
edit_rule_button = textual.Button("Edit Rule", id="edit-rule-button", hx-post="/edit_rule", hx-target="#rule_list")
add_edit_rule_section.add(rule_input, add_rule_button, edit_rule_button)
production_rule_section.add(add_edit_rule_section)

# Delete Production Rule
delete_rule_section = textual.Section("Delete Production Rule")
delete_rule_button = textual.Button("Delete Rule", id="delete-rule-button", hx-post="/delete_rule", hx-target="#rule_list")
delete_rule_section.add(delete_rule_button)
production_rule_section.add(delete_rule_section)

# Production Rule List
rule_list_section = textual.Section("Production Rule List")
rule_list = textual.ListBox(id="rule_list")
rule_list_section.add(rule_list)
production_rule_section.add(rule_list_section)

main_view.add(production_rule_section)

# Lexicon Entries
lexicon_entry_section = textual.Section("Lexicon Entries", layout=textual.layouts.GRID)

# Add/Edit Lexicon Entry
add_edit_entry_section = textual.Section("Add/Edit Lexicon Entry")
lexicon_input = textual.TextField(placeholder="Enter lexicon entry (e.g. cat.n {c-st
