
def load_templates(template_file):
    templates = {}
    with open(template_file, 'r') as f:
        template_str = f.read()
    template_lines = template_str.split('\n')
    current_template = None
    for line in template_lines:
        if line.startswith('   ') and current_template:
            templates[current_template] += '\n' + line
        elif line.startswith('   '):
            continue
        elif line.endswith(':'):
            current_template = line[:-1]
            templates[current_template] = ''
        else:
            current_template = None
    return templates

def load_features(features_file):
    with open(features_file, 'r') as f:
        feature_data = f.read()
    # Do some processing of the feature data, such as splitting it into lines and parsing it
    features = {}
    for line in feature_data.split('\n'):
        # Split the line by ':' and remove leading/trailing whitespace
        feature, values = [x.strip() for x in line.split(':')]
        # Remove the arrow and leading/trailing whitespace from the values string
        values = values.replace('->', '').strip()
        # Split the values string by '$' and remove leading/trailing curly braces
        values = [x.strip() for x in values.split('$') if x.strip()]
        # Add the feature and its values to the features dictionary
        features[feature] = values
    return features

def parse_grammar(grammar_file: str) -> Dict[str, List[Tuple[str, List[str], Dict[str, str], Dict[str, str]]]]:
    """
    Parse an XLE grammar file and return a dictionary of grammar rules, where the keys are
    non-terminal symbols and the values are lists of tuples representing the corresponding
    grammar rules in the form (lhs, rhs, c_constraints, f_constraints).
    """
    grammar = {}
    with open(grammar_file, 'r') as f:
        for line in f:
            # skip comments and empty lines
            if line.startswith("#") or line.strip() == "":
                continue
            # split the line on the "=" character
            lhs, rhs = line.strip().split("=")
            # remove any leading/trailing whitespace and split the lhs into the non-terminal symbol and the c-structure constraints
            lhs = lhs.strip()
            if " " in lhs:
                non_terminal, c_constraints_str = lhs.split(" ", 1)
                c_constraints = {c.split(" ")[0]: c.split(" ")[1] for c in c_constraints_str.split(" ")}
            else:
                non_terminal = lhs
                c_constraints = {}
            # split the rhs into the f-structure constraints and the list of symbols
            if "{" in rhs:
                rhs, f_constraints_str = rhs.split("{")
                f_constraints_str = f_constraints_str.strip()[:-1]
                f_constraints = {f.split(" ")[0]: f.split(" ")[1] for f in f_constraints_str.split(" ")}
                rhs = rhs.strip()
            else:
                f_constraints = {}
                rhs = rhs.strip()
            # split the rhs symbols on whitespace
            rhs_symbols = rhs.split(" ")
            # add the rule to the grammar dictionary
            if non_terminal in grammar:
                grammar[non_terminal].append((non_terminal, rhs_symbols, c_constraints, f_constraints))
            else:
                grammar[non_terminal] = [(non_terminal, rhs_symbols, c_constraints, f_constraints)]
    return grammar
    
    def parse_lexicon(file: str) -> Dict[str, Tuple[str, Dict[str, str]]]:
    lexicon = {}
    with open(file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            tokens = line.split()
            word = tokens[0]
            morph = tokens[1]
            features = {}
            for feature in tokens[2:]:
                if "=" in feature:
                    key, value = feature.split("=")
                    features[key] = value
            lexicon[word] = (morph, features)
    return lexicon
