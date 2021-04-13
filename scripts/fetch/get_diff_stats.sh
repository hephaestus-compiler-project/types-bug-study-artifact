#!/bin/bash
DIFFS=$1

if [ "$#" -ne 1 ]; then
    echo "usage: get_diff_stats.sh DIFFS"
    exit
fi

main ()
{
  for lang in $(ls -d $DIFFS/*); do
    echo "Process: $lang"
    for bug in $(ls $lang); do
      for diff in $(ls $lang/$bug/*.diff); do
        cat $diff | diffstat -t -w 10000 -N 10000 -p 0 > $lang/$bug/stats.csv
        [ $(cat $lang/$bug/stats.csv | wc -l) == "1" ] && \
            echo "$lang/$bug/stats.csv is empty"
      done
    done
  done
}

main
