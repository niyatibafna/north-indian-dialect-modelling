DATADIR="../data/crawled_cleaned/"
anchor="hindi-urdu"
source_file=$DATADIR$anchor".txt"
OUTDIR="lexicons/"

for lang_file in $(ls $DATADIR)
do
    lang=${lang_file/.txt/}
    echo "Processing " $lang
    target_file=$DATADIR$lang_file
    OUTPATH=$OUTDIR$anchor"_"$lang".json"
    # if [[ -f $OUTPATH ]]
    # then
    #     continue
    # fi
    python3 generate_lexicon.py --source_file $source_file --target_file $target_file \
    --max_lexicon_length 1000 --min_source_freq 5 --min_target_freq 3 \
    --OUTPATH $OUTPATH
done
