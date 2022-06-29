DATADIR="../data/crawled_cleaned/"
anchor="hindi-urdu"
source_file=$DATADIR$anchor".txt"
K=50
OUTDIR="lexicons_K"$K"_top5_target0_noempty/"
EMBSPATH="../mli_sem_od/models/upsampled/"
PARAMSDIR="params_K50_target0_noempty/"

for lang_file in $(ls $DATADIR)
do
    lang=${lang_file/.txt/}
    echo "Processing " $lang
    target_file=$DATADIR$lang_file
    embs_file=$EMBSPATH$lang$"_"$anchor".bin"
    OUTPATH=$OUTDIR$anchor"_"$lang".json"
    if [[ $anchor == $lang ]]
    then
        continue
    fi
    python3 generate_lexicon.py \
    --source_file $source_file --target_file $target_file \
    --model $embs_file \
    --max_lexicon_length 5000 --min_source_freq 5 \
    --iterations 500 \
    --PARAMS_DIR $PARAMSDIR --OUTPATH $OUTPATH
done
