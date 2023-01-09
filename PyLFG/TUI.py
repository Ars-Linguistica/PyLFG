import textual

# List of supported languages
languages = ["english", "french", "spanish"]

# Create the main window
window = textual.Window("PyLFG User Interface")

# Create the text input and display panels
input_panel = textual.InputPanel()
display_panel = textual.DisplayPanel()

# Add the panels to the window
window.add_panel(input_panel)
window.add_panel(display_panel)

# Set the current language to English
current_language = "english"

# Display the main window
window.show()

# Main loop
while True:
    # Get user input from the text prompt
    input_text = input_panel.prompt("Enter a sentence or a command:")
    
    # Check if the user entered the exit command
    if input_text.strip() == "/exit":
        break
    
    # Check if the user entered a language toggle command
    if input_text.strip().startswith("/language"):
        # Get the new language from the command
        new_language = input_text.strip().split(" ")[1]
        
        # Check if the new language is supported
        if new_language in languages:
            current_language = new_language
            display_panel.display(f"Language set to {new_language}.")
        else:
            display_panel.display(f"Error: {new_language} is not a supported language.")
    
    # If the user did not enter a command, treat the input as a sentence
    else:
        # Use the PyLFG parse function to generate the parse tree for the input sentence
        parse_tree = parse(input_text, current_language)
        
        # Use the visualize method of the parse tree to display it in the display panel
        parse_tree.visualize(mode="matplotlib", display_panel=display_panel)

# Close the window when the user exits
window.close()
