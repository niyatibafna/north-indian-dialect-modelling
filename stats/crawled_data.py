#! /usr/bin/env python3

import json
import os
import collections
import string

class CrawledData:

    def __init__(self, DATAPATH):
        self.DATAPATH = DATAPATH

    def preprocess(self, file_dict, remove_punctuation = True):
        '''Tokenize, remove punctuation'''
        file_dict["text"] = " ".join(file_dict["text"].split("\n"))
        if remove_punctuation:
            file_dict["text"] = "".join([c if c not in string.punctuation+"।" else " " for c in file_dict["text"]])
#         file_dict["text"] = file_dict["text"].replace("\n", " ")
        file_dict["text"] = " ".join(file_dict["text"].split())
        return file_dict

    def read_crawled_data(self, langs = None, remove_punctuation = True):
        '''Reads data in given path and stores results as JSON
        in self.data'''
        self.data = collections.defaultdict(lambda: dict())
        for lang in os.listdir(self.DATAPATH):
            if langs and lang not in langs:
                continue
            if ".DS_Store" in lang:
                continue
            lang_dir = self.DATAPATH+"/"+lang+"/"
            for file in os.listdir(lang_dir):
                # print(lang_dir+"/"+file)
                try:
                    with open(lang_dir+"/"+file, "r") as f:
                        self.data[lang][file.split(".")[0]] = \
                        self.preprocess(json.load(f), remove_punctuation)
                except:
                    print("Error in loading: {}/{}".format(lang, file))
                    raise


print("booyah2")
# cd = CrawledData("../data/crawled/folksongs/")
# cd.read_crawled_data()
# print(len(cd.data))
# print(cd.data)
