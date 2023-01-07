# Types

D = "Determiner"  # a, an, the
N = "Noun"  # cat, mat, dog
V = "Verb"  # sit, sleep, run
P = "Preposition"  # on, in, under
Adv = "Adverb"  # quickly, slowly
Adj = "Adjective"  # big, small

# Production rules

S -> NP VP
S -> NP VP Adv
S -> NP VP PP
S -> NP VP PP Adv

NP -> D N
NP -> D N PP
NP -> D N Adj
NP -> D N Adj N
NP -> D N PP Adj N
NP -> D N Adj N PP

VP -> V
VP -> V NP
VP -> V NP Adv
VP -> V NP PP
VP -> V NP PP Adv
VP -> V NP NP
VP -> V NP NP Adv
VP -> V NP NP PP
VP -> V NP NP PP Adv

PP -> P NP
