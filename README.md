# PyLFG - A Python package for parsing sentences using Lexical Functional Grammar (LFG)

## Introduction
PyLFG is a package for parsing sentences using Lexical Functional Grammar (LFG). This package provides an implementation of the Earley parsing algorithm for building parse trees from sentences and grammar rules specified in LFG. The primary entry point for the module is the `build_parse_trees` function, which takes a sentence string and a set of grammar rules and lexicon and returns a list of parse trees for the sentence.

### Important note
PyLFG is still in early development and has not yet reached a stable release state.

## Installation
To install PyLFG, use the following command:

```python
pip install pylfg
```

## Usage
The package provides helper functions for loading grammar rules and lexicon from files, and a `LFGParseTree` and `LFGParseTreeNode` class for representing and visualizing parse trees. Here is an example of how to use the package:

```python
from pylfg import build_parse_trees


sentence = "the cat sits on the mat"

# load grammar and lexicon
grammar = load_grammar("path/to/grammar.txt")
lexicon = load_lexicon("path/to/lexicon.txt")

# parse sentence
trees = build_parse_trees(sentence, grammar, lexicon)

# print the first parse tree
print(trees[0])
```

You can also use the LFGParseTree.to_f_structure method to export the f-structure of the sentence in latex format, as shown in this example

```python
f_structure = trees[0].to_f_structure()

# write f-structure to a latex file
with open("f_structure.tex", "w") as f:
    f.write(f_structure)
```
