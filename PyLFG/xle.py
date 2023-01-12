
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

def parse_grammar(grammar_file: str) -> dict:
    grammar = {}
    with open(grammar_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            # Skip empty lines or lines starting with a comment symbol
            if not line.strip() or line.startswith("#"):
                continue
            # Split the line by the "=" symbol to separate the left-hand side and right-hand side of the rule
            lhs, rhs = line.split("=")
            # Strip any leading or trailing whitespace from the left-hand side
            lhs = lhs.strip()
            # Strip any leading or trailing whitespace from the right-hand side and split it by whitespace to get the list of symbols in the rule
            rhs = [symbol.strip() for symbol in rhs.strip().split()]
            # Add the rule to the grammar dictionary, using the left-hand side as the key and the right-hand side as the value
            grammar[lhs] = rhs
    return grammar
