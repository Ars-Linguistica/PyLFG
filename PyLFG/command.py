def process(input_string):
    if input_string[0] == "$":
        # Process command
        command = input_string[1:]
        if command == "display_rules":
            print("Current production rules:")
            for rule in rule_list.items:
                print(rule.text)
        elif command == "display_lexicon":
            print("Current lexicon entries:")
            for entry in lexicon_list.items:
                print(entry.text)
        elif command.startswith("load_grammar"):
            filepath = command.split(" ")[1]
            try:
                with open(filepath, "r") as f:
                    grammar = json.load(f)
                for rule in grammar:
                    lhs, rhs, c_structure_constraints = parse_rule(rule)
                    rule_list.append(f"{lhs} → {' '.join(rhs)} {c_structure_constraints}")
                print(f"Grammar loaded from {filepath}")
            except Exception as e:
                print(f"Error loading grammar from {filepath}: {e}")
        elif command.startswith("load_lexicon"):
            filepath = command.split(" ")[1]
            try:
                with open(filepath, "r") as f:
                    lexicon = json.load(f)
                for entry in lexicon:
                    functional_labels = parse_lexicon_entry(entry)
                    lexicon_list.append(f"{functional_labels}")
                print(f"Lexicon loaded from {filepath}")
            except Exception as e:
                print(f"Error loading lexicon from {filepath}: {e}")
        elif command.startswith("save_grammar"):
            filepath = command.split(" ")[1]
            try:
                grammar = [rule.text for rule in rule_list.items]
                with open(filepath, "w") as f:
                    json.dump(grammar, f)
                print(f"Grammar saved to {filepath}")
            except Exception as e:
                print(f"Error saving grammar to {filepath}: {e}")
        elif command.startswith("save_lexicon"):
            filepath = command.split(" ")[1]
            try:
                lexicon = [entry.text for entry in lexicon_list.items]
                with open(filepath, "w") as f:
                    json.dump(lexicon, f)
                print(f"Lexicon saved to {filepath}")
            except Exception as e:
                print(f"Error saving lexicon to {filepath}: {e}")
        elif command == "f-structure":
                        if parse_tree is not None:
                f_structure = impose_constraints_in_tree(remove_unused_constraints(parse_tree, rule_list.items, lexicon_list.items), rule_list.items, lexicon_list.items)
                print("F-structure:")
                print(f_structure)
            else:
                print("No sentence has been analyzed yet.")
        else:
            print("Invalid command")
    else:
        # Analyze sentence
        parse_tree = parse_sentence(input_string, rule_list.items, lexicon_list.items)
        tree_view.set_tree(parse_tree)
  
           
