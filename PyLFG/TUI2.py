import textual
from xlfg import parse_rule, parse_lexicon_entry, match_constraints, impose_constraints_in_tree, remove_unused_constraints

# Create a Textual App and a MainView
app = textual.Application("PyLFG")
main_view = textual.MainView()

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
@tree_view.on("double_click")
def impose_constraints(node):
    if isinstance(node, LFGParseTreeNodeF):
        # Allow the user to enter new functional labels
        functional_labels = {}
        for label in node.get_all_functional_labels():
            value = input(f"Enter value for {label}: ")
            functional_labels[label] = value
        impose_constraints_in_tree(node, functional_labels)

@tree_view.on("right_click)
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
    selected_node = tree_view.selected_node
    if isinstance(selected_node, LFGParseTreeNodeF):
        sentence = generate_sentence_from_f_structure(selected_node)
        sentence_output.value = sentence
    else:
        sentence_output.value = "Please select an F-structure node to generate a sentence."

# Add the sections to the MainView
main_view.add_section("Production Rules", [rule_input, rule_list])
main_view.add_section("Lexicon", [lexicon_input, lexicon_list])
main_view.add_section("C-structure and F-structure", [tree_view])
main_view.add_section("Sentence Generation", [generate_button, sentence_output])

# Start the App
app.run(main_view)
