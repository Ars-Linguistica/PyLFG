# Types

D = "Determiner"  # a, an, the
N = "Noun"  # cat, mat, dog, book, house, tree
V = "Verb"  # sit, sleep, run, read, live, climb
P = "Preposition"  # on, in, under, with, by, near
Adv = "Adverb"  # quickly, slowly, carefully, happily, silently
Adj = "Adjective"  # big, small, red, blue, happy, green
Pro = "Pronoun"  # I, you, he, she, it, we, they, me, him, her
Conj = "Conjunction"  # and, or, but, because, while

# Production rules

# Simple sentences
S -> NP VP
S -> NP VP Adv
S -> NP VP PP
S -> NP VP PP Adv

# Noun phrases
NP -> D N
NP -> D N PP
NP -> D N Adj
NP -> D N Adj N
NP -> D N PP Adj N
NP -> D N Adj N PP
NP -> Pro
NP -> N

# Verb phrases
VP -> V
VP -> V NP
VP -> V NP Adv
VP -> V NP PP
VP -> V NP PP Adv
VP -> V NP NP
VP -> V NP NP Adv
VP -> V NP NP PP
VP -> V NP NP PP Adv
VP -> V PP

# Prepositional phrases
PP -> P NP

# Compound sentences
S -> S Conj S

# Complex sentences
S -> S Conj VP
S -> S Conj NP VP
S -> S Conj NP VP Adv
S -> S Conj NP VP PP
S -> S Conj NP VP PP Adv

# Modal auxiliaries
VP -> Mod V
VP -> Mod V NP
VP -> Mod V NP Adv
VP -> Mod V NP PP
VP -> Mod V NP PP Adv
VP -> Mod V NP NP
VP -> Mod V NP NP Adv
VP -> Mod V NP NP PP
VP -> Mod V NP NP PP Adv
VP -> Mod V PP

Mod -> 'can'
Mod -> 'could'
Mod -> 'may'
Mod -> 'might'
Mod -> 'must'
Mod -> 'shall'
Mod -> 'should'
Mod -> 'will'
Mod -> 'would'
