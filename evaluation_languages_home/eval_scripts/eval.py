#!/usr/bin/env python3

import os
import argparse
import math
import json
from collections import defaultdict, Counter
import pandas as pd
import editdistance

class Evaluation:

    def get_args(self):
        '''Parses commandline arguments'''

        parser = argparse.ArgumentParser(description = \
        "Evalute predicted lexicon against gold lexicon")
        parser.add_argument("--gold_lexicon", type = str, \
        required = True, help = "Path to gold lexicon")
        parser.add_argument("--pred_lexicon", type = str, \
        required = True, help = "Path to predicted lexicon")
        parser.add_argument("--eval_type", type = str, \
        default = "loose", help = "Type of evaluation: {loose, hard, softgold}")
        parser.add_argument("--OUTPATH", type=str, \
        help = "Path to JSON file to store results")

        return parser.parse_args()

    def read_files(self, filepath):

        with open(filepath) as f:
            return json.load(f)

    def eval(self, gold_lexicon, pred_lexicon, type = "loose"):
        '''
        Basic accuracy-based evaluation
        (type) loose: Considers any gold option equally correct
        (type) hard: Considers only the best gold option to be correct
        '''
        accuracy, found = 0, 0
        for word in gold_lexicon:
            if word not in pred_lexicon:
                continue
            found += 1
            best_pred = max(pred_lexicon[word].keys(), key = lambda x:pred_lexicon[word][x])
            #For now, pred_targets only contains a single element
            # so it is irrelevant whether we do intersection
            # or check whether all pred targets lie in gold targets
            if type=="loose":
                if best_pred in gold_lexicon[word]:
                    accuracy += 1

            elif type=="hard":
                best_gold_score = max(gold_lexicon[word].values())
                best_golds = {word for word in gold_lexicon if gold_lexicon[word]==best_gold_score}
                if best_pred in best_golds:
                    accuracy += 1

            elif type=="softgold":
                best_gold_score = max(gold_lexicon[word].values())
                if best_pred in gold_lexicon[word]:
                    accuracy += gold_lexicon[word][best_pred]/best_gold_score

        result = {
        "accuracy":accuracy/found,
        "found":found,
        "total":len(gold_lexicon)
        }
        return result

    def save_results(self, lang, result, OUTPATH):

        try:
            results = self.read_files(OUTPATH)

        except:
            results = dict()
        results[lang] = result
        with open(OUTPATH, "w") as f:
            json.dump(results, f, ensure_ascii = False, indent=2)

    def driver(self, gold_lexicon, pred_lexicon, eval_type, OUTPATH):
        # Get the target language (currently, we take anchor as source)
        lang = gold_lexicon.split("/")[-1].split("_")[1].split(".")[0]
        # Read lexicons
        gold_lexicon = self.read_files(gold_lexicon)
        pred_lexicon = self.read_files(pred_lexicon)
        # Evaluate
        result = self.eval(gold_lexicon, pred_lexicon, type = eval_type)
        self.save_results(lang, result, OUTPATH)


    def main(self):
        args = self.get_args()
        self.driver(args.gold_lexicon, args.pred_lexicon, \
        args.eval_type, args.OUTPATH)

if __name__ == "__main__":
    obj = Evaluation()
    obj.main()
