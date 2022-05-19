import string
import sys

def preprocess(text):
    '''Remove English words and other junk'''
    eng_words = ["respect", "he", "she", "plural", "to",\
    "sit", "eat", "walk", "drink", "go", "m", "f"]
    text = " ".join([word for word in text.split(" ") if word not in eng_words])
    return text


filename = sys.argv[1]

f = open(filename, "r").read().split("\n")
f = [line.strip() for line in f if line != ""]

#source : 0 , English is source , source : 1, English is target
source = [f[idx] for idx in range(len(f)) if idx%2 == 1]
target = [f[idx] for idx in range(len(f)) if idx%2 == 0]

for idx, sent in enumerate(source):
    clean = "".join([c if c not in string.punctuation else " " for c in sent])
    clean = " ".join(clean.split()).lower()
    source[idx] = preprocess(clean)


for idx, sent in enumerate(target):
    clean = "".join([c if c not in string.punctuation else " " for c in sent])
    clean = " ".join(clean.split())
    target[idx] = clean.lower()

assert(len(source) == len(target))

parallel_data = list()
for idx in range(len(source)):
    parallel_data.append(source[idx] + " ||| " + target[idx])

for sent in parallel_data:
    print(sent)
