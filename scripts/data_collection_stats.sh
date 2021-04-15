#!/bin/bash
# Print stats for Data collection
BUGS=$1

if [ "$#" -ne 1 ]; then
    echo "usage: phase_1_2.sh BUGS"
    exit
fi


main ()
{
  total_p1=0
  total_p2=0
  java_p1=$(wc -l $BUGS/java.txt | cut -d ' ' -f1)
  java_p2=$(wc -l $BUGS/fixes/java.txt | cut -d ' ' -f1)
  kotlin_p1=$(wc -l $BUGS/kotlin.txt | cut -d ' ' -f1)
  kotlin_p2=$(wc -l $BUGS/fixes/kotlin.txt | cut -d ' ' -f1)
  groovy_p1=$(wc -l $BUGS/groovy.txt | cut -d ' ' -f1)
  groovy_p2=$(wc -l $BUGS/fixes/groovy.txt | cut -d ' ' -f1)
  scala2_p1=$(grep "scala" $BUGS/scala.txt | wc -l)
  scala2_p2=$(grep "scala" $BUGS/fixes/scala.txt | wc -l)
  dotty_p1=$(grep "dotty" $BUGS/scala.txt | wc -l)
  dotty_p2=$(grep "dotty" $BUGS/fixes/scala.txt | wc -l)
  total_p1=$(($java_p1 + $kotlin_p1 + $groovy_p1 + $scala2_p1 + $dotty_p1))
  total_p2=$(($java_p2 + $kotlin_p2 + $groovy_p2 + $scala2_p2 + $dotty_p2))
  printf "%8s %15s %15s\n" "Language" "Phase 1" "Phase 2"
  echo "----------------------------------------"
  printf "%8s %15s %15s\n" "Java" "$java_p1" "$java_p2"
  printf "%8s %15s %15s\n" "Scala 2" "$scala2_p1" "$scala2_p2"
  printf "%8s %15s %15s\n" "Scala 3" "$dotty_p1" "$dotty_p2"
  printf "%8s %15s %15s\n" "Kotlin" "$kotlin_p1" "$kotlin_p2"
  printf "%8s %15s %15s\n" "Groovy" "$groovy_p1" "$groovy_p2"
  echo "----------------------------------------"
  printf "%8s %15s %15s\n" "Total" "$total_p1" "$total_p2"
}

main
