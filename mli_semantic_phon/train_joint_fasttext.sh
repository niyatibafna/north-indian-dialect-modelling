#!/usr/bin/env bash
DATADIR="../data/crawled_cleaned/"
JOINT_DIR="../data/temp_joint/"
anchor="hindi-urdu"
ANCH_PATH=$DATADIR$anchor".txt"
JOINT_MODEL_DIR="models/joint/"

mkdir -p $JOINT_DIR
mkdir -p $JOINT_MODEL_DIR

for file in $(ls $DATADIR)
do
    echo $file
    lang=${file/".txt"/}
    echo "READING DATA..."
    LANG_PATH=$DATADIR$file
    JOINT_PATH=$JOINT_DIR$lang$anchor".txt"
    $(cat $ANCH_PATH $LANG_PATH > $JOINT_PATH)
    echo "TRAINING..."
    python3 train_fasttext.py \
    $JOINT_PATH $JOINT_MODEL_DIR$lang"_"$anchor".bin"
    echo "DONE!"
done
