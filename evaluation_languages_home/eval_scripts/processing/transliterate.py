#transliterate source side

import string
import sys
from indictrans import Transliterator

trn = Transliterator(source='eng', target='hin', build_lookup = True)

def transliterate(text):
    return trn.transform(text)

filename = sys.argv[1]

f = open(filename, "r").read().split("\n")
source, target = list(), list()
f = [line.strip() for line in f if line != ""]
for line in f:
    if "|||" not in line:
        continue
    source.append(line.split("|||")[0].strip())
    target.append(line.split("|||")[1].strip())

assert(len(source) == len(target))

for idx in range(len(source)):
    print(transliterate(source[idx]) + " ||| " + target[idx])
