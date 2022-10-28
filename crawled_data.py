#! /usr/bin/env python3

import json
import os
import collections
import string
from indicnlp.tokenize import indic_tokenize

class CrawledData:

    def __init__(self):
        # self.DATAPATH = DATAPATH
        self.data = collections.defaultdict(lambda: dict())

    def preprocess(self, file_dict, remove_punctuation = True):
        '''Tokenize, remove punctuation'''

        file_dict["text"] = " ".join(file_dict["text"].split("\n"))
        file_dict["text"] = indic_tokenize.trivial_tokenize(file_dict["text"])

        #Deal with Roman characters
        avoid_chars = string.ascii_lowercase
        for idx, word in enumerate(file_dict["text"]):
            new_word = ""
            for c in word:
                new_word += c if c not in string.ascii_lowercase else ""
            file_dict["text"][idx] = new_word

        #Remove spaces
        file_dict["text"] = [word for word in file_dict["text"] if word not in {"\n", "\t", " ", ""}]

        #Remove punctuation
        if remove_punctuation:
            file_dict["text"] = [word for word in file_dict["text"] if word not in string.punctuation + "।" + "॥"]

        #Return as text string
        file_dict["text"] = " ".join(file_dict["text"])
        return file_dict
    
    def preprocess_hindialect(self, file_dict, remove_punctuation = False):
        '''For version 1.1,
        ## Removing bad letters:
        ##  - Removing the "wrong" punctuation: repeated punctuation characters
        ##  - Replacing multiple newlines by a single newline 
        ##  - Replacing all spaces with a single space
        ## Basic tokenization '''
        
        acceptable_punc = ".,;:?'" + '"'
        
        file_dict["text"] = file_dict["text"].strip("\n")
        file_dict["text"] = file_dict["text"].strip(" ")
        
        # Other char-level cleaning
        new_text = ""
        for ch in file_dict["text"]:
            # Replace weird spaces with regular spaces
            if ord(ch) in ([32, 160, 5760] + list(range(8192, 8028))):
                ch = " "                         
            
            # Remove certain punctuation
            if ch in string.punctuation and ch not in acceptable_punc:
                continue
               
            if ch in string.ascii_lowercase:
                continue
                        
            new_text += ch 
            
        
        file_dict["text"] =  " ".join(indic_tokenize.trivial_tokenize(new_text))
        # Remove mutiple newlines
        file_dict["text"] = "\n".join([word for word in file_dict["text"].split("\n") if word not in string.whitespace + ""])
        assert "\n\n" not in file_dict["text"]
        file_dict["title"] = file_dict["title"].split("/")[0].strip()

        return file_dict
            
            

        
        

    def read_crawled_data(self, DATAPATH, langs = None, remove_punctuation = True):
        '''Reads data in given path and stores results as JSON in self.data'''

        for lang in os.listdir(DATAPATH):
            if langs and lang not in langs:
                continue
            print("Getting files for {}".format(lang))
            if ".DS_Store" in lang:
                continue
            lang_dir = DATAPATH+"/"+lang+"/"
            for file in os.listdir(lang_dir):
                # print(lang_dir+"/"+file)
                if ".DS_Store" in lang_dir + file:
                    continue
                try:
                    with open(lang_dir+"/"+file, "r") as f:
                        # file.split(".")[0]
                        self.data[lang][len(self.data[lang])] = \
                        self.preprocess_hindialect(json.load(f), remove_punctuation)
                except:
                    print("Error in loading: {}/{}".format(lang, file))
                    # raise




# print("booyah2")
# cd = CrawledData("../data/crawled/folksongs/")
# cd.read_crawled_data()
# print(len(cd.data))
# print(cd.data)
