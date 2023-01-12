
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
