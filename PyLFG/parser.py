import re

from .parse_tree import LFGParseTree, LFGParseTreeNode

def build_parse_tree(tokens: List[str], grammar: Dict[str, List[str]], lexicon: Dict[str, Dict[str, str]]) -> LFGParseTree:
    """
    Build a parse tree for a given list of tokens using the specified grammar rules and lexicon.

    Args:
    - tokens: list of strings, representing the words in the sentence to parse
    - grammar: dictionary containing the grammar rules, where keys are non-terminal symbols and values
    are lists of strings representing the productions for that non-terminal symbol
    - lexicon: dictionary containing the lexicon, where keys are words and values are dictionaries with
    grammatical information (e.g. {"cat": {"a": "SG", "NUM": "SG", "GEND": "FEM"}})

    Returns:
    - LFGParseTree: object representing the parse tree for the input sentence

    """
    nodes = [LFGParseTreeNode(None, None)]
    for token in tokens:
        next_productions = []
        for non_terminal, productions in grammar.items():
            for production in productions:
                if isinstance(production, str) and production in lexicon and token in lexicon[production]:
                    next_productions.append((non_terminal, lexicon[production][token]))
                elif isinstance(production, tuple) and len(production) == 2:
                    annotation, rhs = production
                    if rhs in lexicon and token in lexicon[rhs]:
                        next_productions.append((non_terminal, annotation, lexicon[rhs][token]))
        if not next_productions:
            raise ValueError(f"No productions found for token: {token}")
        new_nodes = []
        for production in next_productions:
            if len(production) == 2:
                new_node = LFGParseTreeNode(production[0], token, functional_annotation=production[1])
            elif len(production) == 3:
                new_node = LFGParseTreeNode(production[0], token, functional_annotation={'type': production[1], 'subtype': production[2]})
            new_nodes.append(new_node)
        nodes.extend(new_nodes)
    return LFGParseTree(nodes[0])


def validate_parse_tree(tree: LFGParseTree, grammar: dict, lexicon: dict) -> bool:
    """
    Validate a parse tree according to the given grammar rules and lexicon entries.
    Parameters:
    - tree (LFGParseTree): The parse tree to validate.
    - grammar (dict): A dictionary of the grammar rules. The keys are the non-terminal symbols and the values are the lists of right-hand sides.
    - lexicon (dict): A dictionary of the lexicon entries. The keys are the grammatical categories and the values are the lists of words in that category along with their functional annotations
    Returns:
    - bool: True if the parse tree is valid according to the grammar and lexicon, False otherwise.
    """
    # Base case: If the tree is a leaf node, it must be a terminal symbol
    if tree.is_leaf():
        if tree.label in grammar["terminals"] and tree.label in lexicon:
            #Checking if the token also exist in the lexicon
            if tree.token in lexicon[tree.label]:
                if tree.functional_annotation == lexicon[tree.label][tree.token]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    # Recursive case: Check that the node's label is a non-terminal,
    # its children's labels are in the list of valid rules, and that their annotations match with the lexicon
    if tree.label in grammar["nonterminals"]:
        for child in tree.children:
            if validate_parse_tree(child, grammar, lexicon) == False:
                return False
        return True
    # If the tree is neither a leaf node nor a non-terminal, it is invalid
    return False

def cyk_parse(sentence, grammar):
"""
Parse a sentence using the CYK algorithm.
Parameters:
sentence (str): The sentence to parse.
grammar (dict): A dictionary of production rules, where the keys are the left-hand sides of the rules and the values are lists of right-hand sides.

Returns:
list[LFGParseTree]: A list of parse trees, one for each valid parse of the sentence. If the sentence is not in the language defined by the grammar, an empty list is returned.
"""

# Tokenize the input
words = sentence.split()
n = len(words)

# Initialize the parse table
table = [[set() for i in range(n - j)] for j in range(n)]

# Fill in the base cases
for i in range(n):
    for production in grammar.values():
        for rhs in production:
            if rhs == words[i]:
                table[0][i].add(rhs)

# Fill in the rest of the table
for j in range(1, n):
    for i in range(n - j):
        for k in range(j):
            for symbol1 in table[k][i]:
                for symbol2 in table[j - k - 1][i + k + 1]:
                    for lhs, rhs in grammar.items():
                        if (symbol1, symbol2) in rhs:
                            table[j][i].add(lhs)

# Generate the parse trees
parse_trees = []
for lhs in table[-1][0]:
    parse_tree = build_parse_tree(words, table, lhs, 0, n - 1, grammar)
    if parse_tree is not None:
        parse_trees.append(parse_tree)

return parse_trees



def parse_lfg(sentence: str, grammar: dict, memo: dict = {}) -> Iterator[LFGParseTree]:
    """
    Parse the given sentence using the given context-free grammar.
    Yields all valid parse trees as LFGParseTree objects.
    Uses memoization to avoid recomputing parse trees for the same input.
    """
    if sentence in memo:
        yield from memo[sentence]
    elif not sentence:
        yield LFGParseTree(symbol="ROOT")
    else:
        for i, word in enumerate(sentence.split()):
            if word in grammar:
                for production in grammar[word]:
                    for parse in parse_lfg(sentence[i + 1:], grammar, memo):
                        yield LFGParseTree(symbol=production, children=(LFGParseTree(symbol=word), parse))
        memo[sentence] = list(parse_lfg(sentence, grammar, memo))


def parse_sentence(sentence: str, lexicon: dict, grammar: dict) -> List[LFGParseTree]:
    """
    Parse a given sentence and return a list of all possible valid parse trees.
    If the sentence is invalid or there are no valid parse trees, return an empty list.
    
    Parameters:
    sentence (str): The sentence to parse.
    lexicon (dict): The lexicon for the parser, mapping words to a list of possible parts of speech.
    grammar (dict): The grammar rules for the parser, mapping parts of speech to a list of possible production rules.
    
    Returns:
    List[LFGParseTree]: A list of all valid parse trees for the given sentence.
    """
    
    # Tag the sentence with parts of speech
    tagged_sentence = pos_tagger(sentence, lexicon)
    
    # Parse the tagged sentence using our LFG parser
    parse_trees = parse_lfg(tagged_sentence, grammar)
    
    # Validate all parse trees to ensure they are valid
    valid_trees = []
    for tree in parse_trees:
        if validate_parse_tree(tree, grammar):
            valid_trees.append(tree)
    
    # Return the list of valid parse trees
    return valid_trees



def pos_tagger(sentence: str, lexicon: dict) -> str:
    """
    Generate all possible parses for the given sentence by considering all possible parts of speech for each word.

    Args:
    - sentence: the sentence to parse, a string
    - lexicon: a dictionary with words as keys and a list of parts of speech tags as values

    Returns:
    - a generator yielding all possible parses for the sentence, as LFG parse trees
    """
    words = sentence.split()
    tags = []
    for word in words:
        if word in lexicon:
            tags.append((word, lexicon[word]))
        else:
            # Default to noun if unknown word
            tags.append((word, "N"))

    def generate_parses(tags, index=0):
        if index == len(tags):
            yield "(S)"
        else:
            word, possibles = tags[index]
            for pos in possibles:
                for parse in generate_parses(tags, index + 1):
                    yield f"(S ({pos} {word}){parse}"

    return generate_parses(tags)

def parse_lexicon(filename: str) -> Dict[str, List[str]]:
    """
    Load the lexicon from the given file and return it as a dictionary.
    
    The file is expected to contain one word and its part of speech tag per line, separated by a colon.
    Lines starting with '#' and empty lines are ignored.
    
    If a word appears multiple times in the file, all its tags are stored in a list in the dictionary.
    
    Args:
        filename (str): The name of the file to load the lexicon from.
    
    Returns:
        Dict[str, List[str]]: The lexicon as a dictionary.
    
    Examples:
        >>> parse_lexicon('lexicon.txt')
        {'the': ['D'], 'cat': ['N'], 'sat': ['V'], 'on': ['P'], 'mat': ['N'], 'fish': ['V', 'N']}
    """
    lexicon = {}
    with open(filename, 'r') as f:
        for line in f:
            # Ignore empty lines and lines starting with '#'
            if not line.strip() or line.startswith('#'):
                continue

            word, pos = line.split(':')
            word = word.strip()
            pos = pos.strip()

            if word in lexicon:
                lexicon[word].append(pos)
            else:
                lexicon[word] = [pos]
    return lexicon

def parse_grammar(filename):
    grammar = {}
    with open(filename, 'r') as f:
        for line in f:
            # Ignore empty lines and lines starting with '#'
            if not line.strip() or line.startswith('#'):
                continue

            lhs, rhs = line.split('->')
            lhs = lhs.strip()
            rhs = rhs.strip()

            if lhs in grammar:
                grammar[lhs].append(rhs)
            else:
                grammar[lhs] = [rhs]
    return grammar
