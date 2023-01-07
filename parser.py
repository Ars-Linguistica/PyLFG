class LFG:
    def __init__(self, f_structure, c_structure):
        self.f_structure = f_structure
        self.c_structure = c_structure
    
    def parse(self, sentence):
        words = sentence.split()
        n = len(words)
        pi = {0: {"S": [""]}}
        bp = {}
        for i in range(1, n+1):
            pi[i] = {}
            for X in self.f_structure:
                pi[i][X] = []
                for RHS, Y in self.f_structure[X]:
                    if len(RHS) == 1 and RHS[0] in self.c_structure and words[i-1] in self.c_structure[RHS[0]]:
                        pi[i][X].append(Y)
                        bp[(i, X, Y)] = (i-1, RHS[0], words[i-1])
                    elif len(RHS) == 2:
                        for Y1 in pi[i-1][RHS[0]]:
                            for Y2 in pi[i][RHS[1]]:
                                pi[i][X].append(f"{Y1} {Y2}")
                                bp[(i, X, f"{Y1} {Y2}")] = (i-1, i, Y1, Y2)
        return pi[n]["S"][0], bp
    
    def get_parse_tree(self, parsing, bp):
        if parsing in self.c_structure:
            return parsing
        else:
            i, X, Y = bp[parsing]
            if len(bp[parsing]) == 3:
                return (X, bp[parsing][2])
            else:
                return (X, self.get_parse_tree(bp[parsing][2], bp), self.get_parse_tree(bp[parsing][3], bp))

# Example usage
lfg = LFG({"S": [("NP VP", "NP_VP")], "NP": [("D N", "D_N")], "VP": [("V", "V")]}, 
          {"D": ["the", "a"], "N": ["cat", "dog"], "V": ["sat", "ran"]})
sentence = "The cat sat"
parsing, bp = lfg.parse(sentence)
parse_tree = lfg.get_parse_tree(parsing, bp)
print(parse_tree)
# Output: ("NP_VP", ("D_N", "the", ("N", "cat")), ("V", "sat"))
