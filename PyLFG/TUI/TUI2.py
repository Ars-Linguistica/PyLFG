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
@tree_view.on("double_click")
def impose_constraints(node):
    if isinstance(node, LFGParseTreeNodeF):
        # Allow the user to enter new functional labels
        functional_labels = {}
        for label in node.get_all_functional_labels():
            value = input(f"Enter value for {label}: ")
            functional_labels[label] = value
        impose_constraints_in_tree(node, functional_labels)

@tree_view.on("right_click")
def remove_constraints(node):
    if isinstance(node, LFGParseTreeNodeF):
        remove_unused_constraints(node)

# Sentence Generation Section
# Create a Button for generating sentences and a TextField to display the generated sentence
generate_button = textual.Button("Generate Sentence")
sentence_output = textual.TextField()

# Add event handler for generating sentences
@generate_button.on("click")
def generate_sentence():
    sentence = generate_sentence_from_f_structure(tree_view.root)
    sentence_output.value = sentence

# Add visual representation of parse tree
d3.create_tree_vis(tree_view)

# Add toggle button for switching between c-structure and f-structure views
structure_toggle = textual.ToggleButton("C-structure", "F-structure")

# Add event handler for switching between views
@structure_toggle.on("change")
def switch_view(state):
    if state == "C-structure":
        d3.switch_to_c_structure(tree_view)
    else:
        d3.switch_to_f_structure(tree_view)

# Add undo and redo buttons
undo_button = textual.Button("Undo")
redo_button = textual.Button("Redo")

# Add event handlers for undo and redo
@undo_button.on("click")
def undo():
    app.undo()

@redo_button.on("click")
def redo():
    app.redo()

# Add save and load buttons
save_button = textual.Button("Save")
load_button = textual.Button("Load")

# Add event handlers for saving and loading
@save_button.on("click")
def save():
    grammar = {
        "rules": rule_list.items,
        "lexicon": lexicon_list.items,
        "parse_tree": tree_view.root
    }
    with     open("grammar.json", "w") as f:
        json.dump(grammar, f)

@load_button.on("click")
def load():
    with open("grammar.json", "r") as f:
        grammar = json.load(f)
    rule_list.items = grammar["rules"]
    lexicon_list.items = grammar["lexicon"]
    tree_view.root = grammar["parse_tree"]

# Add share button
share_button = textual.Button("Share")

# Add event handler for sharing
@share_button.on("click")
def share():
    grammar = {
        "rules": rule_list.items,
        "lexicon": lexicon_list.items,
        "parse_tree": tree_view.root
    }
    json_grammar = json.dumps(grammar)
    email = input("Enter email address to share with: ")
    # Use email library to send json_grammar to email address

# Add consistency check button
consistency_check_button = textual.Button("Check Consistency")

# Add event handler for consistency check
@consistency_check_button.on("click")
def check_consistency():
    if check_consistency_of_grammar(tree_view.root):
        print("Grammar is consistent.")
    else:
        print("Grammar is inconsistent.")

# Add debug button
debug_button = textual.Button("Debug")

# Add event handler for debugging
@debug_button.on("click")
def debug():
    debug_parse_tree(tree_view.root)

# Add all the widgets to the main view
main_view.add(interactive_prompt, rule_input, rule_list, lexicon_input, lexicon_list, tree_view, structure_toggle, generate_button, sentence_output, undo_button, redo_button, save_button, load_button, share_button, consistency_check_button, debug_button)
# Add interactive_prompt handler to the main view
main_view.add_event_handler(process_input)

# Run the app
app.run()

    

