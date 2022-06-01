#!/usr/bin/env bash

INDIR="../../eval_data/formatted_hin/"
ALIGN_DIR="../../eval_data/alignments/hin/"
# LEX_DIR="../../eval_data/lexicons/hindi-urdu_source/"
LEX_DIR="../../eval_data/lexicons/hindi-urdu_target/"
FA_DIR="../../../../fast_align/build/./fast_align"

rm -r -f $ALIGN_DIR $LEX_DIR
mkdir -p $ALIGN_DIR $LEX_DIR

for file in $(ls $INDIR)
do
    $FA_DIR -i $INDIR$file -v -o -d > $ALIGN_DIR$file
    #For Hindi as source:
    # python3 read_alignments.py $INDIR$file $ALIGN_DIR$file $LEX_DIR"hindi-urdu_"${file/.txt/}".json"
    #For Hindi as target:
    python3 read_alignments.py $INDIR$file $ALIGN_DIR$file $LEX_DIR${file/.txt/}"_hindi-urdu.json"
done
