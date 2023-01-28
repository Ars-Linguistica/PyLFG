import textual
import matplotlib.pyplot as plt

from .parse_tree import LFGParseTree, LFGParseTreeNode, LFGParseTreeNodeF
from .parser import build_parse_trees, parse_lexicon, parse_grammar

supported_languages = ["EN", "FR", "ES", "IT"]

# Create the main window
window = textual.Window("PyLFG")

# Create a panel for the input prompt
prompt = textual.Input("Enter a sentence to parse:")

# Create a panel for the parse tree visualization
tree_panel = textual.Panel()

# Add the input prompt and tree panel to the main window
window.add(prompt, tree_panel)

# Set the current language to English
language = "EN"

# Load the default grammar
grammar = parse_grammar("{language}/grammar.txt")

# Load the default lexicon
lexicon = parse_lexicon("{language}/lexicon.txt")



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

        if command == "help":
            print("The following commands are available:")
            print("\t/clear - Clear the parse tree")
            print("\t/save [filename] - Save the parse tree to a file")
            print("\t/load [filename] - Load a parse tree from a file")
            print("\t/grammar - Display the current grammar")
            print("\t/set_grammar [language] - Set the current grammar to the specified language (EN, ES, IT, FR)")
            print("\t/history - Display the parse history")
            print("\t/export_history [filename] - Export the parse history to a file")
            print("\t/load_history [filename] - Load a parse history from a file")
            print("\t/language [EN,ES,IT,FR] - Switch between languages")
            print("\t/help - Display this help menu")
        # Clear the tree panel
        elif command == "clear":
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
            if len(args) != 1:
                print("Invalid number of arguments for /language command")
                continue
            if args[0] not in supported_languages:
                print("The language {args[0]} is not supported by PyLFG")
                continue
            else:
                language = args[0]
                grammar = parse_grammar("{language}/grammar.txt")
                lexicon = parse_lexicon("{language}/lexicon.txt")
    else:
        # get parse tree
        trees = build_parse_trees(input_text, grammar, lexicon)
        for i, tree in enumerate(trees):
            print(f"Tree {i+1}:")
            tree_panel.clear()
            tree_panel.add(tree.visualize("matplotlib"))
            history.append((input_text, tree))
