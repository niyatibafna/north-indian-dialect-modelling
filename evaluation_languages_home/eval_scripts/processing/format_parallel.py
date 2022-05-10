import string
import sys

filename = sys.argv[1]

f = open(filename, "r").read().split("\n")
f = [line.strip() for line in f if line != ""]

source = [f[idx] for idx in range(len(f)) if idx%2 == 1]
target = [f[idx] for idx in range(len(f)) if idx%2 == 0]

for idx, sent in enumerate(source):
    clean = "".join([c for c in sent if c not in string.punctuation])
    source[idx] = clean.lower()

for idx, sent in enumerate(target):
    clean = "".join([c for c in sent if c not in string.punctuation])
    target[idx] = clean.lower()

assert(len(source) == len(target))

parallel_data = list()
for idx in range(len(source)):
    parallel_data.append(source[idx] + " ||| " + target[idx])

for sent in parallel_data:
    print(sent)
