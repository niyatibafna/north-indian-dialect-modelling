#!/usr/bin/env python3
#Script to align 2 non-Eng files

import sys

l1 = open(sys.argv[1], "r").read().split("\n")
l2 = open(sys.argv[2], "r").read().split("\n")

l1 = [sent for sent in l1 if sent != ""]
l2 = [sent for sent in l2 if sent != ""]


eng_to_l1 = dict()
eng_to_l2 = dict()

for idx in range(len(l1)):
    l1_sent = l1[idx].split("|||")[0].strip()
    l1_eng_sent = l1[idx].split("|||")[1].strip()
    eng_to_l1[l1_eng_sent] = l1_sent

for idx in range(len(l2)):
    l2_sent = l2[idx].split("|||")[0].strip()
    l2_eng_sent = l2[idx].split("|||")[1].strip()
    eng_to_l2[l2_eng_sent] = l2_sent


for eng_sent in set(eng_to_l1.keys()).intersection(set(eng_to_l2.keys())):
    if eng_to_l1[eng_sent] != "" and eng_to_l2[eng_sent] != "":
        print(eng_to_l1[eng_sent], " ||| ", eng_to_l2[eng_sent])

# print("Source-eng sentences: ", len(l1))
# print("Hindi-eng sentences: ", len(l2))
# print("Source-hin: ", len(set(eng_to_l1.keys()).intersection(set(eng_to_l2.keys()))))
#
#
# common = set(eng_to_l1.keys()).intersection(set(eng_to_l2.keys()))
# all = set(eng_to_l1.keys()).union(set(eng_to_l2.keys()))
# uncommon = sorted(list(all - common))
#
# print("Source:")
# for u in uncommon:
#     if u in eng_to_l1.keys():
#         print(u)
#
# print("Hindi:")
# for u in uncommon:
#     if u in eng_to_l2.keys():
#         print(u)
#
#
#
# print("\n\n\n")
