
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
