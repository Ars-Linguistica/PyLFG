# Import the necessary libraries
import re
import os
import textwrap
import matplotlib.pyplot as plt

from textual import CommandHandler, TextualClient, document

# Import the necessary functions from the PyLFG package
from pylfg import build_parse_tree, cyk_parse, validate_parse_tree

# Set the prompt for the user input
prompt = ">>> "

# Initialize the command handler
command_handler = CommandHandler()

# Define the handler function for the /language command
@command_handler.command("/language")
def handle_language_command(client, command, arguments):
    """
    Change the language of the parser.
    """
    # Set the language of the parser
    language = arguments.strip()
    client.language = language
    
    # Update the prompt to reflect the current language
    client.prompt = f"{language} {prompt}"
    
    # Print a message to the user
    client.write("Language changed to: {}".format(language))
    
# Define the handler function for the /clear command
@command_handler.command("/clear")
def handle_clear_command(client, command, arguments):
    """
    Clear the display panel.
    """
    # Clear the matplotlib plot
    plt.clf()
    
    # Clear the Textual display panel
    client.clear_display_panel()
    
# Define the handler function for the /save command
@command_handler.command("/save")
def handle_save_command(client, command, arguments):
    """
    Save the current parse tree to a file.
    """
    # Get the filename from the arguments
    filename = arguments.strip()
    
    # Save the current matplotlib plot to the specified file
    plt.savefig(filename)
    
    # Print a message to the user
    client.write("Parse tree saved to file: {}".format(filename))

# Define the handler function for the /load command
@command_handler.command("/load")
def handle_load_command(client, command, arguments):
    """
    Load a parse tree from a file.
    """
    # Get the filename from the arguments
    filename = arguments.strip()
    
    # Load the parse tree from the specified file
    with open(filename, "r") as f:
        parse_tree_str = f.read()
    
    # Display the parse tree in the Textual display panel
    client.write(parse_tree_str, style="code")
    
    # Display the parse tree using matplotlib
    plt.plot(parse_tree_str)
    plt.show()
    
# Define the handler function for the /grammar command
@command_handler.command("/grammar")
def handle_grammar_command(client, command, arguments):
    """
    Display the current grammar.
    """
    # Print the current grammar to the user
    client.write("Current grammar:\n{}".format(client.grammar), style="code")
    
# Define the handler function for the /set_grammar command
@command_handler.command("/set_grammar")
def handle_set_grammar_command(client, command, arguments):
    """
    Set the grammar for PyLFG.
    """
    # Parse the arguments
    try:
        grammar_path = arguments[0]
    except IndexError:
        client.write_line("Error: No grammar specified.")
        return
    
    # Load the grammar from the specified file
    try:
        with open(grammar_path, "r") as f:
            grammar = load_grammar(f)
    except Exception as e:
        client.write_line(f"Error: Could not load grammar: {e}")
        return
    
    # Set the grammar
    set_grammar(grammar)
    client.write_line(f"Successfully set grammar from file: {grammar_path}")

@command_handler("/visualize")
def handle_visualize_command(client, command, arguments):
    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", choices=["ascii", "matplotlib"], default="ascii")
    args = parser.parse_args(arguments)
    
    # Visualize the parse tree
    client.current_tree.visualize(mode=args.mode)

@command_handler.command("/history")
def handle_history_command(client, command, arguments):
    """
    Display the history of commands and their outputs.
    """
    # Print the command history
    for i, (c, o) in enumerate(client.history):
        print(f"{i}: {c}")
        print(o)

