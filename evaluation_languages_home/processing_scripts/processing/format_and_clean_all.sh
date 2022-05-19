#!/bin/bash
INDIR="../../eval_data/raw/"
OUTDIR="../../eval_data/formatted_eng/"

mkdir -p $OUTDIR
for file in $(ls $INDIR)
do
    python3 format_and_clean.py $INDIR$file >> $OUTDIR$file
done
