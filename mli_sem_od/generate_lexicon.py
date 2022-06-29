import os
import argparse
import math
import json
from collections import defaultdict, Counter
import pandas as pd
import editdistance
import jaro
from pyfasttext import FastText
import sys

class MLI_SEM_OD:

    def __init__(self):
        '''Initialize langs'''
        self.K = 50


    def get_args(self):
        parser = argparse.ArgumentParser(description = "Build a lexicon from 2 corpora using bilingual embeddings and \
        orthographic distance.")
        parser.add_argument("--source_file", type=str, default=None, required=True, help="Source corpus filepath")
        parser.add_argument("--target_file", type=str, default=None, required=True, help="Target corpus filepath")
        parser.add_argument("--embs_file", type=str, default=None, required=True, help="fastText bilingual embeddings file")
        parser.add_argument("--max_lexicon_length", type=int, default=math.inf, help="Maximum length of extracted lexicon")
        parser.add_argument("--min_source_freq", type=int, default=None, help="Min freq of source side words")
        parser.add_argument("--min_target_freq", type=int, default=None, help="Min freq of target side words")
        parser.add_argument("--OUTPATH", type=str, help="Path for saving lexicon (JSON)")

        return parser.parse_args()

    def read_file(self, filepath):
        '''Reads text file and returns as string'''
        with open(filepath, "r") as f:
            return f.read()

    def get_lexicon_words(self, source_words, target_words, max_lexicon_length, min_source_freq, min_target_freq=None):
        '''Decide which source-side words will be in the lexicon'''

        cand_source_words = defaultdict(lambda:0, {w:f for w, f in source_words.most_common(max_lexicon_length) if f >= min_source_freq})
#         cand_target_words = defaultdict(lambda:0, {w:f for w, f in target_words.items() if f >= min_target_freq})

        return cand_source_words, target_words

    def get_frequency_threshold(self, lang_lexicon):
        '''Logarithmic freq threshold'''

        total = sum(lang_lexicon.values())
        return math.log(total, 100) - 1

    def find_best_match(self, word, cand_target_words, weighted = False, num_targets = 5):
        '''Find best match using OD
        Here, cand_target_words are (word, sim_score) pairs. If weighted is set, the sim_scores are used,
        otherwise not.
        '''
#         vowel_range = list(range(2305, 2315)) + list(range(2317, 2325)) + list(range(2365, 2384))
        # bad_char_range = range(2364, 2367)

        if weighted:
            # dist_scores = [(cand, 1-score*(1-editdistance.eval(word, cand)/max(len(word), len(cand)))) \
            #                 for (cand, score) in cand_target_words]

            dist_scores = [(cand, 1-score*jaro.jaro_winkler_metric(word, cand)) \
                    for (cand, score) in cand_target_words]


        else:
            dist_scores = [(cand, 1 - jaro.jaro_winkler_metric(word, cand)) \
                    for (cand, score) in cand_target_words]

            # dist_scores = [(cand, editdistance.eval(word, cand)/max(len(word), len(cand))) \
            #             for (cand, score) in cand_target_words]


        # LOW IS GOOD!
        best_pairs = sorted(dist_scores, key = lambda x:x[1])[:num_targets]

        return word, best_pairs


#         min_dist, best_word = 2, ""
#         for cand in cand_target_words:
# #             ned = editdistance.eval(word, cand)/max(len(word), len(cand))
# #             if ned < min_dist:
# #                 min_dist = ned
# #                 best_word = cand
#
#             score = jaro.jaro_winkler_metric(word, cand[0])
#             if weighted:
#                 # weight by sim score
#                 score *= cand[1]
#
#             dist = 1 - score
#
#             if dist < min_dist:
#                 min_dist = dist
#                 best_word = cand[0]
#
#         return best_word, min_dist


    def get_sem_candidates(self, word, cand_target_words, K = 50):
        '''Get semantics-based candidates for a word based on bilingual embeddings'''
        nns = self.model.nearest_neighbors(word, k = K)
        # Add word itself with perfect score
        nns = [(word, 1)] + nns

        return [nn for nn in nns if nn[0] in cand_target_words]


    def build_lexicon(self, cand_source_words, cand_target_words):
        '''Build bilingual lexicon using NED'''
        lexicon = defaultdict(lambda: dict())

        for source in cand_source_words:
            sem_cands = [cand for cand in self.get_sem_candidates(source, cand_target_words, K = self.K)]
            _, top_k = self.find_best_match(source, sem_cands, weighted = True)
            lexicon[source] = {target:-score for (target, score) in top_k}

        return lexicon

    def save_lexicon(self, lexicon, OUTPATH):
        '''Dump lexicon'''
        OUTDIR = "/".join(OUTPATH.split("/")[:-1])+"/"
        if not os.path.isdir(OUTDIR):
            os.makedirs(OUTDIR)

        with open(OUTPATH, "w") as f:
            json.dump(lexicon, f, ensure_ascii = False, indent = 2)


    def driver(self, source_file, target_file, model, max_lexicon_length = math.inf, \
    min_source_freq = None, min_target_freq = None, OUTPATH = None):
        # Read files
        source_corpus = self.read_file(source_file)
        target_corpus = self.read_file(target_file)

        # Can pass either fastText model or filepath

        if isinstance(model, str):
            print("LOADING FASTTEXT")
            self.model = FastText(model)

        # Filter
        source_words = Counter(source_corpus.split())
        target_words = Counter(target_corpus.split())

        max_lexicon_length = min(max_lexicon_length, len(source_words))
        if min_source_freq is None:
            min_source_freq = self.get_frequency_threshold(source_words)

        cand_source_words, cand_target_words = self.get_lexicon_words(source_words, target_words, \
        max_lexicon_length, min_source_freq)
#         print(min_source_freq, min_target_freq)
        # Build lexicon
        lexicon = self.build_lexicon(cand_source_words, cand_target_words)

        # Save lexicon
        if OUTPATH:
            self.save_lexicon(lexicon, OUTPATH)

    def main(self):
        args = self.get_args()
        self.driver(args.source_file, args.target_file, args.embs_file, \
        args.max_lexicon_length, args.min_source_freq, args.min_target_freq, \
        args.OUTPATH)


if __name__ == "__main__":
    obj = MLI_SEM_OD()
    obj.main()
