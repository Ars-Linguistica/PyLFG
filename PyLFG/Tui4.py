import textual
import json
from xlfg import parse_rule, parse_lexicon_entry, match_constraints, impose_constraints_in_tree, remove_unused_constraints
import d3
import re

# Create a Textual App and a MainView
app = textual.Application("PyLFG")
main_view = textual.MainView()

# Interactive prompt section
interactive_prompt = textual.TextField(placeholder="Enter sentence to be analyzed or command preceded by $ symbol")

# Create a dictionary of commands and their corresponding functions
commands = {
    "display_rules": display_rules,
    "display_lexicon": display_lexicon,
    "clear": clear_screen,
    "save": save_grammar_lexicon,
    "load": load_grammar_lexicon,
    "validate": validate_grammar_lexicon,
    "test": test_grammar_lexicon,
    "help": show_help
}

# Add event handler for interactive prompt
@interactive_prompt.on("submit")
def process_input():
    input_string = interactive_prompt.value
    if input_string[0] == "$":
        # Process command
        command_match = re.match("^\$(\w+)\s*(.*)", input_string)
        command = command_match.group(1)
        args = command_match.group(2)
        if command in commands:
            commands[command](args)
        else:
            print("Invalid command. Type $help for a list of available commands.")
    else:
        # Analyze sentence
        parse_tree = parse_sentence(input_string, rule_list.items, lexicon_list.items)
        tree_view.set_tree(parse_tree)

# Production Rule Section
# Create a TextField for entering new production rules and a ListBox to display existing rules
rule_input = textual.TextField(placeholder="Enter production rule (e.g. NP → Det N {c-structure constraints})")
rule_list = textual.ListBox()

# Add event handlers for adding and editing production rules
@rule_input.on("submit")
def add_rule():
    rule = rule_input.value
    lhs, rhs, c_structure_constraints = parse_rule(rule)
    # Add the rule to the list
    rule_list.append(f"{lhs} → {' '.join(rhs)} {c_structure_constraints}")

@rule_list.on("double_click")
def edit_rule(item):
    rule_input.value = item.text
    rule_list.remove(item)

# Lexicon Section
# Create a TextField for entering new lexicon entries and a ListBox to display existing entries
lexicon_input = textual.TextField(placeholder="Enter lexicon entry (e.g. [functional label1=value1; functional label2=value2])")
lexicon_list = textual.ListBox()

# Add event handlers for adding and editing lexicon entries
@lexicon_input.on("submit")
def add_lexicon_entry():
    lexicon_entry = lexicon_input.value
    functional_labels = parse_lexicon_entry(lexicon_entry)
    # Add the entry to the list
    lexicon_list.append(f"{functional_labels}")

@lexicon_list.on("double_click")
def edit_lexicon_entry(item):
    lexicon_input.value = item.text
    lexicon_list.remove(item)

# C-structure and F-structure Section
# Create a TreeView to display the parse tree
tree_view = textual.TreeView()

# Add event handlers for imposing constraints and removing unused constraints
@tree_view.on("right_click")
def impose_constraints(node):
    impose_constraints_in_tree(node)

@tree_view.on("ctrl_click")
def remove_unused_constraints(node):
    remove_unused_constraints(node)

# Function definitions for commands
def display_rules():
    print("Current production rules:")
    for rule in rule_list.items:
        print(rule.text)

def display_lexicon():
    print("Current lexicon entries:")
    for entry in lexicon_list.items:
        print(entry.text)

def clear_screen():
    # Clear the screen or output area
    pass

def save_grammar_lexicon(args):
    # Save the current grammar and lexicon to a file in the specified format
    pass

def load_grammar_lexicon(args):
    # Load a grammar and lexicon from a file in the specified format
    pass

def validate_grammar_lexicon():
    # Check if the current grammar and lexicon are well-formed and consistent
    pass

def test_grammar_lexicon(args):
    # Accept a test set of sentences and check if the grammar and lexicon can correctly parse them
    pass

def show_help():
    # List all available commands and their usage
    pass

