#!/bin/bash
INDIR="../../eval_data/raw/"
OUTDIR="../../eval_data/formatted/"

mkdir $OUTDIR
for file in $(ls $INDIR)
do
    python3 format_parallel.py $INDIR$file >> $OUTDIR${file/raw/formatted}
done
