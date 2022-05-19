#!/bin/sh

GOLDDIR="../../eval_data/lexicons/hindi-urdu_source/"
PREDDIR="../../../mli_ned/lexicons/"
OUTDIR="../../eval_results/mli_ned/"
eval_type="softgold"
OUTPATH=$OUTDIR$"results_hindi-urdu_source_"$eval_type".json"

mkdir -p $OUTDIR
rm $OUTPATH

for file in $(ls $GOLDDIR)
do
    if [[ -f $PREDDIR$file ]]
    then
        echo $file
        python3 ../eval.py \
        --gold_lexicon $GOLDDIR$file --pred_lexicon $PREDDIR$file \
        --eval_type $eval_type --OUTPATH $OUTPATH
    fi
done
