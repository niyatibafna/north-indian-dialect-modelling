#!/usr/bin/env python3
from tqdm import tqdm
import os
import argparse
import math
import json
from collections import defaultdict, Counter
import pandas as pd
import editdistance
import Levenshtein as lv
import copy
import random
from pyfasttext import FastText

class MLI_SEM_EMOD:

    def __init__(self):

        self.prev_trans_matrix = defaultdict(lambda:defaultdict(lambda:0))
        self.trans_matrix = defaultdict(lambda:defaultdict(lambda:0))
        self.totals = defaultdict(lambda:1)

        self.seen = defaultdict(lambda:set())
        self.null_char = "NULL"

        self.init_same_char_counts = 1
        self.init_total = 2

        self.training = False

        self.sem_nns = dict()
        self.K = 50 #nearest neighbours taken into consideration


    def get_args(self):
        parser = argparse.ArgumentParser(description = "Build a lexicon from 2 corpora using iterative OD.")
        parser.add_argument("--source_file", type=str, default=None, required=True, help="Source corpus filepath")
        parser.add_argument("--target_file", type=str, default=None, required=True, help="Target corpus filepath")
        parser.add_argument("--model", type=str, default=None, required=True, help="fastText bilingual embeddings file")
        parser.add_argument("--max_lexicon_length", type=int, default=math.inf, help="Maximum length of extracted lexicon")
        parser.add_argument("--min_source_freq", type=int, default=None, help="Min freq of source side words")
        parser.add_argument("--min_target_freq", type=int, default=None, help="Min freq of target side words")
        parser.add_argument("--iterations", type=int, default=50, help="Maximum EM iterations")
        parser.add_argument("--batch_size", type=int, default=100, help="Batch size for a single iteration")
        parser.add_argument("--updates", type=int, default=10, help="Number of updates per iterations")
        parser.add_argument("--load_pretrained_model", action="store_true", help="Will load model parameters from PARAMS_DIR")
        parser.add_argument("--OUTPATH", type=str, help="Path for saving lexicon (JSON)")
        parser.add_argument("--PARAMS_DIR", type=str, help="Directory path for saving model parameters")

        return parser.parse_args()

    def read_file(self, filepath):
        '''Reads text file and returns as string'''
        with open(filepath, "r") as f:
            return f.read()

    def get_frequency_threshold(self, lang_lexicon):
        '''Logarithmic freq threshold'''

        total = sum(lang_lexicon.values())
        return math.log(total, 100) - 1


    def get_lexicon_words(self, source_words, target_words,\
                          min_source_freq, min_target_freq):
        '''Decide which source-side words will be in the lexicon'''

        cand_source_words = defaultdict(lambda:0, {w:f for w, f in source_words.items() if f >= min_source_freq})
        cand_target_words = defaultdict(lambda:0, {w:f for w, f in target_words.items() if f >= min_target_freq})

        return cand_source_words, cand_target_words


    def initialize_trans_matrix(self, cand_source_words, cand_target_words, type = "uniform"):
        '''Initialize transition matrix and totals matrix, including insertions and deletions'''

        print("Intializing TRANSITION MATRIX...")
        source_chars = set("".join(word for word in cand_source_words))
        source_chars.add(self.null_char)
        target_chars = set("".join(word for word in cand_target_words))
        target_chars.add(self.null_char)

        total_targets = len(target_chars)

        for source in source_chars:
            for target in target_chars:
                if source == target:
                    self.trans_matrix[source][target] = self.init_same_char_counts
                    continue

                if source in target_chars:
                    self.trans_matrix[source][target] = \
                    (self.init_total-self.init_same_char_counts)/(total_targets-1)

                else:
                    self.trans_matrix[source][target] = \
                    self.init_total/total_targets

        print("Intialized TRANSITION MATRIX of dimensions {}x{}".format(len(source_chars)+1, len(target_chars)+1))

    def initialize_model_params(self, iterations, batch_size, updates, \
                                cand_source_words, cand_target_words, \
                                load_pretrained_model = False, PARAMS_DIR = None):
        '''Initializes training params'''


        self.batch_size = batch_size
        self.iterations = iterations
        self.updates = updates

        if load_pretrained_model:
            print("Loading pretrained...")
            self.load_model_params(PARAMS_DIR)
        else:
            self.initialize_trans_matrix(cand_source_words, cand_target_words)

        #self.totals and self.seen are already correctly initialized


    def op2chars(self, op, source, target):
        '''Returns chars based on levenshtein op'''

        if op[0] == "replace":
            char1 = source[op[1]]
            char2 = target[op[2]]
        if op[0] == "insert":
            char1 = self.null_char
            char2 = target[op[2]]
        if op[0] == "delete":
            char1 = source[op[1]]
            char2 = self.null_char
        if op[0] == "retain":
            char1 = source[op[1]]
            char2 = source[op[1]]

        return char1, char2

    def augmented_ops(self, source, target):
        '''Returns minimal ed ops but also char retentions'''
        ops = lv.editops(source, target)
        bad_sidxs = {sidx for (op, sidx, _) in ops if op != "insert"}
        ret_idxs = [("retain", sidx) for sidx in range(len(source)) if sidx not in bad_sidxs]
        return ops + ret_idxs


    def update_params(self, pair):
        '''Update matrix counts given a new observation'''
        (source, target) = pair
        ops = self.augmented_ops(source, target)

        for op in ops:

            char1, char2 = self.op2chars(op, source, target)

            self.trans_matrix[char1][char2] += 1
            self.totals[char1] += 1


    def update_params_all(self, pairs):
        '''Update all paramaters for a collection of pairs'''

        self.prev_trans_matrix = copy.deepcopy(self.trans_matrix)

        for pair in pairs:
            if pair[1] not in self.seen[pair[0]]:
                self.seen[pair[0]].add(pair[1])
                self.update_params(pair)


    def check_convergence(self):
        return self.trans_matrix == self.prev_trans_matrix


    def find_neg_log_prob(self, source, target):
        '''Find log probability of source --> target using trans matrix'''
        ops = self.augmented_ops(source, target)
        log_prob = 0
        for op in ops:
            char1, char2 = self.op2chars(op, source, target)
            try:
                log_prob += math.log(self.trans_matrix[char1][char2]/self.totals[char1])
            except:
                continue
#                 print(char1, char2)
#                 print(source, target)
#                 print(self.trans_matrix[char1][char2])
#                 print(self.totals[char1])
#                 print(self.trans_matrix[char1][char2]/self.totals[char1])



        return -log_prob

    def get_sem_candidates(self, word, cand_target_words, K = 50):
        '''Get semantics-based candidates for a word based on bilingual embeddings'''

        if word not in self.sem_nns:
            nns = self.model.nearest_neighbors(word, k = K)
            self.sem_nns[word] = {nn for nn in nns if nn[0] in cand_target_words}

        if not self.training and word in cand_target_words:
            self.sem_nns[word].add((word,1))
            # print("2", word in self.sem_nns[word])

        return self.sem_nns[word]

    def find_best_match(self, source, cand_target_words, num_targets = 5):
        '''Find best match for source over cand words'''
        if self.training:
            min_dist, best_word = math.inf, ""
            for cand in cand_target_words:
                if cand.strip() == "" or source == cand:
                    continue
                dist_score = self.find_neg_log_prob(source, cand)
                if dist_score < min_dist:
                    min_dist = dist_score
                    best_word = cand
            return source, best_word, min_dist

        # cand_target_words.append(source)
        dist_scores = [(cand, self.find_neg_log_prob(source, cand)) for cand in cand_target_words]
        best_pairs = sorted(dist_scores, key = lambda x:x[1])[:num_targets]

        return source, best_pairs



    def choose_best_pairs(self, cand_source_words, cand_target_words, updates = None):
        '''Find best matches for all and select top self.K'''

        if not updates:
            updates = self.updates

        dist_scores = list()

        for source in cand_source_words:
            sem_cands = [cand[0] for cand in self.get_sem_candidates(source, cand_target_words, K = self.K)]
            # throwing away sem sim scores
            best_match = self.find_best_match(source, sem_cands)
            if best_match[1].strip() != "":
                dist_scores.append(best_match)


        best_pairs = sorted(dist_scores, key = lambda x:x[2])[:updates]

        return best_pairs


    def get_batch(self, cand_source_words, batch_size = None):
        '''Randomly choose batch based on pre-set batch size'''
        if batch_size is None:
            batch_size = self.batch_size
        cand_source_words = list(cand_source_words.keys())
        return random.choices(cand_source_words, k = self.batch_size)


    def em_iterations(self, cand_source_words, cand_target_words):

        self.training = True

        for it in tqdm(range(self.iterations)):
#             print("Running iteration: {}".format(it+1))

            batch_source_words = self.get_batch(cand_source_words)

            # EXPECTATION
#             print("E-Step")
            best_pairs = self.choose_best_pairs(batch_source_words, cand_target_words)
            best_pairs = [(trip[0], trip[1]) for trip in best_pairs]
            if it % 20 == 0 and it:
                print("Words chosen for updates : ", best_pairs)

            # MAXIMISATION
#             print("M-Step")
            self.update_params_all(best_pairs)

            # CHECK FOR CONVERGENCE
#             if self.check_convergence():
#                 print("Converged!")
#                 break

        self.training = False

    def dump_model_params(self, PARAMS_DIR):
        '''Save model params for inspection and continued training'''
        if not os.path.isdir(PARAMS_DIR):
            os.makedirs(PARAMS_DIR)

        with open(PARAMS_DIR+"trans_matrix.json", "w") as f:
            json.dump(self.trans_matrix, f, ensure_ascii = False, indent = 2)

        with open(PARAMS_DIR+"totals.json", "w") as f:
            json.dump(self.totals, f, ensure_ascii = False, indent = 2)


        with open(PARAMS_DIR+"seen.json", "w") as f:
            seen = {source:list(target_set) for source, target_set in self.seen.items()}
            json.dump(seen, f, ensure_ascii = False, indent = 2)

    def load_model_params(self, PARAMS_DIR):
        '''Initialize by loading pre-trained params'''
        with open(PARAMS_DIR+"trans_matrix.json", "r") as f:
            self.trans_matrix = json.load(f)

        with open(PARAMS_DIR+"totals.json", "r") as f:
            self.totals = json.load(f)


        with open(PARAMS_DIR+"seen.json", "r") as f:
            self.seen = json.load(f)
            self.seen = {source:set(target_set) for source, target_set in self.seen.items()}



    def build_lexicon(self, cand_source_words, cand_target_words, max_lexicon_length):
        '''Build bilingual lexicon using current model parameters'''

        max_lexicon_length = min(max_lexicon_length, len(cand_source_words))
        cand_source_words = defaultdict(lambda:0, \
                                        {w:f for w, f in Counter(cand_source_words).most_common(max_lexicon_length)})

        lexicon = defaultdict(lambda: dict())

        for source in cand_source_words:
            sem_cands = [cand[0] for cand in self.get_sem_candidates(source, cand_target_words, K = self.K)]
            _, top_k = self.find_best_match(source, sem_cands)
            lexicon[source] = {target:-score for (target, score) in top_k}

        return lexicon


    def save_lexicon(self, lexicon, OUTPATH):
        '''Dump lexicon'''
        OUTDIR = "/".join(OUTPATH.split("/")[:-1])+"/"
        if not os.path.isdir(OUTDIR):
            os.makedirs(OUTDIR)

        with open(OUTPATH, "w") as f:
            json.dump(lexicon, f, ensure_ascii = False, indent = 2)


    def driver(self, source_file, target_file, model, \
               max_lexicon_length = math.inf, min_source_freq = None, min_target_freq = None, \
               iterations = 50, batch_size = 100, updates = 20, \
               load_pretrained_model = False, \
               OUTPATH = None, PARAMS_DIR = None):


        # Read files
        print("Not allowing empty targets")
        source_corpus = self.read_file(source_file)
        target_corpus = self.read_file(target_file)

        # Read model instance
        if isinstance(model, str):
            print("LOADING FASTTEXT")
            model = FastText(model)

        # Filter
        source_words = Counter(source_corpus.split())
        target_words = Counter(target_corpus.split())
        if min_source_freq is None:
            min_source_freq = self.get_frequency_threshold(source_words)
        if min_target_freq is None:
            # min_target_freq = self.get_frequency_threshold(target_words)
            min_target_freq = 0

        cand_source_words, cand_target_words = self.get_lexicon_words(source_words, target_words, \
                                                                      min_source_freq, min_target_freq)



        # TODO: Add options for different types of initialization

        self.initialize_model_params(iterations, batch_size, updates, \
                                     cand_source_words, cand_target_words, \
                                     load_pretrained_model, PARAMS_DIR)

        self.model = model

        # TRAIN MODEL
        self.em_iterations(cand_source_words, cand_target_words)

        if PARAMS_DIR:
            self.dump_model_params(PARAMS_DIR)



        # BUILD LEXICON

#         batch_source_words = self.get_batch(cand_source_words, 100)
#         best_pairs = self.choose_best_pairs(batch_source_words, cand_target_words)
#         print(best_pairs)

        print("BUILDING LEXICON")
        lexicon = self.build_lexicon(cand_source_words, cand_target_words, max_lexicon_length)

        # Save lexicon
        if OUTPATH:
            self.save_lexicon(lexicon, OUTPATH)

        # Dump model parameters

        return lexicon


    def main(self):
        args = self.get_args()
        self.driver(args.source_file, args.target_file, args.model, \
        args.max_lexicon_length, args.min_source_freq, args.min_target_freq, \
        args.iterations, args.batch_size, args.updates, \
        args.load_pretrained_model, \
        args.OUTPATH, args.PARAMS_DIR)

if __name__ == "__main__":
    obj = MLI_SEM_EMOD()
    obj.main()
