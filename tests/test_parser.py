from PyLFG.parser import build_parse_trees, parse_grammar, parse_lexicon
from PyLFG.parse_tree import LFGParseTree, LFGParseTreeNodeF
from pathlib import Path
import pytest



def test_build_parse_trees():
    grammar_file = os.path.join(os.path.dirname(__file__), "..", "EN", "grammar.txt")
    with open(grammar_file, "r") as f:
        grammar_str = f.read()
    grammar = json.loads(grammar_str)
    
    lexicon_file = os.path.join(os.path.dirname(__file__), "..", "EN", "lexicon.txt")
    with open(lexicon_file, "r") as f:
        lexicon_str = f.read()
    lexicon = json.loads(lexicon_str)

    parse_trees = build_parse_trees("The cat sits on the book.", grammar, lexicon)

    assert len(parse_trees) == 1
    tree = parse_trees[0]
    assert isinstance(tree, LFGParseTree)
    assert tree.to_string() == "(S (NP (D (the)) (N (cat))) (VP (V (sits)) (PP (P (on)) (NP (D (the)) (N (book)))))"
    
    f_structure = tree.f_structure_matrix()
    assert f_structure["SUBJ"] == "the cat"
    assert f_structure["PRED"] == "sits on the book"
    assert f_structure["MOD"] == None

    nodes = tree.get_all_nodes()
    for node in nodes:
        if node.label == "cat":
            assert node.get_functional_label("PRED") == "cat"
            assert node.get_all_f_structure() == {}
        if node.label == "sits":
            assert node.get_functional_label("PRED") == "sits<SUBJ.sit_1stArg>"
            assert node.get_functional_label("TENSED") == "-"
            assert node.get_functional_label("ASPECT") == "IMPERFECTIVE"
            assert node.get_all_f_structure() == {"PRED":"sits<SUBJ.sit_1stArg>", "TENSED":"-", "ASPECT":"IMPERFECTIVE"}

def test_parse_grammar():
    path = Path('EN')
    grammar_path = path / 'grammar.txt'
    lexicon_path = path / 'lexicon.txt'
    expected_grammar = {
        'S': [['NP', 'VP', '[Adv]'], ['NP', 'VP', 'PP', '[Adv]'], ['PRO', 'VP', '[Adv]'], ['PRO', 'VP', 'PP', '[Adv]']],
        'NP': [['D', 'N']]
    }
    expected_lexicon = {'.': 'DOT', 'the': 'D', 'cat': 'N', 'dog': 'N', 'book': 'N', 'house': 'N', 'tree': 'N', 'sit': 'V', 'sleep': 'V', 'run': 'V', 'read': 'V', 'live': 'V', 'climb': 'V', 'on': 'P', 'in': 'P', 'under': 'P', 'with': 'P'}
    grammar, lexicon = parse_grammar(grammar_path, lexicon_path)
    assert grammar == expected_grammar
    assert lexicon == expected_lexicon

def test_parse_lexicon():
    lexicon = parse_lexicon("tests/EN/lexicon.txt")
    expected_lexicon = {"the": {"D": {"PRED": "the"}}, 
                        "cat": {"N": {"PRED": "cat"}}, 
                        "dog": {"N": {"PRED": "dog"}}, 
                        "book": {"N": {"PRED": "book"}}, 
                        "house": {"N": {"PRED": "house"}}, 
                        "tree": {"N": {"PRED": "tree"}}, 
                        "sit": {"V": {"PRED": "sit<SUBJ.sit_1stArg>", "TENSED": "-", "ASPECT": "IMPERFECTIVE"}}, 
                        "sleep": {"V": {"PRED": "sleep<SUBJ.sleep_1stArg>", "TENSED": "-", "ASPECT": "IMPERFECTIVE"}}, 
                        "run": {"V": {"PRED": "run<SUBJ.run_1stArg>", "TENSED": "-", "ASPECT": "IMPERFECTIVE"}}, 
                        "read": {"V": {"PRED": "read<SUBJ.read_1stArg, OBJ.read_2ndArg>", "TENSED": "-", "ASPECT": "IMPERFECTIVE"}}, 
                        "live": {"V": {"PRED": "live<SUBJ.live_1stArg>", "TENSED": "-", "ASPECT": "IMPERFECTIVE"}}, 
                        "climb": {"V": {"PRED": "climb<SUBJ.climb_1stArg>", "TENSED": "-", "ASPECT": "IMPERFECTIVE"}}, 
                        "on": {"P": {"PRED": "on"}}, 
                        "in": {"P": {"PRED": "in"}}, 
                        "under": {"P": {"PRED": "under"}}, 
                        "with": {"P": {"PRED": "with"}}}
    
    assert lexicon == expected_lexicon
    

