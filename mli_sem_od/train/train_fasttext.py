import fasttext
import sys
import math

DATA_PATH = sys.argv[1]
MODEL_PATH = sys.argv[2]

try:
    threshold = sys.argv[3]
except:
    threshold = 5

# lang_data = open(DATAPATH, "r").read()
# threshold = math.log(len(lang_data), 100) - 1

model = fasttext.train_unsupervised(DATA_PATH, dim = 300, minCount = threshold)
model.save_model(MODEL_PATH)
