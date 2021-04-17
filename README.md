# Artifact for "Well-Typed Programs Can Go Wrong: A Study of Typing-Related Bugs in JVM Compilers"

This is the artifact for the paper titled
"Well-Typed Programs Can Go Wrong:
A Study of Typing-Related Bugs in JVM Compilers".

An archived version of the artifact will also be published on Zenodo,
upon this paper's publication.

# Overview

The artifact contains the dataset and scripts to reproduce the results
described in our paper.
The artifact has the following structure:

* `scripts`: This is the directory that contains the scripts needed to
reproduce the results, the figures, and the tables presented in our paper.
* `scripts/fetch`: This is the directory that contains the scripts needed to
download the initial dataset described in our paper
(_bug collection_ and _post-filtering_).
* `categorization`: Python code used to categorize the analyzed bugs.
For more information see `categorization/README.md`.
* `data`: This is dataset of 320 the typing-related bugs under study.
* `data/bugs.json`: This document contains all 320 bugs examined in our study
                    and their categorization. Each bug entry has the following fields:
    * `language`: The language of the compiler.
    * `compiler`: The compiler in which the bug occurred.
    * `is_correct`: `True` if the bug-revealing test case is compilable;
       `False` otherwise.
    * `symptom`: The bug's symptom.
    * `bug_cause`: The root cause of the bug.
    * `error`: This field indicates how the bug was introduced.
    * `chars`: This is an array containing the characteristics of the bug-revealing test case.
* `data/characteristics.json`: This document contains the categories
   and the sub-categories of the bug-revealing test cases.
* `data/{groovy,java,kotlin,scala}.json`: General statistics regarding
   the creation and resolution date, the assignee,
   and the number of comments associated with each bug.
* `data/diffs/{groovy,java,kotlin,scala}/bug_id/*.diff`: The revisions associated with 
   the fix of bug `bug_id`.
* `data/diffs/{groovy,java,kotlin,scala}/bug_id/stats.csv`: Lines of code affected
   by the fix of bug `bug_id`.
* `data/test_cases/{groovy,java,kotlin,scala}/bug_id/*.{kt,java,scala,groovy}`:
The test case of the fix of bug `bug_id`.
* `data/test_cases/{groovy,java,kotlin,scala}/bug_id/stats.json`:
Statistics on the bug-revealing test case (number of declarations,
method/function calls, LoCs) associated with the bug `bug_id`.
* `data/iterations/1/{groovy,java,kotlin,scala}.txt`: Bugs analyzed in each
iteration. Each line contains two entries (comma separated):
(1) the URL pointing to the bug report,
and (2) the URL pointing to the fix of the bug.
* `data/collection`: The entire dataset produced by the _post-filtering_ step
  (4.153 bugs) of our bug collection approach.

# Requirements

* A Unix-like operating system (tested on Ubuntu and Debian).

* An installation of Python3

* An installation of Docker

* At least 20GB of available disk space

# Getting Started

## Setup

There are two options for reproducing the results of the paper.
If you run an Ubuntu/Debian OS,
we provide the instructions for installing the necessary
`apt` packages and libraries
used for running the scripts of the artifact.
Otherwise if you do not have an Ubuntu/Debian installation,
this artifact provides you with a Docker image
that contains the required setup
for executing the scripts and reproducing the results of our paper.

#### Option1: Ubuntu/Debian Installation

**NOTE**: If you do not run an Ubuntu/Debian OS, please jump to the
Section "Option2: Docker Image Installation".

You need to install some `apt` packages and some Python packages to run the
experiments of this artifact.
First, download the following packages using `apt`.

```bash
apt install curl jq git mercurial diffstat cloc
```

You also need to install some Python packages.
In a Python virtualenv run the following:

```bash
virtualenv .env
source .env/bin/activate
pip install requests matplotlib pandas seaborn
```

#### Option2: Docker Image Installation

To build the Docker image from source,
run the following command (estimated running time: ~3 min)

```bash
docker build . -t bug-study
```

Run the following command to create a new container.

```bash
docker run -it \
    -v $(pwd)/scripts:/home/scripts \
    -v $(pwd)/downloads:/home/downloads \
    -v $(pwd)/data:/home/data \
    -v $(pwd)/figures:/home/figures \
    bug-study /bin/bash
```

After executing the command, you will be able to enter the home directory
(i.e., `/home`). This directory contains
(1) the scripts for reproducing the results of the paper (see `scripts/`),
(2) the data of our bug study (see `data/`),
(3) a dedicated directory for storing the generated figures (see `figures/`),
and (4) `downloads/` which is the directory where the data
produced by the _bug collection_ and _post-filtering_ phases
will be saved (in case you decide to re-create the bug dataset).

**Some further explanations**:
The option `-v` is used to mount a local volume inside the Docker container.
In this way, data produced during the execution of the container
will not be lost upon container's exit
(e.g., the resulting figures will be stored in `$(pwd)/figures`).

## Download the bugs and fixes from sources

**NOTE 1:**
If you do not want to re-download the bugs from the sources
and re-create the bug dataset,
you can go directly to the next section ("Step-by-Step Instructions").

To download and re-construct the initial dataset described in
Section 2.1 of the paper, then you will need at least 20 GB of available disk
space. At this point, we should note that the generated dataset will probably
contain more bugs than the dataset described in the paper because new bugs
will have been fixed from the time we downloaded the bugs until now.

**NOTE 2:**
To run the following scripts successfully,
you need to obtain a Github access token
(see [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)) so that
you are able to interact with the Github API.
Once you obtain it,
please assign it to a shell variable named `GH_TOKEN`.

```bash
export GH_TOKEN=<your Github access token>
```


The following script applies our bug collection approach.
Specifically,
it searches over the issue trackers of the examined compilers
and retrieves fixed typing-related bugs that meet our search criteria
as described in Section 2.1 of our paper.
Then,
it runs the _post-filtering_ step to filter out bugs
without any explicit fix or a test case.
To fetch the data,
run the following script (estimated running time: ~18 hours)


```bash
./scripts/fetch/fetch.sh downloads $GH_TOKEN
```

The command above executes six scripts.
The first five scripts compose the _bug collection_ phase of our approach,
while the 6th script stands for the _post-filtering_ step.
In the following,
the shell variable `$DOWNLOADS` corresponds to the `downloads/` directory,
which is passed as an argument in the first command
(`scripts/fetch/fetch.sh`).


### 1. Fetch Groovy bugs

```bash
python scripts/fetch/fetch_groovy_bugs.py $DOWNLOADS/bugs/groovy.txt \
        $DOWNLOADS/bugs/fixes/descriptions/groovy $DOWNLOADS/bugs/groovy.json
```

This script fetches `groovyc` bugs
using the Jira REST API
(see <https://issues.apache.org/jira/rest/api>).
It saves (1) the URLs of the retrieved bugs
in `$DOWNLOADS/bugs/groovy.txt`,
(2) the description and the summary of each
bug in
`$DOWNLOADS/bugs/fixes/descriptions/groovy/GROOVY-XXXX`
(where `XXXX` stands for the id of the bug),
and (3) some general statistics,
(such as `created` date, `resolution` date, and `reporter`)
in `$DOWNLOADS/bugs/groovy.json`.

### 2. Fetch Kotlin bugs

```bash
python scripts/fetch/fetch_kotlin_bugs.py $DOWNLOADS/bugs/kotlin.txt \
        $DOWNLOADS/bugs/fixes/descriptions/kotlin $DOWNLOADS/bugs/kotlin.json
```

This script fetches `kotlinc` bugs
using the YouTrack REST API
(see <https://youtrack.jetbrains.com/api/issues>).
The script stores
(1) the URLs of the retrieved `kotlinc` bugs
in `$DOWNLOADS/bugs/kotlin.txt`,
(2) the description and the summary for each
bug in
`$DOWNLOADS/bugs/fixes/descriptions/kotlin/KT-XXXX`,
and (3) some general statistics
(such as `created` date, `resolution` date, and `reporter`)
in `$DOWNLOADS/bugs/kotlin.json`.

### 3. Fetch Java bugs

```bash
python scripts/fetch/fetch_java_bugs.py $DOWNLOADS/bugs/java.txt \
        $DOWNLOADS/bugs/fixes/descriptions/java $DOWNLOADS/bugs/java.json
```

This script fetches `javac` bugs
using the Jira REST API
(see <https://bugs.openjdk.java.net/rest/api>),
The script saves
(1) the URLs of the retrieved bugs
in `$DOWNLOADS/bugs/java.txt`,
(2) the description and the summary for each bug in
`$DOWNLOADS/bugs/fixes/descriptions/java/JDK-XXXX`,
(3) some general statistics
(such as `created` date, `resolution` date, and `reporter`)
in `$DOWNLOADS/bugs/java.json`.

### 4. Fetch Scala bugs

```bash
python scripts/fetch/fetch_scala_bugs.py $DOWNLOADS/bugs/scala.txt \
        $DOWNLOADS/bugs/fixes/descriptions/scala $DOWNLOADS/bugs/scala.json $GH_TOKEN
```

This script fetches bugs related to `scalac` and `dotty`
using the Github REST API
(see <https://api.github.com>).
The script saves
(1) the URLs of the scripts
in `$DOWNLOADS/bugs/scala.txt`,
(2) the description and the summary for each bug in
`$DOWNLOADS/bugs/fixes/descriptions/scala/scala-XXXX`,
and (3) some general
statistics
(such as `created` date, `resolution` date, and `reporter`)
in `$DOWNLOADS/bugs/scala.json`.

### 5. Clone compilers' repositories

```bash
./scripts/fetch/clone.sh $DOWNLOADS/repos
```

This script clones a number of repositories.
We use the history of these repositories to search for fixes
corresponding to the collected bugs.
In particular,
the script clones the following repositories.

```
https://github.com/JetBrains/kotlin
https://github.com/apache/groovy
https://github.com/lampepfl/dotty
https://github.com/scala/scala
https://github.com/openjdk/valhalla
http://hg.openjdk.java.net/type-annotations/type-annotations/
http://hg.openjdk.java.net/jdk/jdk/
http://hg.openjdk.java.net/jdk7/jdk7/
http://hg.openjdk.java.net/jdk7u/jdk7u/
http://hg.openjdk.java.net/jdk8/jdk8/
http://hg.openjdk.java.net/jdk8u/jdk8u/
http://hg.openjdk.java.net/jdk9/jdk9/
http://hg.openjdk.java.net/jdk10/master/
http://hg.openjdk.java.net/jdk/jdk13/
http://hg.openjdk.java.net/jdk/jdk14/
```

### 6. Detect bug fixes

```
./scripts/fetch/find_fixes.sh $DOWNLOADS/bugs \
        $DOWNLOADS/bugs/fixes/descriptions $DOWNLOADS/repos \
        $DOWNLOADS/bugs/fixes $GH_TOKEN 2>&1 | tee $DOWNLOADS/logs
```

This script is responsible for detecting fixes
associated with the bugs fetched by
the previous scripts.
To do so,
for each bug,
it first searches over
the corresponding repository for commits containing
the ID of the bug in commit's message.
If that fails and the repository is hosted in GitHub,
then the script searches for
pull requests that have tagged the given bug ID.
Finally,
the scripts produces
`$DOWNLOADS/bugs/fixes/{groovy,kotlin,java,scala}.txt`,
which contains the URL of each bug report and fix.


Finally,
to print some general statistics regarding
our bug collection approach run

```bash
./scripts/data_collection_stats.sh downloads/bugs
```

The above script prints the total number of bugs collected
in the previous step.
It produces an output similar to the following.

```
Language         Phase 1         Phase 2
----------------------------------------
    Java            1252             873
 Scala 2            1180            1067
 Scala 3             429             366
  Kotlin            2189            1601
  Groovy             300             246
----------------------------------------
   Total            5350            4153
```

## Download the 320 typing-related bugs

To download the data associated with
the 320 typing-related that
were manually examined in our paper,
run the following script (estimated running time: 4--5 min)

```bash
./scripts/fetch/get_data_for_selected_bugs.sh downloads data
```

Finally, we need to get the fixes and the statistics for the selected bugs
of our dataset. This script takes as input the `downloads` directory, which
includes the initial dataset, and the `data` directory, which must contain
an `iterations` directory with the selected bugs. Specifically, in this
directory, files contain bugs associated with their fixes.
For example, you can look at `data/iterations/1/java.txt`. The script
downloads fixes' diffs, and computes statistics for these fixes in
`data/diffs/{groovy,java,kotlin,scala}/bug_id`. Each generated directory
contains a `.diff` and a `stats.csv` file. More specifically, the following
scripts will be executed.

1. Get fixes of the bugs.

```bash
./scripts/fetch/get_fixes.sh $DATA/iterations $DOWNLOADS/repos $DATA/diffs
```

This script finds the bugs' fixes in `$DATA/iterations` from the corresponding
compiler's repository or its pull request from GitHub.
Finally, it saves the diffs in `$DATA/diffs`.

2. Compute statistics of diffs.

```bash
./scripts/fetch/get_diff_stats.sh $DATA/diffs
```

Using `diffstat` this script computes the stats of the diffs.

3. Copy general statistics.

```bash
python scripts/fetch/copy_stats.py $DATA/iterations/ $DOWNLOADS/bugs/ $DATA/
```

For the bugs in `$DATA/iterations/` this script copies their statistics from
the files `$DOWNLOADS/bugs/{groovy,kotlin,java,scala}.json`
into `$DATA/{groovy,kotlin,java,scala}.json`.

4. Compute LoCs of test cases.

```bash
./scripts/fetch/add_locs.sh $DATA/test_cases
```

Using `cloc`, this script computes the stats of the test cases.

# Step by Step Instructions

In the following section, we provide scripts that reproduce the results
presented in the paper using the dataset from `data` directory.

## Collecting Bugs & Fixes (Section 2.1)

Run the following script to print the results of the bug collection phases.
Specifically, it will print the data of Table 1.

```bash
./scripts/data_collection_stats.sh data/collection
```

In `data/collection` directory is the data of the bugs that compose our
initial dataset. The above script prints the following.

```
Language         Phase 1         Phase 2
----------------------------------------
    Java            1252             873
 Scala 2            1180            1067
 Scala 3             429             366
  Kotlin            2189            1601
  Groovy             300             246
----------------------------------------
   Total            5350            4153
```


## RQ1: Symptoms (Section 3.1)

For the first research question, we will use a script reproduce Fig 1 that
shows the distribution of symptom categories. To do so, run:

```bash
python scripts/rq1.py data/bugs.json --output figures/symptoms.pdf
```

This produces `symptoms.pdf` in the `figures` directory.
It also prints a table in standard output that presents the total values
and the percentages of symptoms per compiler. Specifically, it will print
the following.

```
Symptom                               groovyc          javac        kotlinc scalac & Dotty          Total
---------------------------------------------------------------------------------------------------------
Unexpected Compile-Time Error     59 (73.75%)    38 (47.50%)    30 (37.50%)    36 (45.00%)   163 (50.94%)
Internal Compiler Error           10 (12.50%)    25 (31.25%)    18 (22.50%)    26 (32.50%)    79 (24.69%)
Unexpected Runtime Behavior        9 (11.25%)    11 (13.75%)    22 (27.50%)    11 (13.75%)    53 (16.56%)
Misleading Report                   2 (2.50%)      4 (5.00%)      7 (8.75%)      5 (6.25%)     18 (5.62%)
Compilation Performance Issue       0 (0.00%)      2 (2.50%)      3 (3.75%)      2 (2.50%)      7 (2.19%)
```

## RQ2: Bug Patterns (Section 3.2)

For the second research question, first we will reproduce Figures 7a and 7b.
These figures demonstrates the distribution of bug patterns with regards to
the compiler and the symptoms. Second, we will produce two tables, one for
each figure that display the total values and the percentages of the patterns.

```bash
python scripts/rq2.py data/bugs.json --patterns figures/patterns.pdf \
    --patterns-symptoms figures/patterns_symptoms.pdf
```

The above command produce the figures `figures/patterns.pdf` and
`figures/patterns_symptoms.pdf`, and it prints the following in the
standard output.

```
Bug Cause                                    groovyc              javac            kotlinc     scalac & Dotty              Total
--------------------------------------------------------------------------------------------------------------------------------
Type-related Bugs                        37 (46.25%)        34 (42.50%)        31 (38.75%)        27 (33.75%)       129 (40.31%)
Semantic Analysis Bugs                   17 (21.25%)        16 (20.00%)        20 (25.00%)        24 (30.00%)        77 (24.06%)
Resolution Bugs                          24 (30.00%)        17 (21.25%)        22 (27.50%)        14 (17.50%)        77 (24.06%)
Error Handling & Reporting                 1 (1.25%)        10 (12.50%)          5 (6.25%)          6 (7.50%)         22 (6.88%)
AST Transformation Bugs                    1 (1.25%)          3 (3.75%)          2 (2.50%)         9 (11.25%)         15 (4.69%)

Bug Cause                              Unexpected        Internal      Unexpected      Misleading     Compilation           Total
---------------------------------------------------------------------------------------------------------------------------------
Type-related Bugs                     90 (28.12%)      23 (7.19%)      10 (3.12%)       3 (0.94%)       3 (0.94%)    129 (40.31%)
Semantic Analysis Bugs                 24 (7.50%)      21 (6.56%)      27 (8.44%)       3 (0.94%)       2 (0.62%)     77 (24.06%)
Resolution Bugs                       44 (13.75%)      11 (3.44%)      16 (5.00%)       5 (1.56%)       1 (0.31%)     77 (24.06%)
Error Handling & Reporting              0 (0.00%)      15 (4.69%)       0 (0.00%)       7 (2.19%)       0 (0.00%)      22 (6.88%)
AST Transformation Bugs                 5 (1.56%)       9 (2.81%)       0 (0.00%)       0 (0.00%)       1 (0.31%)      15 (4.69%)
```


## RQ3: Bug Fixes (Section 3.3)

In the third research question, we study the duration and the fixes of the bugs.
Hence, we will produce Fig 13a, Fig 13b, and Fig 14. We will also print in
the standard output the mean, median, standard deviation, max, and min per
language for files number, lines number, and duration of the fixes.


```bash
python scripts/rq3.py data/diffs/ data/ --directory figures
```

The previous command saves Fig 13a in `figures/lines.pdf`, Fig 13b in
`figures/files.pdf`, and Fig 14 in `figures/duration.pdf`.
Note that you can use `--all` option to plot lines for all languages in
the figures `lines.pdf` and `files.pdf`.
The script also prints the following tables.

```
                         Lines
============================================================
          Mean      Median    SD        Min       Max
------------------------------------------------------------
Java      30.95     16.00     40.60     1.00      190.00
Kotlin    56.15     21.50     144.21    1.00      1177.00
Groovy    49.10     23.00     89.20     1.00      706.00
Scala     73.40     9.50      379.35    1.00      3381.00
------------------------------------------------------------
Total     52.40     16.00     208.33    1.00      3381.00

                         Files
============================================================
          Mean      Median    SD        Min       Max
------------------------------------------------------------
Java      1.60      1.00      1.03      1.00      5.00
Kotlin    2.70      2.00      2.56      1.00      15.00
Groovy    1.49      1.00      0.86      1.00      5.00
Scala     2.46      1.00      5.22      1.00      45.00
------------------------------------------------------------
Total     2.06      1.00      3.01      1.00      45.00

                      Duration
============================================================
          Mean      Median    SD        Min       Max
------------------------------------------------------------
Java      131.39    21.00     284.86    0.00      1621.00
Kotlin    164.16    34.00     296.25    0.00      1337.00
Groovy    122.05    8.00      278.64    0.00      1472.00
Scala     328.09    55.50     628.74    0.00      3209.00
------------------------------------------------------------
Total     186.42    24.00     407.32    0.00      3209.00
```

## RQ4: Test Case Characteristics (Section 3.4)


For this research question, we will use two scripts.
The first script, will generate Figure 15 and it will print Tables 2, 3, and 4
in the standard output. Whereas the second script will print the lift scores
reported in Section 3.4.2.

```bash
python scripts/rq4.py data/characteristics.json data/bugs.json data/test_cases/ \
    --output figures/characteristics.pdf
```

This script generates `figures/characteristics.pdf` and produces:

```
General statistics on test case characteristics
===============================================================
Compilable test cases                        216 / 320 (67.50%)
Non-compilable test cases                    104 / 320 (32.50%)
---------------------------------------------------------------
LoC (mean)                                                10.24
LoC (median)                                                  8
---------------------------------------------------------------
Number of class decls (mean)                               1.98
Number of class decls (median)                                2
---------------------------------------------------------------
Number of method decls (mean)                              2.89
Number of method decls (median)                               2
Number of method calls (mean)                              2.48
Number of method calls (median)                               1
---------------------------------------------------------------

Most frequent features
===============================================================
Parameterized type                                       46.56%
Type argument inference                                  31.87%
Parameterized class                                      30.00%
Parameterized function                                   26.25%
Inheritance                                              24.06%

Least frequent features
===============================================================
Multiple implements                                       2.19%
This                                                      2.19%
Arithmetic Expressions                                    1.88%
Loops                                                     1.25%
Sealed Classes                                            0.94%

Most bug-triggering features per language
===========================================================================================================================================================
                 Java                                 Groovy                                Kotlin                                Scala
-----------------------------------------------------------------------------------------------------------------------------------------------------------
Parameterized type            51.25% | Parameterized type            41.25% | Parameterized type            36.25% | Parameterized type            57.50% |
Type argument inference       42.50% | Collection API                35.00% | Parameterized class           33.75% | Parameterized class           42.50% |
Functional interface          37.50% | Type argument inference       35.00% | Type argument inference       32.50% | Inheritance                   32.50% |
Parameterized function        35.00% | Lambda                        25.00% | Parameterized function        26.25% | Implicits                     23.75% |
Parameterized class           30.00% | Parameterized function        21.25% | Inheritance                   25.00% | Parameterized function        22.50% |

Most frequent characteristic categories
========================================
Parametric polymorphism           57.19%
OOP features                      53.75%
Type inference                    43.44%
Type system features              36.25%
Functional programming            31.56%
Standard library                  30.63%
Standard features                 28.75%
Other                             28.75%
```

As already mentioned, the following script reports the lift scores that we
refer in the paper.

```bash
python scripts/lift.py data/bugs.json data/ data/diffs/
```

It produces:

```
Char Categories -> Char Categories
Lift        Standard library -> Functional programming : 5.3639 (Confidence A->B: 0.5306, Support B: 0.0989) -- Totals A: 98, B: 101, A-B: 52
Lift        Standard library -> Type inference         : 5.1717 (Confidence A->B: 0.7041, Support B: 0.1361) -- Totals A: 98, B: 139, A-B: 69
Characteristics -> Characteristics
Lift            Variable arguments -> Overloading                  : 24.0282 (Confidence A->B: 0.4545, Support B: 0.0189) -- Totals A: 11, B: 29, A-B: 5
Lift             Use-site variance -> Parameterized function       : 17.1765 (Confidence A->B: 0.9412, Support B: 0.0548) -- Totals A: 17, B: 84, A-B: 16
Lift       Type argument inference -> Parameterized function       : 12.7034 (Confidence A->B: 0.6961, Support B: 0.0548) -- Totals A: 102, B: 84, A-B: 71
Lift                     Implicits -> Parameterized class          : 10.9260 (Confidence A->B: 0.6842, Support B: 0.0626) -- Totals A: 19, B: 96, A-B: 13
Lift       Type argument inference -> Collection API               : 8.5882 (Confidence A->B: 0.3922, Support B: 0.0457) -- Totals A: 102, B: 70, A-B: 40
Lift       Type argument inference -> Parameterized type           : 6.9599 (Confidence A->B: 0.6765, Support B: 0.0972) -- Totals A: 102, B: 149, A-B: 69
```

Note that this script can be used to compute various lift scores.
To print all available lift scores use the option `--all`.
Furthermore, you can set the number of pairs to print with `--limit` option,
a threshold with `--threshold` option, and a population threshold with
`--ithreshold`.

```
usage: lift.py [-h] [--threshold THRESHOLD] [--ithreshold ITHRESHOLD]
               [--limit LIMIT] [--all] bugs stats diffs

Lift correlations

positional arguments:
  bugs                  File with the bugs
  stats                 Directory that contains the stats for the bugs.
  diffs                 Directory that contains the diffs of the bug fixes.

optional arguments:
  -h, --help            show this help message and exit
  --threshold THRESHOLD
                        Threshold for lift.
  --ithreshold ITHRESHOLD
                        Intersections threshold for lift.
  --limit LIMIT         Max entries to show per pair.
  --all                 Print lift score for all categories
```
