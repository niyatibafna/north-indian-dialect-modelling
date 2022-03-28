#! /usr/bin/env python3
import os
import json
DATA_FOLDER = "../data/crawled/poetry/"

for dir in os.listdir(DATA_FOLDER):
    if ".DS" in dir or "count" in dir:
        continue
    print(dir)
    # dir_path = DATA_FOLDER+dir+"/"
    # token_count = 0
    # poem_count = 0
    # for file in os.listdir(dir_path):
    #     poem_count += 1
    #     try:
    #         with open(dir_path+file, "r") as f:
    #             poem_info = json.load(f)
    #         token_count += len(poem_info["text"].split(" "))
    #     except:
    #         print("Something weird happened")
    #
    # # print(str(dir) + "\t"+ str(token_count))
    # print(token_count)
    # print(poem_count)
