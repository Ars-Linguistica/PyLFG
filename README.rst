PyLFG - A Python package for parsing sentences using Lexical Functional Grammar (LFG)
=====================================================================================

Introduction
------------

PyLFG (Python Library for Lexical Functional Grammar) is a new
open-source project that aims to provide a comprehensive set of tools
for working within the Lexical Functional Grammar (LFG) formalism. LFG
is a syntactic theory that represents the structure of natural language
using a combination of lexical and functional information. This project
provides a set of classes and methods for representing and manipulating
LFG structures, including lexical functional structures (f-structures)
and c-structures.

PyLFG’s primary goal is to make LFG research more accessible to a wider
community by providing a fully modular library that allows researchers
to easily try new ideas and improve existing ones. The library will not
only parse sentences but also generate sentences from f-structures, and
it will have transfer capabilities to do automated translation.

PyLFG is also designed to be user-friendly, providing both a TUI
(Terminal User Interface) and a WebUI for easy interaction. The library
being written in Python makes it perfectly suited for linguistics
students who are taught Python in university.

The lack of open-source LFG parsers is a significant problem in the
field of linguistics research. Many academically developed LFG parsers
have been abandoned by their authors, making them inaccessible to the
wider community. This is a major obstacle for researchers who are
interested in studying LFG, as they are often forced to rely on
proprietary software that is difficult to access and modify.

The open-source nature of PyLFG is crucial in addressing this problem.
By providing an open-source LFG parser, PyLFG aims to make LFG research
more accessible to a wider community, allowing researchers to easily try
new ideas and improve existing ones. The ability to view and modify the
source code of the library also allows for greater transparency and
reproducibility in research, which is essential for the advancement of
knowledge.

Moreover, PyLFG’s open-source nature allows for collaboration and
contributions from the wider community. This can lead to the development
of new features and improvements in the library, making it a valuable
tool for linguistics students and professors, language learning
applications, and documenting under-resourced languages.

Open science is the best way of spreading and furthering knowledge, and
PyLFG aims to contribute to this goal by providing a valuable tool that
can be used by researchers and practitioners alike. The open-source
nature of PyLFG will ensure that it is accessible to anyone who is
interested in studying LFG, making it an essential tool for advancing
knowledge in the field of linguistics.

Important note
~~~~~~~~~~~~~~

PyLFG is still in early development and has not yet reached a stable
release state.

Features
--------

PyLFG is designed to be a comprehensive tool for working within the
Lexical Functional Grammar (LFG) formalism, providing a range of
features that make it a valuable tool for researchers and practitioners
alike.

-  Modularity: PyLFG is fully modular, allowing researchers to easily
   replace all parts of the LFG parsing pipeline, from tokenizing
   sentences to the rich visualizations of the x-structures. This allows
   for flexibility in trying new ideas and improving existing ones,
   making it a valuable tool for advancing knowledge in the field of
   linguistics.
-  Parsing and generation: PyLFG is not only able to parse sentences but
   also generate sentences from f-structures, which is an essential
   capability for automated translation and language learning
   applications.
-  Transfer capabilities: PyLFG has transfer capabilities which allow it
   to do automated translation between languages, making it a useful
   tool for researchers and practitioners working on natural language
   processing.
-  User-friendly interface: PyLFG provides both a TUI (Terminal User
   Interface) and a WebUI for easy interaction, making it accessible to
   a wide range of users, including students and professors who are
   taught Python in university.
-  Open-source: PyLFG is an open-source project, meaning that the source
   code is freely available for anyone to view and modify. This allows
   for greater transparency and reproducibility in research, and also
   enables collaboration and contributions from the wider community.
-  Suitable for linguistics students and professors: PyLFG is written in
   Python, which is a widely used programming language in the field of
   linguistics research. This makes it perfectly suited for linguistics
   students and professors, as well as python programmers in general.
-  Valuable tool for documenting under-resourced languages: PyLFG
   provides a valuable tool for documenting under-resourced languages,
   which is essential for preserving and studying these languages.

In summary, PyLFG is a comprehensive and user-friendly open-source tool
that provides a range of features that make it valuable for linguistics
students and professors, language learning applications, and documenting
under-resourced languages.

Use Cases
---------

PyLFG can be used in a variety of applications, making it a valuable
tool for researchers and practitioners working in a range of fields.
Some of the key use cases include:

-  Linguistics research: PyLFG is a valuable tool for linguistics
   students and professors who study syntactic theories. It can be used
   to parse sentences and generate f-structures, which can be used to
   test hypotheses and advance knowledge in the field.
-  Language learning applications: PyLFG’s ability to generate sentences
   from f-structures makes it a useful tool for language learning
   applications. It can be used to generate grammatically correct
   sentences for language learners to practice, and its transfer
   capabilities can also be used to translate between languages.
-  Documenting under-resourced languages: PyLFG’s ability to parse and
   generate sentences makes it a valuable tool for documenting
   under-resourced languages. It can be used to create grammatically
   correct sentences for use in language dictionaries and phrasebooks,
   and its transfer capabilities can also be used to translate between
   languages.
-  Natural language processing: PyLFG’s transfer capabilities and
   ability to generate sentences from f-structures make it a valuable
   tool for researchers and practitioners working on natural language
   processing. It can be used to automate the translation of sentences
   between languages, which has a wide range of applications, such as
   machine translation and language-based search engines.
-  Language-based search engines: PyLFG can be used to generate
   f-structures, which can be used to create grammatically correct
   sentences for use in language-based search engines. This makes it a
   valuable tool for researchers and practitioners working in this
   field.

In summary, PyLFG is a versatile tool that can be used in a wide range
of applications, making it a valuable tool for researchers and
practitioners working in linguistics, language learning, natural
language processing, and language-based search engines.

Technical Details
-----------------

PyLFG’s architecture is divided into five main components:

-  Tokenization: PyLFG uses the NLTK library to tokenize sentences. This
   allows users to tokenize sentences in multiple languages, including
   English, Spanish, French, and German.
-  Morphological Analysis: PyLFG uses a morphological analyzer to
   identify the base forms of words and their grammatical properties.
   This is an important step in the LFG parsing process, as it provides
   the necessary information for generating f-structures.
-  Parsing: PyLFG uses a modified version of the C-Structure Earley
   parser to parse sentences and generate f-structures. This parser is
   based on the Earley algorithm, which is a top-down parsing algorithm
   that is well-suited for parsing context-free grammars.
-  C-Structure and F-Structure Construction: PyLFG uses the information
   obtained from tokenization and morphological analysis to construct
   both C-structures and F-structures. These structures represent the
   syntactic and functional properties of sentences, respectively.
-  Visualization: PyLFG uses the Graphviz library to visualize
   f-structures. This allows users to create rich visualizations of
   f-structures, making it easy to understand and analyze the structures
   generated by the parser.

In addition, PyLFG also provides a TUI (Terminal User Interface) and a
WebUI (Web User Interface) which makes it easy for users to interact
with the library, parse sentences and visualize the f-structures

PyLFG is written in Python, which means users of the library can
leverage the wide range of libraries and frameworks available in Python,
such as NLTK and Spacy, which makes it a powerful and flexible tool for
working with LFG structures.

Contributing
------------

PyLFG is an open-source project and we welcome contributions from the
community. There are several ways to contribute, including:

-  Reporting bugs: If you find a bug in PyLFG, please report it on the
   GitHub issue tracker. Be sure to include as much information as
   possible, such as the version of PyLFG you are using, the steps to
   reproduce the bug, and any error messages you received.
-  Suggesting features: If you have an idea for a new feature in PyLFG,
   please suggest it on the GitHub issue tracker. Be sure to include as
   much detail as possible about the feature, including any relevant use
   cases or examples.
-  Writing code: If you would like to contribute code to PyLFG, please
   fork the repository on GitHub and submit a pull request. Be sure to
   follow the existing code style, and include tests and documentation
   for your changes.
-  Documentation: If you find any errors or inconsistencies in the
   documentation, or would like to suggest improvements, please let us
   know on the GitHub issue tracker.
-  Examples: If you have examples of using PyLFG in your research or
   projects, we would love to hear about them and feature them in the
   documentation.

We are looking forward to hearing from you and working together to
improve PyLFG. Thank you for considering to contribute to this project!

Please also note that by contributing to this project, you agree to
abide by our code of conduct.

Conclusion
----------

PyLFG is a powerful open-source Python library for working within the
Lexical Functional Grammar (LFG) formalism. It provides a comprehensive
set of classes and methods for representing and manipulating LFG
structures, including lexical functional structures (f-structures) and
c-structures. With its modular design, PyLFG allows researchers to
easily experiment with new ideas and customize their LFG parsing
pipeline.

By making PyLFG open-source, we aim to contribute to the goal of open
science and the spread and advancement of knowledge in the field of
linguistics.

We invite the community to contribute to the development of PyLFG by
reporting bugs, suggesting new features, writing code, improving
documentation and sharing examples of using PyLFG. We are looking
forward to working together to improve PyLFG and make it an even more
powerful tool for researchers in the field of linguistics.

Usage
-----

The package provides helper functions for loading grammar rules and
lexicon from files, and a ``LFGParseTree`` and ``LFGParseTreeNode``
class for representing and visualizing parse trees. Here is an example
of how to use the package:

.. code:: python

   from pylfg import build_parse_trees


   sentence = "the cat sits on the mat"

   # load grammar and lexicon
   grammar = load_grammar("path/to/grammar.txt")
   lexicon = load_lexicon("path/to/lexicon.txt")

   # parse sentence
   trees = build_parse_trees(sentence, grammar, lexicon)

   # print the first parse tree
   print(trees[0])

You can also use the LFGParseTree.to_f_structure method to export the
f-structure of the sentence in latex format, as shown in this example

.. code:: python

   f_structure = trees[0].to_f_structure()

   # write f-structure to a latex file
   with open("f_structure.tex", "w") as f:
       f.write(f_structure)
