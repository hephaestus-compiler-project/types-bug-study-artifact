#!/bin/bash
# Find fixes and check if there is a test case in them
BUGS=$1
DESCRIPTIONS=$2
REPOS=$3
RESULTS=$4
GH_TOKEN=$5

if [ "$#" -ne 5 ]; then
    echo "usage: find_fixes.sh BUGS DESCRIPTIONS REPOS RESULTS GH_TOKEN"
    exit
fi

mkdir -p $RESULTS

echoerr() { printf "%s\n" "$*" >&2; }

get_issue ()
{
  local repo=$1
  local url=$2
  if [ "$repo" == "valhalla" ]; then
    local issue=${url##*-}
  else
    local issue=${url##*/}
  fi
  echo $issue
  return
}

get_owner ()
{
  local repo=$1
  if [[ "$repo" == *"groovy"* ]]; then
    echo apache
  elif [[ "$repo" == *"kotlin"* ]]; then
    echo JetBrains
  elif [[ "$repo" == *"dotty"* ]]; then
    echo lampepfl
  elif [[ "$repo" == *"scala"* ]]; then
    echo scala
  else # valhalla
    echo openjdk
  fi
  return
}

is_test ()
{
  local repo=$1
  local file=$2
  if [[ "$repo" == *"groovy"* ]]; then
    if [[ "$file" == *"test"* ]]; then
      return 0
    else
      return 1
    fi
  elif [[ "$repo" == *"kotlin"* ]]; then
    if [[ "$file" == *"test"* ]]; then
      return 0
    else
      return 1
    fi
  elif [[ "$repo" == *"dotty"* ]]; then
    if [[ "$file" == *"tests"* ]]; then
      return 0
    else
      return 1
    fi
  elif [[ "$repo" == *"scala"* ]]; then
    if [[ "$file" == *"test/files"* ]]; then
      return 0
    else
      return 1
    fi
  else # valhalla
    if [[ "$file" == *"test"* ]]; then
      return 0
    else
      return 1
    fi
  fi
  return
}

has_potential_test_in_desc ()
{
  local lang=$1
  local issue=$2
  local repo=$3
  local prev_pwd=$(pwd)
  local status=1
  if [[ "$lang" == *"groovy"* ]]; then
    cd $DESCRIPTIONS/$lang
    if cat $issue | grep -iqF "{code}"; then
      status=0
    fi
  elif [[ "$lang" == *"kotlin"* ]]; then
    cd $DESCRIPTIONS/$lang
    if cat $issue | grep -iqF "\`\`\`"; then
      status=0
    fi
  elif [[ "$lang" == *"scala"* ]]; then
    cd $DESCRIPTIONS/$lang
    if cat $repo-$issue | grep -iqF "\`\`\`scala"; then
      status=0
    fi
  elif [[ "$lang" == *"java"* ]]; then
    cd $DESCRIPTIONS/$lang
    if cat JDK-$issue | grep -iqF "{"; then
      status=0
    fi
  fi
  cd $prev_pwd
  return $status
}


get_diff_prs_from_comments ()
{
  local owner=$1
  local repo=$2
  local issue=$3

  brepo=$repo
  if [ "$repo" == "scala" ]; then
    brepo="bug"
  fi
  local diff_prs_c=""
  local request_url="https://api.github.com/repos/$owner/$brepo/issues/$issue/comments"
  local github_api_res=$(curl -H "Accept: application/vnd.github.v3+json" \
      -H "Authorization: token $GH_TOKEN" \
      $request_url 2> /dev/null)
  sleep 2
  while read -r comment ; do
    if echo $comment | grep '#' | grep -iqF fix; then
      pr=$(echo $comment | egrep -o "#[0-9]*")
      if [ ! -z "$pr" ] && [ "$pr" != "#" ]; then
        for p in $pr; do
          p=$(echo $p | tr -d "#")
          diff_prs_c="${diff_prs_c}https://github.com/$owner/$repo/pull/$p.diff "
        done
      fi
    elif echo $comment | grep 'pull' | grep -iqF fix; then
      pr=$(echo $comment | egrep -o "https://github.com/$owner/$repo/pull/[0-9]*")
      if [ ! -z "$pr" ]; then
        diff_prs_c="${diff_prs_c}$pr.diff "
      fi
    fi
  done <<< $(echo "$github_api_res" | jq '.[].body')
  echo $diff_prs_c
}

find_fixes ()
{
  local repo=$1
  local lang=$2
  local url=$3

  local owner=$(get_owner $repo)

  local issue=$(get_issue $repo $url)

  local log_prefix="log $repo:$issue"

  # echoerr "$log_prefix:START"

  # Get commits; if there isn't any commit, try to find pull requests.
  local old_pwd=$(pwd)
  cd $REPOS/$repo
  # We use --all because the fix may be in another branch
  # Because we look in all branches, commits may exist with same message but
  # different commit hash. In that case we want to keep only one.
  # Hence, we use awk and we compare many columns except the first one.
  local commits=$(git log --grep $issue --oneline --all 2> /dev/null | \
      awk '{print $1}')
  # Find PRs
  local prs=""
  request_url="https://api.github.com/search/issues?q=repo:$owner/$repo+type:pr+$issue in:body+$issue in:title"
  github_api_res=$(curl -H "Accept: application/vnd.github.v3+json" \
      -H "Authorization: token $GH_TOKEN" \
      $request_url 2> /dev/null)
  sleep 2
  diff_prs=$(echo $github_api_res | jq '.items[].pull_request.diff_url')


  # If both PRs and commits are empty and the lang is scala check in comments
  # for PRs.
  if [ "$lang" == "scala" ]; then
    diff_prs_comments=$(get_diff_prs_from_comments $owner $repo $issue)
    if [ -z "$diff_prs" ]; then
      diff_prs="${diff_prs_comments}"
    else
      diff_prs="${diff_prs} ${diff_prs_comments}"
    fi
  fi

  local files=""

  # For Java projects we should also check into the mercurial repo
  # type-annotations/langtools
  if [ "$lang" == "java" ] && [ -z "$commits" ]; then
    cd $old_pwd && cd $REPOS/type-annotations/langtools
    commits_tp=$(hg log --keyword $issue 2> /dev/null | grep changeset | cut -d ':' -f2 | \
        sed 's/^ *//;s/ *$//')
    if [ -z "$commits" ]; then
      commits=$commits_tp
    else
      commits="${commits} ${commits_tp}"
    fi
    for commit in $commits_tp; do
      files="${files}$(hg log -p -r $commit 2> /dev/null | diffstat -p 0 -l -N 1000)\n"
    done
  fi

  # Get files changed in commits and pull requests
  if [ ! -z "$commits" ]; then
    for commit in $commits; do
      files="${files}$(git diff $commit^! 2> /dev/null | diffstat -p 0 -l -N 1000)\n"
    done
  fi

  diff_prs_new=""
  if [ ! -z "$diff_prs" ]; then
    for diff_pr in $diff_prs; do
      diff_pr=$(echo $diff_pr | sed -e 's/^"//' -e 's/"$//')
      diff_pr_res=$(curl -L $diff_pr 2> /dev/null)
      sleep 2
      # There is a chance that the issue is not a PR but a simple issue
      if ! $(echo $diff_pr_res | grep "<!DOCTYPE html>" -iqF); then
        sleep 1
        # Unfortunately, echo $diff_pr_res | ... does not work
        files="${files}$(curl -L $diff_pr 2> /dev/null | diffstat -p 0 -l -N 1000)\n"
        diff_prs_new="${diff_prs_new}${diff_pr} "
      fi
    done
  fi
  cd $old_pwd

  # echoerr "$log_prefix:COMMITS: $commits"
  # echoerr "$log_prefix:PRs: $(echo $diff_prs_new | sed 's/.diff//g')"
  # echoerr "$log_prefix:FILES: $files"

  if [[ -z "$files" ]]; then
    echoerr "Warning: could not found fix for $url"
    echo ""
    return
  fi

  # Check if there is at least one file that isn't a test case.
  has_fix=0
  for file in $files; do
    break_loop=""
    if [[ "$file" == *"\n"* ]]; then
      for f in $(echo -e $file); do
        if ! $(is_test $repo $f); then
          has_fix=1
          break_loop="true"
          break
        fi
      done
    else
      if ! $(is_test $repo $file); then
        has_fix=1
        break
      fi
    fi
    if [ ! -z "$break_loop" ]; then
      break
    fi
  done

  if [[ "$has_fix" -eq "0" ]]; then
    echoerr "Warning: could not found fix for $url (only tests)"
    echo ""
    return
  fi

  # Check if there is at least one test case.
  has_test_case=0
  for file in $files; do
    if $(is_test $repo $file); then
      has_test_case=1
      break
    fi
  done

  # Check if there is a potential test case in the description of the issue
  if [[ "$has_test_case" -eq "0" ]]; then
    if $(has_potential_test_in_desc $lang $issue $repo); then
      has_test_case=1
    fi
  fi

  if [[ "$has_test_case" -eq "0" ]]; then
    echoerr "Warning: could not found test case for $url"
    res=""
  else
    prs=$(echo $diff_prs_new | sed 's/.diff//g')
    commits_urls=""
    commit_url="https://github.com/$owner/$repo/commit"
    for commit in $commits; do
      commits_urls="${commits_urls}${commit_url}/${commit} "
    done
    res="${commits_urls}${prs}"
  fi
  echo $res
  return
}

get_repo ()
{
  local url=$1
  if [[ "$url" == *"GROOVY"* ]]; then
    echo groovy
  elif [[ "$url" == *"KT"* ]]; then
    echo kotlin
  elif [[ "$url" == *"dotty"* ]]; then
    echo dotty
  elif [[ "$url" == *"scala"* ]]; then
    echo scala
  else # Java
    echo valhalla
  fi
  return
}

function process_file ()
{
  local file=$1
  local lang=$2
  res=""  # bug_url,fixes  where fixes are urls to commits or PRs
  echo "Process $file"
  for url in $(cat $file); do
    local repo=$(get_repo $url)
    local fixes=$(find_fixes $repo $lang $url)
    if [ ! -z "$fixes" ]; then
      res="${res}${url},${fixes}\n"
    fi
  done
  mkdir -p $RESULTS/
  echo -e "$res" > $RESULTS/$lang.txt
  return
}

main ()
{
  for f in $(ls -d $BUGS/*.txt); do
    lang=${f##*/}
    lang=${lang%.txt}
    process_file $f $lang
  done
}

main
