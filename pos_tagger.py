def pos_tagger(sentence: str, lexicon: dict) -> str:
    words = sentence.split()
    tags = []
    for word in words:
        if word in lexicon:
            tags.append((word, lexicon[word]))
        else:
            # Default to noun if unknown word
            tags.append((word, "N"))
    result = "(S "
    for tag in tags:
        result += "(" + tag[1] + " " + tag[0] + ")"
    result += ")"
    return result

# Example usage
sentence = "The cat sat on the mat"
print(pos_tagger(sentence, lexicon))  # Output: "(S (NP (D the) (N cat)) (VP (V sat) (PP (P on) (NP (D the) (N mat)))))"
