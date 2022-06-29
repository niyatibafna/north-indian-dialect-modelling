DATADIR="../data/crawled_cleaned/"
anchor="hindi-urdu"
source_file=$DATADIR$anchor".txt"
OUTDIR="lexicons_jw_top5/"

for lang_file in $(ls $DATADIR)
do
    lang=${lang_file/.txt/}
    echo "Processing " $lang
    target_file=$DATADIR$lang_file
    OUTPATH=$OUTDIR$anchor"_"$lang".json"
    if [[ $anchor == $lang ]]
    then
        continue
    fi
    python3 generate_lexicon.py --source_file $source_file --target_file $target_file \
    --max_lexicon_length 5000 --min_source_freq 5 \
    --OUTPATH $OUTPATH
done
