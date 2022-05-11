#!/usr/bin/env bash
echo "FORMATTING AND CLEANING"
bash format_and_clean_all.sh
echo "TRANSLITERATING"
bash transliterate_all.sh
echo "PARALLELIZING WITH HINDI"
bash parallelize_with_hindi_all.sh
echo "ALIGNING AGAINST ENGLISH"
bash read_alignments_all_eng.sh
echo "ALIGNING AGAINST HINDI"
bash read_alignments_all_hin.sh
