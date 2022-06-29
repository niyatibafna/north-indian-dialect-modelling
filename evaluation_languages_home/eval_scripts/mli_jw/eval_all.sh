#!/bin/sh

GOLDDIR="../../eval_data/lexicons/hindi-urdu_source/"
PREDDIR="../../../mli_od/lexicons_jw_top5/"
OUTDIR="../../eval_results/mli_jw/"
eval_type="loose"
OUTPATH=$OUTDIR$"results_top5_hindi-urdu_source_"$eval_type".json"

mkdir -p $OUTDIR
rm $OUTPATH

for file in $(ls $GOLDDIR)
do
    echo "SEARCHING" $file
    if [[ -f $PREDDIR$file ]]
    then
        echo "FOUND" $file
        python3 ../eval.py \
        --gold_lexicon $GOLDDIR$file --pred_lexicon $PREDDIR$file \
        --eval_type $eval_type --OUTPATH $OUTPATH
    fi
done
