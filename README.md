# PyLFG - A Python package for parsing sentences using Lexical Functional Grammar (LFG)

## Introduction

PyLFG (Python Library for Lexical Functional Grammar) is a new open-source project that aims to provide a comprehensive set of tools for working within the Lexical Functional Grammar (LFG) formalism. LFG is a syntactic theory that represents the structure of natural language using a combination of lexical and functional information. This project provides a set of classes and methods for representing and manipulating LFG structures, including lexical functional structures (f-structures) and c-structures.

PyLFG's primary goal is to make LFG research more accessible to a wider community by providing a fully modular library that allows researchers to easily try new ideas and improve existing ones. The library will not only parse sentences but also generate sentences from f-structures, and it will have transfer capabilities to do automated translation.

PyLFG is also designed to be user-friendly, providing both a TUI (Terminal User Interface) and a WebUI for easy interaction. The library being written in Python makes it perfectly suited for linguistics students who are taught Python in university.

The lack of open-source LFG parsers is a significant problem in the field of linguistics research. Many academically developed LFG parsers have been abandoned by their authors, making them inaccessible to the wider community. This is a major obstacle for researchers who are interested in studying LFG, as they are often forced to rely on proprietary software that is difficult to access and modify.

The open-source nature of PyLFG is crucial in addressing this problem. By providing an open-source LFG parser, PyLFG aims to make LFG research more accessible to a wider community, allowing researchers to easily try new ideas and improve existing ones. The ability to view and modify the source code of the library also allows for greater transparency and reproducibility in research, which is essential for the advancement of knowledge.

Moreover, PyLFG's open-source nature allows for collaboration and contributions from the wider community. This can lead to the development of new features and improvements in the library, making it a valuable tool for linguistics students and professors, language learning applications, and documenting under-resourced languages.

Open science is the best way of spreading and furthering knowledge, and PyLFG aims to contribute to this goal by providing a valuable tool that can be used by researchers and practitioners alike. The open-source nature of PyLFG will ensure that it is accessible to anyone who is interested in studying LFG, making it an essential tool for advancing knowledge in the field of linguistics.

### Important note
PyLFG is still in early development and has not yet reached a stable release state.



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
