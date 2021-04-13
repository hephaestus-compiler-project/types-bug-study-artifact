#!/bin/bash
# Append LOCs to stats.json
TESTS=$1

if [ "$#" -ne 1 ]; then
    echo "usage: add_locs.sh TEST_CASES"
    exit
fi


main ()
{
  for f in $(ls $TESTS); do
    lang="${TESTS}/$f"
    for t in $(ls $lang); do
      echo "$t"
      old_pwd=$(pwd)
      cd $lang/$t
      cat stats.json | \
          jq --arg loc $(cloc --exclude-lang=JSON --sum-one --csv . | \
          tail -1 | cut -d ',' -f5 ) '. + {loc: $loc}' > stats_locs.json
      cd $old_pwd
    done
  done
}

main
