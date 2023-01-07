# Types

D = "Determiner"  # a, an, the
N = "Noun"  # cat, mat, dog, book
V = "Verb"  # sit, sleep, run, read
P = "Preposition"  # on, in, under, with
Adv = "Adverb"  # quickly, slowly, carefully
Adj = "Adjective"  # big, small, red, blue
Pro = "Pronoun"  # I, you, he, she, it, we, they
Conj = "Conjunction"  # and, or, but

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

# Types

D = "Determiner"  # a, an, the
N = "Noun"  # cat, mat, dog, book, house
V = "Verb"  # sit, sleep, run, read, live
P = "Preposition"  # on, in, under, with, by
Adv = "Adverb"  # quickly, slowly, carefully, happily
Adj = "Adjective"  # big, small, red, blue, happy
Pro = "Pronoun"  # I, you, he, she, it, we, they, me
Conj = "Conjunction"  # and, or, but, because

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
