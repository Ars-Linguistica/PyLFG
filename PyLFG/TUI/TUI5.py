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

# Instantiate the CommandHandler
command_handler = CommandHandler(rule_list, lexicon_list, tree_view)

# Add event handlers for UI elements
@interactive_prompt.on("submit")
def process_input():
    input_string = interactive_prompt.value
    command_handler.process(input_string)

@add_rule_button.on("click")
    def add_rule():
        rule = rule_input.value
        lhs, rhs, c_structure_constraints = parse_rule(rule)
        # Add the rule to the list
        rule_list.append(f"{lhs} → {' '.join(rhs)} {c_structure_constraints}")
        
@edit_rule_button.on("click")
def edit_rule():
    selected_rule = rule_list.selected_item
    rule_input.value = selected_rule.text
    rule_list.remove(selected_rule)
    
@delete_rule_button.on("click")
def delete_rule():
    selected_rule = rule_list.selected_item
    rule_list.remove(selected_rule)

@add_lexicon_button.on("click")
def add_lexicon():
    entry = lexicon_input.value
    functional_labels = parse_lexicon_entry(entry)
    lexicon_list.append(f"{functional_labels}")
    
@edit_lexicon_button.on("click")
def edit_lexicon():
    selected_entry = lexicon_list.selected_item
    lexicon_input.value = selected_entry.text
    lexicon_list.remove(selected_entry)

@delete_lexicon_button.on("click")
def delete_lexicon():
    selected_entry = lexicon_list.selected_item
    lexicon_list.remove(selected_entry)

# Run the app
app.run(main_view)

