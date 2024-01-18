import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def is_noun(word):
    words = word_tokenize(word)
    tagged_words = pos_tag(words)
    
    # Check if the first word is tagged as a noun (NN or NNS)
    if tagged_words and tagged_words[0][1] in ['NN', 'NNS']:
        return True
    else:
        return False

# Example usage
word_to_check = "door"
if is_noun(word_to_check):
    print(f"{word_to_check} is a noun.")
else:
    print(f"{word_to_check} is not a noun.")
