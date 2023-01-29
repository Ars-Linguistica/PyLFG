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
            
    def clear_rules(self):
    self.rule_list.clear()

def clear_lexicon(self):
    self.lexicon_list.clear()

def export_parse_tree(self, format):
    with open("parse_tree." + format, "w") as f:
        f.write(str(self.parse_tree))

def add_constraint(self, rule_or_entry, constraint):
    if rule_or_entry in self.rule_list.items:
        rule_or_entry.add_constraint(constraint)
    elif rule_or_entry in self.lexicon_list.items:
        rule_or_entry.add_constraint(constraint)
    else:
        print("Invalid rule/entry")

def remove_constraint(self, rule_or_entry, constraint):
    if rule_or_entry in self.rule_list.items:
        rule_or_entry.remove_constraint(constraint)
    elif rule_or_entry in self.lexicon_list.items:
        rule_or_entry.remove_constraint(constraint)
    else:
        print("Invalid rule/entry")

def rename_label(self, old_label, new_label):
    self.parse_tree.rename_label(old_label, new_label)

def swap_rules(self, rule1, rule2):
    index1 = self.rule_list.items.index(rule1)
    index2 = self.rule_list.items.index(rule2)
    self.rule_list.items[index1], self.rule_list.items[index2] = self.rule_list.items[index2], self.rule_list.items[index1]

def swap_entries(self, entry1, entry2):
    index1 = self.lexicon_list.items.index(entry1)
    index2 = self.lexicon_list.items.index(entry2)
    self.lexicon_list.items[index1], self.lexicon_list.items[index2] = self.lexicon_list.items[index2], self.lexicon_list.items[index1]

def undo(self):
    self.previous_action.undo()

def help(self):
    print("Available commands: clear_rules, clear_lexicon, export_parse_tree, add_constraint, remove_constraint, rename_label, swap_rules, swap_entries, undo, help, generate_fst, parse_tree, display_c_structure_constraints, display_f_structure_constraints, add_c_structure_constraint, add_f_structure_constraint, remove_c_structure_constraint, remove_f_structure_constraint")

def generate_fst(self):
    # code for generating finite state transducer
    
    def invalid_command(self):
        print("Invalid command")

