import textual
import matplotlib.pyplot as plt

from .parse_tree import LFGParseTree, LFGParseTreeNode
from .parser import build_parse_tree, validate_parse_tree, cyk_parse

# Create the main window
window = textual.Window("PyLFG")

# Create a panel for the input prompt
prompt = textual.Input("Enter a sentence to parse:")

# Create a panel for the parse tree visualization
tree_panel = textual.Panel()

# Add the input prompt and tree panel to the main window
window.add(prompt, tree_panel)

# Load the default grammar
grammar = load_grammar("EN")

# Set the current language to English
language = "EN"

# Initialize the history
history = []

# Main loop
while True:
    # Get the user input
    input_text = prompt.input()

    # Check if the user entered a command
    if input_text.startswith("/"):
        # Split the command and its arguments
        command, *args = input_text[1:].split()

        # Clear the tree panel
        if command == "clear":
            tree_panel.clear()

        # Save the current tree to a file
        elif command == "save":
            if len(args) != 1:
                print("Invalid number of arguments for /save command")
                continue
            save_tree(tree, args[0])

        # Load a tree from a file
        elif command == "load":
            if len(args) != 1:
                print("Invalid number of arguments for /load command")
                continue
            tree = load_tree(args[0])
            tree_panel.clear()
            tree_panel.add(tree.visualize("matplotlib"))

        # Display the current grammar
        elif command == "grammar":
            print(grammar)

        # Set the current grammar
        elif command == "set_grammar":
            if len(args) != 1:
                print("Invalid number of arguments for /set_grammar command")
                continue
            grammar = load_grammar(args[0])
            language = args[0]

        # Display the parse history
        elif command == "history":
            for i, (sentence, tree) in enumerate(history):
                print(f"{i}: {sentence}")

        # Export the parse history to a file
        elif command == "export_history":
            if len(args) != 1:
                print("Invalid number of arguments for /export_history command")
                continue
            export_history(history, args[0])

        # Load a parse history from a file
        elif command == "load_history":
            if len(args) != 1:
                print("Invalid number of arguments for /load_history command")
                continue
            history = load_history(args[0])

        # Toggle between languages
        elif command == "language":
            if language == "EN":
                language = "EN"
                grammar = load_grammar("EN")
            elif language == "ES":
                language = "ES"
                grammar = load_grammar("ES")
            elif language == "IT":
                language = "IT"
                grammar = load_grammar("IT")
            elif language == "FR":
                language = "FR"
                grammar = load_grammar("FR")