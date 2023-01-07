test_cases = [
    ("The cat sat on the mat", "(S (NP (D the) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (N mat)))))"
    ("I can run quickly", "(S (NP (Pro I)) (VP (Mod can) (V run) (Adv quickly)))"
    ("I can run and you can run too", "(S (NP (Pro I)) (VP (Mod can) (V run)) (Conj and) (S (NP (Pro you)) (VP (Mod can) (V run) (Adv too))))"
    ("She could have eaten the apple", "(S (NP (Pro She)) (VP (Mod could) (V have) (VP (V eaten) (NP (D the) (N apple)))))"
    ("The big cat slept in the tree", "(S (NP (D the) (Adj big) (N cat)) (VP (V slept) (PP (P in) (NP (D the) (N tree)))))"
    ("The big cat slept in the tree because he was tired", "(S (NP (D the) (Adj big) (N cat)) (VP (V slept) (PP (P in) (NP (D the) (N tree)))) (Conj because) (S (NP (Pro he)) (VP (V was) (Adj tired))))"
    ("The cat sat on the mat while the dog slept", "(S (NP (D the) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (N mat)))) (Conj while) (S (NP (D the) (N dog)) (VP (V slept))))"
    ("The cat sat on the mat, which was red", "(S (NP (D the) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (N mat)))) (, which) (VP (V was) (Adj red)))"
)

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
    ("The big red cat sat on the small green mat in the house quickly.", "(S (NP (D the) (Adj big) (Adj red) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (Adj small) (Adj green) (N mat))) (PP (P in) (NP (D the) (N house))) (Adv quickly)))"),
    ("I can swim in the pool quickly because I am a good swimmer.", "(S (NP (Pro I)) (VP (Mod can) (V swim) (PP (P in) (NP

tests = [    ("The cat sat on the mat", "(S (NP (D the) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (N mat)))))"),    ("The big red cat sat on the mat", "(S (NP (D the) (Adj big) (Adj red) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (N mat)))))"),    ("The cat quickly sat on the mat", "(S (NP (D the) (N cat)) (VP (Adv quickly) (V sat) (PP (P on) (NP (D the) (N mat)))))"),    ("The cat sat on the big red mat", "(S (NP (D the) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (Adj big) (Adj red) (N mat)))))"),    ("The cat sat on the mat with the dog", "(S (NP (D the) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (N mat))) (PP (P with) (NP (D the) (N dog)))))"),    ("The cat sat on the mat because it was tired", "(S (NP (D the) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (N mat))) (Conj because) (S (NP (Pro it)) (VP (V was) (Adj tired))))))")]
