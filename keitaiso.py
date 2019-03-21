from janome.tokenizer import Tokenizer

t = Tokenizer()

s = 'すもももももももものうち'

print(type(t.tokenize(s)))
# <class 'list'>

print(type(t.tokenize(s)[0]))
# <class 'janome.tokenizer.Token'>
for token in t.tokenize(s):
    print(token)