#!/usr/bin/env bash

INDIR="../../eval_data/formatted_eng_dev/"
ALIGN_DIR="../../eval_data/alignments/eng/"
LEX_DIR="../../eval_data/lexicons/eng/"
FA_DIR="../../../../fast_align/build/./fast_align"

rm -r -f $ALIGN_DIR $LEX_DIR
mkdir -p $ALIGN_DIR $LEX_DIR

for file in $(ls $INDIR)
do
    $FA_DIR -i $INDIR$file -v -o -d > $ALIGN_DIR$file
    python3 read_alignments.py $INDIR$file $ALIGN_DIR$file $LEX_DIR${file/txt/json}
done
