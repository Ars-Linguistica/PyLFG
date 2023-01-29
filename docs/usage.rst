=====
Usage
=====

PyLFG is a package for parsing sentences using Lexical Functional Grammar (LFG).
This module provides an implementation of the Earley parsing algorithm for building parse trees
from sentences and grammar rules specified in LFG.

The primary entry point for the module is the `LfgParser` class and its main method parse(sentence), which takes a sentence string
and a set of grammar rules and lexicon and returns a list of parse trees for the sentence.

The package also provides helper functions for loading grammar rules and lexicon from files,
and a `LFGParseTree` and `LFGParseTreeNode` class for representing and visualizing parse trees,
as well as a FStructure class to represent the f-structure of the analyzed sentence.

PyLFG is designed to be compatible with both XLFG_ and XLE_ (Xerox Linguistic Environment) grammar/lexicon formats. The goal of PyLFG is to be agnostic and modular with regards to the grammar/lexicon format, meaning that it can work with different formats without being tied to a specific one. This allows PyLFG to support more formats in the future through the use of plugins.

In order to achieve this, PyLFG uses a plugin-based architecture that allows users to easily add new formats to the library. Each plugin is responsible for parsing and interpreting the specific format that it supports. This allows PyLFG to remain independent of any particular format, and to be easily extensible to support new formats as they become available.

PyLFG's compatibility with xlfg and xle formats is achieved by providing built-in plugins for these formats. These plugins allow PyLFG to parse and interpret the grammar and lexicon files in these formats, allowing users to easily use PyLFG with existing xlfg and xle grammars and lexicons.

In summary, PyLFG is designed to be a flexible and modular library for working with different grammar and lexicon formats. Its plugin-based architecture allows it to support multiple formats, including xlfg and xle, and it can easily be extended to support new formats in the future. This makes PyLFG a powerful tool for natural language processing research and development.

To use the package, you need to first create an instance of the LfgParser class, passing the format of the grammar you want to use, either "xlfg" or "xle". Then you can call the parse method on the instance, passing the sentence and the grammar rules and lexicon as arguments.

Example usage:

.. code-block:: python

    parser = LfgParser("xlfg", grammar_rules, lexicon)
    trees = parser.parse("The cat sat on the mat")


The package also provides classes for loading grammar rules and lexicon from files, such as `XlfgParser` and `XleParser` for the respective grammar formats. These classes take the path to the grammar and lexicon files as arguments and provide a parse method for parsing sentences.û

.. code-block:: python

    xlfg_parser = XlfgParser("path/to/grammar.xlfg", "path/to/lexicon.xlfg")
    trees = xlfg_parser.parse("The cat sat on the mat")


.. code-block:: python

    xle_parser = XleParser("path/to/template.xle", "path/to/features.xle", "path/to/grammar.xle", "path/to/lexicon.xle")
    trees = xle_parser.parse("The cat sat on the mat")




In addition, the package also provides the `parse_rule` and `parse_lexicon_entry` helper functions for parsing individual grammar rules and lexicon entries, and the `match_c_constraints` and `match_f_constraints` functions for checking if a given rule matches the constraints of a given lexicon entry.

The features of PyLFG are still evolving rapidly so we advise you to consult the API reference for a detailed description of all the classes provided by PyLFG.


.. _XLFG: https://xlfg.labri.fr
.. _XLE: https://ling.sprachwiss.uni-konstanz.de/pages/xle/
