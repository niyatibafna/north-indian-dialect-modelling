import string
from collections import defaultdict

source, target = list(), list()
f = open("hin-mag_formatted.txt", "r").read().split("\n")
f = [line for line in f if line != ""]
for line in f:
    if "|||" not in line:
        continue
    source.append(line.split("|||")[0].strip())
    target.append(line.split("|||")[1].strip())


alignments = open("alignments/hin-mag.align", "r").read().split("\n")
alignments = [alignment for alignment in alignments if alignment != ""]

assert(len(source) == len(target) == len(alignments))

dictionary = defaultdict(lambda: defaultdict(lambda: 0))

for idx in range(len(alignments)):
    print(source[idx])
    print(target[idx])

    source_words = source[idx].strip().split()
    target_words = target[idx].strip().split()
    align = [(int(x.split("-")[0]), int(x.split("-")[1])) for x in alignments[idx].strip().split()]
    for a in align:
        sw, tw = source_words[a[0]], target_words[a[1]]
        dictionary[sw][tw] += 1
        print(sw, tw)
    print("\n\n")


for word in dictionary:
    print(word)
    print(dict(dictionary[word]))
    print("\n\n")
