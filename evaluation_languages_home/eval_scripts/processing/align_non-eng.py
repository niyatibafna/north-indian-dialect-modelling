l1 = open("hin-eng_formatted.txt", "r").read().split("\n")
l2 = open("mag-eng_formatted.txt", "r").read().split("\n")
l1 = [a for a in l1 if a != ""]
l2 = [a for a in l2 if a != ""]

print(len(l1))
print(len(l2))

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
    print(eng_to_l1[eng_sent], " ||| ", eng_to_l2[eng_sent])
l2  openmagengformattedtxt rreadsplitn ||| l1  openhinengformattedtxt rreadsplitn
l2  a for a in l2 if a   ||| l1  a for a in l1 if a  
printlenl2 ||| printlenl1
engtol2  dict ||| engtol1  dict
l1sent  l1idxsplit0strip ||| for idx in rangelenl1
engtol1l1engsent  l1sent ||| l1engsent  l1idxsplit1strip
l2sent  l2idxsplit0strip ||| for idx in rangelenl2
engtol2l2engsent  l2sent ||| l2engsent  l2idxsplit1strip
printengtol1engsent    engtol2engsent ||| for engsent in setengtol1keysintersectionsetengtol2keys
['l1 = open("hin-eng_formatted.txt", "r").read().split("\\n")']
align_non-eng.py
l2  openmagengformattedtxt rreadsplitn ||| l1  openhinengformattedtxt rreadsplitn
l2  a for a in l2 if a   ||| l1  a for a in l1 if a  
printlenl2 ||| printlenl1
engtol2  dict ||| engtol1  dict
l1sent  l1idxsplit0strip ||| for idx in rangelenl1
engtol1l1engsent  l1sent ||| l1engsent  l1idxsplit1strip
l2sent  l2idxsplit0strip ||| for idx in rangelenl2
engtol2l2engsent  l2sent ||| l2engsent  l2idxsplit1strip
printengtol1engsent    engtol2engsent ||| for engsent in setengtol1keysintersectionsetengtol2keys
l2  a for a in l2 if a    l1  a for a in l1 if a ||| l2  openmagengformattedtxt rreadsplitn  l1  openhinengformattedtxt rreadsplitn
engtol2  dict  engtol1  dict ||| printlenl2  printlenl1
engtol1l1engsent  l1sent  l1engsent  l1idxsplit1strip ||| l1sent  l1idxsplit0strip  for idx in rangelenl1
engtol2l2engsent  l2sent  l2engsent  l2idxsplit1strip ||| l2sent  l2idxsplit0strip  for idx in rangelenl2
l1  openhinengformattedtxt rreadsplitn ||| printengtol1engsent    engtol2engsent  for engsent in setengtol1keysintersectionsetengtol2keys
