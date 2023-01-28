"""
The file xlfg.py contains several functions that pertain to processing and manipulating phrase structure rules and lexicon entries in the eXtended Lexical Functional Grammar (XLFG) formalism.
"""

def parse_rule(rule: str) -> Tuple[str, List[str]]:
    """
    Given a string representation of a XLFG phrase structure rule, returns a tuple of 
    the rule in the format "LHS → RHS" and a list of c-structure constraints.

    :param rule: the string representation of a XLFG phrase structure rule
    :return: a tuple of the rule in the format "LHS → RHS" and a list of c-structure constraints
    """
    c_structure_constraints = re.findall(r"{.*?}", rule)
    rule = rule.replace(" ".join(c_structure_constraints),"").strip()
    lhs, rhs = rule.split("→")
    lhs = lhs.strip()
    rhs = [x.strip() for x in rhs.split()]
    return lhs, rhs, c_structure_constraints

def parse_lexicon_entry(lexicon_entry: str) -> dict:
    """
    Given a string representation of a XLFG lexicon entry, returns a dictionary of
    functional labels and their values.

    :param lexicon_entry: the string representation of a XLFG lexicon entry
    :return: a dictionary of functional labels and their values
    """
    functional_labels = {}
    lexicon_entry = lexicon_entry.replace("[", "").replace("]", "").replace(";", "")
    labels = lexicon_entry.split()
    for label in labels:
        parts = label.split('=')
        if len(parts) == 2:
            functional_labels[parts[0].strip()] = parts[1].strip()
    return functional_labels

def match_constraints(rule: str, lexicon_entry: dict) -> bool:
    """
    Given a rule and lexicon entry, check if the constraints in the rule are satisfied by the lexicon entry.
    :param rule: the rule to check constraints against
    :param lexicon_entry: the lexicon entry to check against the rule's constraints
    :return: True if the constraints are satisfied, False otherwise
    """
    # Extract the functional constraints from the rule
    match = re.search(f"\\{{(.*?)\\}}", rule)
    if match:
        constraints = match.group(1)
    else:
        # If there are no constraints specified in the rule, return True
        return True

def match_c_constraints(rule, tokens, i):
    """
    Given a rule, a list of tokens, and an index, check if the c-structure constraints in the rule are satisfied by the token at the given index.
    :param rule: the rule to check constraints against
    :param tokens: a list of tokens
    :param i: the index of the token to check against the rule's c-structure constraints
    :return: True if the constraints are satisfied, False otherwise
    """
    c_structure_constraints = rule.c_structure_constraints
    for constraint in c_structure_constraints:
        match = re.search(constraint, tokens[i])
        if not match:
            return False
    return True

def match_f_constraints(rule, lexicon_entry):
    """
    Given a rule and a lexicon entry, check if the f-structure constraints in the rule are satisfied by the lexicon entry.
    :param rule: the rule to check constraints against
    :param lexicon_entry: the lexicon entry to check against the rule's f-structure constraints
    :return: True if the constraints are satisfied, False otherwise
    """
    f_structure_constraints = rule[2]
    for constraint in f_structure_constraints:
        if not constraint.is_valid(lexicon_entry):
            return False
    return True

def impose_constraints_in_tree(tree: LFGParseTreeNodeF, constraints: dict):
    """
    Impose the constraints on the parse tree.
    :param tree: the root node of the parse tree
    :param constraints: the constraints, in the form of a dictionary where the keys are the functional labels and the values are the corresponding label values
    """
    for label, value in constraints.items():
        tree.add_functional_label(label, value)
    for child in tree.children:
        if isinstance(child, LFGParseTreeNodeF):
            impose_constraints_in_tree(child, constraints)

def remove_unused_constraints(node: LFGParseTreeNodeF):
    """
    remove unused constraint labels from a parse tree node and its children
    """
    # first remove constraints from the current node
    labels_to_remove = set(node.get_all_functional_labels().keys())
    for child in node.children:
        if isinstance(child, LFGParseTreeNodeF):
            labels_to_remove -= set(child.get_all_functional_labels().keys())
    for label in labels_to_remove:
        node.remove_functional_label(label)
    
    # then recursively remove constraints from children nodes
    for child in node.children:
        if isinstance(child, LFGParseTreeNodeF):
            remove_unused_constraints(child)

def parse_lexicon(file):
    """
    Given a file path, read the lexicon from the file and return the lexicon entries as a dictionary.
    :param file: the path of the file containing the lexicon
    :return: a dictionary of lexicon entries
    """
    entries = {}
    with open(file) as f:
        for line in f:
            if line.startswith("//"):
                continue
            if line.startswith("_"):
                entry_type, fields = line.strip().split(" ")
                entries[entry_type] = fields
                continue
            if "|" in line:
                entries_raw = line.strip().split("|")
                for e in entries_raw:
                    word, category_raw, f_struct = e.strip().split(" ")
                    word = word.replace("\"", "")
                    category = category_raw.strip("[").strip("]")
                    f_struct = f_struct.strip("[").strip("]")
                    f_struct = f_struct.split(",")
                    f_struct = {f.split(":")[0].strip(): f.split(":")[1].strip() for f in f_struct}
                    if word in entries:
                        entries[word].append({"category": category, "f_struct": f_struct})
                    else:
                        entries[word] = [{"category": category, "f_struct": f_struct}]
            else:
                word, category_raw, f_struct = line.strip().split(" ")
                word = word.replace("\"", "")
                category = category_raw.strip("[").strip("]")
                f_struct = f_struct.strip("[").strip("]")
                f_struct = f_struct.split(",")
                f_struct = {f.split(":")[0].strip(): f.split(":")[1].strip() for f in f_struct}
                entries[word] = [{"category": category, "f_struct": f_struct}]
    return entries

def parse_xlfg_rule(rule: str) -> Tuple[str, List[str], Dict[str, str], Dict[str, Dict[str, str]]]:
    """
    Given a string representation of a XLFG phrase structure rule, returns a tuple of 
    the rule in the format "LHS → RHS", c-structure constraints, and f-structure constraints.
    """

    # Split the rule by '{' and '}' to separate the rule and the constraints
    rule_parts = re.split(r'[{}]', rule)
    # Assign the first part to lhs and rhs
    lhs, rhs = rule_parts[0].strip().split("→")
    # Assign the second part to c-structure constraints
    c_constraints = {}
    if len(rule_parts) > 1:
        c_constraints = parse_c_constraints(rule_parts[1])
    # Assign the third part to f-structure constraints
    f_constraints = {}
    if len(rule_parts) > 2:
        f_constraints = parse_f_constraints(rule_parts[2])
    rhs = [x.strip() for x in rhs.split()]
    return lhs.strip(), rhs

def parse_grammar(file: str) -> Dict[str, List[Tuple[str, List[str], Dict[str, str], Dict[str, Dict[str, str]]]]]:
    grammar = {}
    with open(file) as f:
        rules = f.read().split('\n')
        for rule in rules:
            rule_lhs, rule_rhs, rule_c_constraints, rule_f_constraints = parse_xlfg_rule(rule)
            if rule_lhs in grammar:
                grammar[rule_lhs].append((rule_rhs, rule_c_constraints, rule_f_constraints))
            else:
                grammar[rule_lhs] = [(rule_rhs, rule_c_constraints, rule_f_constraints)]
    return grammar
