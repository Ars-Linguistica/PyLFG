import textual
import json
from xlfg import parse_rule, parse_lexicon_entry, match_constraints, impose_constraints_in_tree, remove_unused_constraints
import d3
from command import CommandHandler

# Create a Textual App and a MainView
app = textual.Application("PyLFG")
main_view = textual.MainView()

# Interactive prompt section
interactive_prompt = textual.TextField(placeholder="Enter sentence to be analyzed or command preceded by $ symbol")

# Add event handler for interactive prompt
@interactive_prompt.on("submit")
def process_input():
    input_string = interactive_prompt.value
    process(input_string)

# Instantiate the CommandHandler
command_handler = CommandHandler(rule_list, lexicon_list, parse_tree)

# Add the event handler for the interactive prompt
@interactive_prompt.on("submit")
def process_input():
    input_string = interactive_prompt.value
    command_handler.process(input_string)

# Production Rule Section
# Create a TextField for entering new production rules and a ListBox to display existing rules
rule_input = textual.TextField(placeholder="Enter production rule (e.g. NP → Det N {c-structure constraints})")
rule_list = textual.ListBox()
add_rule_button = textual.Button("Add Rule")
edit_rule_button = textual.Button("Edit Rule")
delete_rule_button = textual.Button("Delete Rule")

# Add event handlers for adding and editing production rules
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
