#!/bin/sh

GOLDDIR="../../eval_data/hindi2nepali_bil_lex.json"
PREDDIR="../../../mli_od/lexicons_ned_top5/"
OUTDIR="../../eval_results/mli_ned/"
OUTPATH=$OUTDIR$"results_nepwbst_top5.json"

mkdir -p $OUTDIR
rm $OUTPATH

file="hindi-urdu_nepali.json"
# echo "SEARCHING" $file
# if [[ -f $PREDDIR$file ]]
# then
echo "FOUND" $file
python3 ../../eval.py \
--gold_lexicon $GOLDDIR --pred_lexicon $PREDDIR$file \
--OUTPATH $OUTPATH
# fi
