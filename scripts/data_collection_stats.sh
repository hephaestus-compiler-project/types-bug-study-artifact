#!/bin/bash
# Print stats for Data collection
BUGS=$1

if [ "$#" -ne 1 ]; then
    echo "usage: phase_1_2.sh BUGS"
    exit
fi


print_results()
{
  phase=$1
  directory=$2
  total=0
  for f in $(ls -d $directory); do
    lang=${f##*/}
    lang=${lang%.txt}
    if [[ "$lang" == "scala" ]]; then
        dotty=$(grep "dotty" $f | wc -l)
        scala=$(grep "scala" $f | wc -l)
        total=$(($total + $dotty + $scala))
        echo "$phase scala 2: $scala"
        echo "$phase scala 3: $dotty"
        echo "$phase scala: $(($scala + $dotty))"
    else
      res=$(wc -l $f | cut -d ' ' -f1)
      total=$(($total + $res))
      echo "$phase $lang: $res"
    fi
  done
  echo "$phase total: $total"
}

main ()
{
  print_results "Phase 1" "$BUGS/*.txt"
  print_results "Phase 2" "$BUGS/fixes/*.txt"
}

main
