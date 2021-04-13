#! /bin/bash
DOWNLOADS=$1
DATA=$2

if [ "$#" -ne 2 ]; then
    echo "usage: get_$DATA_for_selected_bugs.sh DOWNLOADS DATA"
    exit
fi

./scripts/fetch/get_fixes.sh $DATA/iterations $DOWNLOADS/repos $DATA/diffs
./scripts/fetch/get_diff_stats.sh $DATA/diffs
python scripts/fetch/copy_stats.py $DATA/iterations/ $DOWNLOADS/bugs/ $DATA/
./scripts/fetch/add_locs.sh $DATA/test_cases
