#! /bin/bash
DOWNLOADS=$1
GH_TOKEN=$2

if [ "$#" -ne 2 ]; then
    echo "usage: fetch.sh DOWNLOADS GH_TOKEN"
    exit
fi

# PHASE 1
echo "Fetching Groovy Bugs..."
python scripts/fetch/fetch_groovy_bugs.py $DOWNLOADS/bugs/groovy.txt \
        $DOWNLOADS/bugs/fixes/descriptions/groovy $DOWNLOADS/bugs/groovy.json
echo "Fetching Kotlin Bugs..."
python scripts/fetch/fetch_kotlin_bugs.py $DOWNLOADS/bugs/kotlin.txt \
        $DOWNLOADS/bugs/fixes/descriptions/kotlin $DOWNLOADS/bugs/kotlin.json
echo "Fetching Java Bugs..."
python scripts/fetch/fetch_java_bugs.py $DOWNLOADS/bugs/java.txt \
        $DOWNLOADS/bugs/fixes/descriptions/java $DOWNLOADS/bugs/java.json
echo "Fetching Scala Bugs..."
python scripts/fetch/fetch_scala_bugs.py $DOWNLOADS/bugs/scala.txt \
        $DOWNLOADS/bugs/fixes/descriptions/scala $DOWNLOADS/bugs/scala.json $GH_TOKEN
echo "Cloning Compilers' Repositories..."
./scripts/fetch/clone.sh $DOWNLOADS/repos
# PHASE 2
echo "Finding Test Cases & Fixes (Post-Filtering)..."
echo "This requires some time. Please bear with us ..."
./scripts/fetch/find_fixes.sh $DOWNLOADS/bugs \
        $DOWNLOADS/bugs/fixes/descriptions $DOWNLOADS/repos \
        $DOWNLOADS/bugs/fixes $GH_TOKEN 2>&1 | tee $DOWNLOADS/logs
