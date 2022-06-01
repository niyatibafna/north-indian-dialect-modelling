import fasttext
import sys

DATA_PATH = sys.argv[1]
MODEL_PATH = sys.argv[2]
model = fasttext.train_unsupervised(DATA_PATH, dim = 300)
model.save_model(MODEL_PATH)
