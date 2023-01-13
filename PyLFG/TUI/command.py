import json

class CommandHandler:
    def __init__(self, rule_list, lexicon_list, parse_tree):
        self.rule_list = rule_list
        self.lexicon_list = lexicon_list
        self.parse_tree = parse_tree

    def process(self, input_string):
        if input_string[0] == "$":
            # Process command
            command = input_string[1:]
            command_parts = command.split(" ")
            command_name = command_parts[0]
            command_args = command_parts[1:]
            getattr(self, command_name, self.invalid_command)(*command_args)
        else:
            # Analyze sentence
            self.parse_tree = parse_sentence(input_string, self.rule_list.items, self.lexicon_list.items)
            tree_view.set_tree(self.parse_tree)

    def display_rules(self):
        print("Current production rules:")
        for rule in self.rule_list.items:
            print(rule.text)
    
    def display_lexicon(self):
        print("Current lexicon entries:")
        for entry in self.lexicon_list.items:
            print(entry.text)
    
    def load_grammar(self, filepath):
        try:
            with open(filepath, "r") as f:
                grammar = json.load(f)
            for rule in grammar:
                lhs, rhs, c_structure_constraints = parse_rule(rule)
                self.rule_list.append(f"{lhs} → {' '.join(rhs)} {c_structure_constraints}")
            print(f"Grammar loaded from {filepath}")
        except Exception as e:
            print(f"Error loading grammar from {filepath}: {e}")
    
    def load_lexicon(self, filepath):
        try:
            with open(filepath, "r") as f:
                lexicon = json.load(f)
            for entry in lexicon:
                functional_labels = parse_lexicon_entry(entry)
                self.lexicon_list.append(f"{functional_labels}")
            print(f"Lexicon loaded from {filepath}")
        except Exception as e:
            print(f"Error loading lexicon from {filepath}: {e}")
    
    def save_grammar(self, filepath):
        try:
            grammar = [rule.text for rule in self.rule_list.items]
            with open(filepath, "w") as f:
                json.dump(grammar, f)
            print(f"Grammar saved to {filepath}")
        except Exception as e:
            print(f"Error saving grammar to {filepath}: {e}")
    
    def save_lexicon(self, filepath):
        try:
            lexicon = [entry.text for entry in self.lexicon_list.items]
                        with open(filepath, "w") as f:
                json.dump(lexicon, f)
            print(f"Lexicon saved to {filepath}")
        except Exception as e:
            print(f"Error saving lexicon to {filepath}: {e}")

    def f_structure(self):
        if self.parse_tree is not None:
            f_structure = impose_constraints_in_tree(remove_unused_constraints(self.parse_tree, self.rule_list.items, self.lexicon_list.items), self.rule_list.items, self.lexicon_list.items)
            print("F-structure:")
            print(f_structure)
        else:
            print("No sentence has been analyzed yet.")
    
    def invalid_command(self):
        print("Invalid command")

