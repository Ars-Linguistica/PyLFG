"""
Module for performing LFG (Lexical Functional Grammar) based translations.

This module contains the LfgTranslator class, which uses LFG grammars and lexicons to translate sentences from one language to another. The class takes in source and target language information, as well as source and target grammars and lexicons, and uses these to parse and translate sentences.
"""

class LfgTranslator:
    """
    The LfgTranslator class is used to translate sentences from one language to another using LFG (Lexical-Functional Grammar) theory.
    """
    def __init__(self, source_language: str, target_language: str, source_grammar: dict, target_grammar: dict, source_lexicon: dict, target_lexicon: dict):
        self.source_language = source_language
        self.target_language = target_language
        self.source_grammar = source_grammar
        self.target_grammar = target_grammar
        self.source_lexicon = source_lexicon
        self.target_lexicon = target_lexicon
        
    def transfer_f_structure(self, f_structure: dict) -> dict:
        """
        Translates the f-structure from the source language to the target language
        :param f_structure: the f-structure of the source language sentence
        :return: the f-structure of the target language sentence
        """
        target_f_structure = {}
        for attribute, value in f_structure.items():
            if attribute in self.source_grammar['transfer']:
                target_attribute = self.source_grammar['transfer'][attribute]
                if target_attribute in self.target_grammar['attributes']:
                    target_value = value
                    if target_attribute in self.target_lexicon:
                        target_value = self.target_lexicon[target_value]
                    target_f_structure[target_attribute] = target_value
        return target_f_structure
    
    def translate(self, sentence: str) -> str:
        """
        Translates the sentence from the source language to the target language
        :param sentence: the source language sentence
        :return: the target language sentence
        """
        parser = LfgParser(self.source_language)
        parse_trees = parser.parse(sentence)
        target_sentence = ""
        for parse_tree in parse_trees:
            f_structure = parse_tree.f_structure
            target_f_structure = self.transfer_f_structure(f_structure)
            target_sentence += generate_sentence(target_f_structure) + " "
        return target_sentence.strip()
