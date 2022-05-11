#!/usr/bin/env bash

INDIR="../../eval_data/formatted_eng/"
#CLEANDIR="../../eval_data/formatted_hin_clean/"
OUTDIR="../../eval_data/formatted_eng_dev/"
files=$(ls $INDIR)

rm -r -f $OUTDIR
mkdir -p $OUTDIR
# rm -r -f $CLEANDIR
# mkdir -p $CLEANDIR

for file in $files
do
    # python3 preprocess.py $INDIR$file > $CLEANDIR$file
    python3 transliterate.py $INDIR$file > $OUTDIR$file
done
