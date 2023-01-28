import openfst_python as fst
from typing import List

class FstTokenizer:
    def __init__(self, fst_file: str):
        self.fst_file = fst_file
        self.tokenizer = fst.Fst.read(self.fst_file)

    def tokenize(self, sentence: str) -> List[str]:
        """
        Tokenize a sentence using a Finite State Transducer (FST).
        :param sentence: (str) Sentence to tokenize
        :return: (List[str]) List of tokenized words
        """
        # Create an FST acceptor from the sentence
        input_fst = fst.string_to_fst(sentence)
        # Compose the acceptor with the tokenizer
        composed = fst.compose(input_fst, self.tokenizer)
        # Extract the output strings of the composed FST
        out_strings = fst.extract_output_strings(composed)
        return out_strings


def tokenize_with_fst(sentence: str, fst_file: str) -> List[str]:
    """
    Tokenize a sentence using a Finite State Transducer (FST).
    :param sentence: (str) Sentence to tokenize
    :param fst_file: (str) File path of the FST
    :return: (List[str]) List of tokenized words
    """
    # Open the FST
    tokenizer = fst.Fst.read(fst_file)
    # Create an FST acceptor from the sentence
    input_fst = fst.string_to_fst(sentence)
    # Compose the acceptor with the tokenizer
    composed = fst.compose(input_fst, tokenizer)
    # Extract the output strings of the composed FST
    out_strings = fst.extract_output_strings(composed)
    return out_strings


class FstMorph:
    def __init__(self, fst_file: str):
        self.fst_file = fst_file
        self.morph_analyzer = fst.Fst.read(self.fst_file)

    def morphological_decomposition(self, string: str):
    """
    Given a string and the path of a FST morphological analyzer, returns the morphological decomposition of the string.

    :param string: the string to analyze
    :param fst_file: path of the FST morphological analyzer
    :return: list of tuples, where each tuple contains the morphological decomposition of a word in the string
    """
    self.morph_analyzer.set_input_symbols(self.morph_analyzer.input_symbols())
    self.morph_analyzer.set_output_symbols(self.morph_analyzer.output_symbols())
    self.morph_analyzer.set_start(self.morph_analyzer.start())
    self.morph_analyzer.set_final(self.morph_analyzer.final())
    self.morph_analyzer.set_properties(fst.Fst.EXPANDED, True)
    self.morph_analyzer.set_properties(fst.Fst.ACCEPTOR, True)

    words = string.split()
    morph_decomposition = []
        for word in words:
        self.morph_analyzer.set_input_str(word)
        self.morph_analyzer.set_output_str(word)
        self.morph_analyzer.compose(self.morph_analyzer)
        morph_decomp = []
        for path in self.morph_analyzer.paths():
            morph_decomp.append((path.input_str(), path.output_str()))
        morph_decomposition.append(morph_decomp)
    return morph_decomposition
  
  
  
