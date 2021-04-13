#!/bin/bash
ITERATIONS=$1
REPOS=$2
RESULTS=$3
TEMPFILE=$(mktemp)
trap "rm -f $TEMPFILE" 0 2 3 15

if [ "$#" -ne 3 ]; then
    echo "usage: get_fixes.sh ITERATIONS REPOS RESULTS"
    exit
fi

mkdir -p $RESULTS

echoerr() { printf "%s\n" "$*" >&2; }

get_repo ()
{
  local fix=$1
  if [[ "$fix" == *"groovy"* ]]; then
    echo groovy
  elif [[ "$fix" == *"kotlin"* ]]; then
    echo kotlin
  elif [[ "$fix" == *"dotty"* ]]; then
    echo dotty
  elif [[ "$fix" == *"scala"* ]]; then
    echo scala
  elif [[ "$fix" == *"github"* ]]; then
    echo valhalla # Java
  elif [[ "$fix" == *"jdk/jdk"* ]]; then
    echo jdk
  elif [[ "$fix" == *"jdk7/jdk7"* ]]; then
    echo jdk7/langtools
  elif [[ "$fix" == *"jdk7u/jdk7u"* ]]; then
    echo jdk7u/langtools
  elif [[ "$fix" == *"jdk8/jdk8"* ]]; then
    echo jdk8/langtools
  elif [[ "$fix" == *"jdk8u/jdk8u"* ]]; then
    echo jdk8u/langtools
  elif [[ "$fix" == *"jdk9/jdk9"* ]]; then
    echo jdk9/langtools
  elif [[ "$fix" == *"jdk10/master"* ]]; then
    echo jdk10
  elif [[ "$fix" == *"jdk/jdk13"* ]]; then
    echo jdk13
  elif [[ "$fix" == *"jdk/jdk14"* ]]; then
    echo jdk14
  fi
}

get_commit_diff()
{
  local repo=$1
  local commit=$2
  local old_pwd=$(pwd)
  cd $REPOS/$repo
  if ! git diff $commit^! > $TEMPFILE 2> /dev/null; then
    echo "Warning: could not found commit $commit in $repo"
  fi
  cd $old_pwd
}

get_pr_diff()
{
  local fix=$1
  if ! curl -L $fix.diff > $TEMPFILE 2> /dev/null; then
    echo "Warning: could not download pr $fix"
  fi
  sleep 2
}

get_rev_diff()
{
  local repo=$1
  local rev=$2
  local old_pwd=$(pwd)
  cd $REPOS/$repo
  if ! hg log -p -r $rev > $TEMPFILE 2> /dev/null; then
    echo "Warning: could not found commit $rev in $repo"
  fi
  cd $old_pwd
}

process_file ()
{
  local file=$1
  local lang=$2
  echo "Process $file"
  for l in $(cat $file); do
    bug=$(echo $l | awk -F"," '{print $1}')
    bug=${bug##*/}
    fix=$(echo $l | awk -F"," '{print $2}')
    repo=$(get_repo $fix)
    diff_name=""
    if [[ "$fix" == *"commit"* ]]; then
      commit=${fix##*/}
      get_commit_diff $repo $commit
      diff_name="commit-$commit.diff"
    elif [[ "$fix" == *"pull"* ]]; then
      pr=${fix##*/}
      get_pr_diff $fix
      diff_name="pr-$pr.diff"
    elif [[ "$fix" == *"rev"* ]]; then
      rev=${fix##*/}
      get_rev_diff $repo $rev
      diff_name="rev-$rev.diff"
    else
      echo "Warning could not found fix for $bug"
      continue
    fi
    if [ "$lang" == "scala" ]; then
      if [ "$repo" == "dotty" ]; then
        bug="dotty-${bug}"
        diff_name="dotty-${diff_name}"
      else
        bug="scala-${bug}"
        diff_name="scala-${diff_name}"
      fi
    fi
    mkdir -p $RESULTS/$lang/$bug
    if [ ! -z "$diff_name" ]; then
      cat $TEMPFILE > $RESULTS/$lang/$bug/$diff_name
    fi
  done
}

main ()
{
  for iter in $(ls -d $ITERATIONS/*); do
    for f in $(ls $iter); do
      lang=${f##*/}
      lang=${lang%.txt}
      process_file $iter/$f $lang
    done
  done
}

main
