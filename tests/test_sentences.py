test_sentences = [
    ("The cat sat on the mat.", "(S (NP (D the) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (N mat)))))"),
    ("I can swim.", "(S (NP (Pro I)) (VP (Mod can) (V swim)))"),
    ("I can swim quickly.", "(S (NP (Pro I)) (VP (Mod can) (V swim) (Adv quickly)))"),
    ("I can swim in the pool.", "(S (NP (Pro I)) (VP (Mod can) (V swim) (PP (P in) (NP (D the) (N pool)))))"),
    ("I can swim in the pool quickly.", "(S (NP (Pro I)) (VP (Mod can) (V swim) (PP (P in) (NP (D the) (N pool))) (Adv quickly)))"),
    ("The cat sat on the mat while the dog slept.", "(S (NP (D the) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (N mat)))) (Conj while) (S (NP (D the) (N dog)) (VP (V slept))))"),
    ("The cat sat on the mat while the dog slept because the cat was tired.", "(S (NP (D the) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (N mat)))) (Conj while) (S (NP (D the) (N dog)) (VP (V slept))) (Conj because) (S (NP (D the) (N cat)) (VP (V was) (Adj tired))))"),
    ("The big red cat sat on the small green mat.", "(S (NP (D the) (Adj big) (Adj red) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (Adj small) (Adj green) (N mat)))))"),
    ("The big red cat sat on the small green mat quickly.", "(S (NP (D the) (Adj big) (Adj red) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (Adj small) (Adj green) (N mat))) (Adv quickly)))"),
    ("The big red cat sat on the small green mat in the house.", "(S (NP (D the) (Adj big) (Adj red) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (Adj small) (Adj green) (N mat))) (PP (P in) (NP (D the) (N house)))))"),
    ("The big red cat sat on the small green mat in the house quickly.", "(S (NP (D the) (Adj big) (Adj red) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (Adj small) (Adj green) (N mat))) (PP (P in) (NP (D the) (N house))) (Adv quickly)))"),]
