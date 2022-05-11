#!/bin/bash

INDIR="../../eval_data/formatted_eng_dev/"
OUTDIR="../../eval_data/formatted_hin/"
HIN_PATH=$INDIR"hindi-urdu.txt"

rm -r -f $OUTDIR
mkdir $OUTDIR

for file in $(ls $INDIR)
do
    python3 parallelize_with_hindi.py $INDIR$file $HIN_PATH > $OUTDIR$file
done
