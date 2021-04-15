# Artifact for Well-Typed Programs Can Go Wrong: A Study of Typing-Related Bugs in JVM Compilers

This is the artifact for the paper titled
"Well-Typed Programs Can Go Wrong:
A Study of Typing-Related Bugs in JVM Compilers".

An archived version of the artifact will also be published on Zenodo,
upon this paper's publication.

Overview
--------

The artifact contains the dataset and scripts to re-compute the results
described in our paper. The artifact has the following structure:

* `scripts`: This is the directory that contains the scripts needed to
re-compute the results presented in our paper.
* `scripts/fetch`: This is the directory that contains the scripts needed to
download the initial dataset described in our paper (Phase 1 and Phase 2).
* `categorization`: A python DSL language to categorize the analyzed bugs.
For more information see `categorization/README.md`.
* `data`: The dataset of the analyzed 320 bugs.
* `data/bugs.json`: Contains all 320 bugs of our study. Each bug has the
following fields:
    * `language`: The language of the compiler.
    * `compiler`: The compiler in which the bug occurred.
    * `is_correct`: `True` if the test case is compilable. In case the test is
non-compilable, the value of this field is `False`.
    * `symptom`: The effect of this bug.
    * `pattern`: The category of this bug.
    * `root_cause`: The cause that introduced this bug.
    * `chars`: The characteristics of the test case that trigger the bug.
* `data/characteristics.json`: The categories and the sub-categories of
the characteristics that trigger the bugs in our dataset.
* `data/{groovy,java,kotlin,scala}.json`: Data about the timestamp,
the reporter, the assignee, and the number of comments for each bug.
* `data/diffs/{groovy,java,kotlin,scala}/bug_id/*.diff`: The diff of the fix.
* `data/diffs/{groovy,java,kotlin,scala}/bug_id/stats.csv`: The LoC of the fix.
* `data/test_cases/{groovy,java,kotlin,scala}/bug_id/*.{kt,java,scala,groovy}`:
The test case of the fix.
* `data/test_cases/{groovy,java,kotlin,scala}/bug_id/stats.json`:
Statistics for the fix (number of declarations, method/function calls, LoCs).
* `data/iterations/1/{groovy,java,kotlin,scala}.txt`: Bugs analyzed in each
iteration, each line contains the URL for the bug report and the URL for the
fix of the bugs, separated by a comma.
* `data/collection`: Phase 2 dataset (4.153 bugs).

Requirements
------------

* A Unix-like operating system (tested on Ubuntu and Debian) with python3,
or a Docker installation.


#### Ubuntu/Debian

You need to install some apt packages and some python packages to run the
experiments of this artifact.
First, download the following packages using apt.

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

#### Docker

First, build the docker image.

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
(i.e., /home). This directory contains the `scripts` where the scripts that
we are going to execute are stored, `data` where the data of the bug study are
stored, `figures` which is the directory where we are going to save the produced
figures, and `downloads` which is the directory where the data of Phase 1 and
Phase 2 will be saved if you decide to get the initial data from their sources.

Some further explanations:

The option `-v` is used to mount a local volume inside the Docker container.
This option is used to get data from this repository to the Docker container,
and to store all the figures produced from the scripts in `$(pwd)/figures`.

Download the bugs and fixes from sources
----------------------------------------

If you select to download and regenerate the initial dataset described in
Section 2.1 of the paper, then you will need at least 20 GB of available disk
space. At this point, we should note that the generated dataset will probably
contain more bugs than the dataset described in the paper because new bugs
will have been fixed from the time we downloaded the bugs until now.

* Download the data (~18 hours).

```bash
./scripts/fetch/fetch.sh downloads $GH_TOKEN
```

This command will execute several scripts in order to download all the data.
The `downloads` directory is the directory in which the data will be saved.
Moreover, you will need to save in a local variable called `GH_TOKEN`, a
GitHub API token. This command takes that much time because (1) we need to
download a number of large code repositories (compilers' codebases), and (2)
we need to wait between some requests due to the rate limits of the GitHub API.
More specifically, the following scripts will be executed. Note that in place
of `$DOWNLOADS` is the `downloads` directory. The first five scripts compose
Phase 1 of our collection process, while the 6th script is Phase 2 of our
process.

1. Fetch Groovy bugs.

```bash
python scripts/fetch/fetch_groovy_bugs.py $DOWNLOADS/bugs/groovy.txt \
        $DOWNLOADS/bugs/fixes/descriptions/groovy $DOWNLOADS/bugs/groovy.json
```

This script fetches `groovyc` bugs from
<https://issues.apache.org/jira/rest/api>, then it saves the URLs of the scripts
in `$DOWNLOADS/bugs/groovy.txt`, the description and the summary for each
bug (with id: GROOVY-XXXX) in
`$DOWNLOADS/bugs/fixes/descriptions/groovy/GROOVY-XXXX`, and it saves
statistics such as `created` timestamp, `resolution` timestamp, and `reporter`
in `$DOWNLOADS/bugs/groovy.json`.

2. Fetch Kotlin bugs.

```bash
python scripts/fetch/fetch_kotlin_bugs.py $DOWNLOADS/bugs/kotlin.txt \
        $DOWNLOADS/bugs/fixes/descriptions/kotlin $DOWNLOADS/bugs/kotlin.json
```

This script fetches bugs for the Kotlin compiler from
<https://youtrack.jetbrains.com/api/issues>, it saves the URLs of the scripts
in `$DOWNLOADS/bugs/kotlin.txt`, the description and the summary for each
bug (with id: KT-XXXX) in
`$DOWNLOADS/bugs/fixes/descriptions/kotlin/KT-XXXX`, and it saves
statistics such as `created` timestamp, `resolution` timestamp, and `reporter`
in `$DOWNLOADS/bugs/kotlin.json`.

3. Fetch Java bugs.

```bash
python scripts/fetch/fetch_java_bugs.py $DOWNLOADS/bugs/java.txt \
        $DOWNLOADS/bugs/fixes/descriptions/java $DOWNLOADS/bugs/java.json
```

This script fetches bugs for `javac` from
<https://bugs.openjdk.java.net/rest/api>, it saves the URLs of the scripts
in `$DOWNLOADS/bugs/java.txt`, the description and the summary for each
bug (with id: JDK-XXXX) in
`$DOWNLOADS/bugs/fixes/descriptions/java/JDK-XXXX`, and it saves
statistics such as `created` timestamp, `resolution` timestamp, and `reporter`
in `$DOWNLOADS/bugs/java.json`.

4. Fetch Scala bugs.

```bash
python scripts/fetch/fetch_scala_bugs.py $DOWNLOADS/bugs/scala.txt \
        $DOWNLOADS/bugs/fixes/descriptions/scala $DOWNLOADS/bugs/scala.json $GH_TOKEN
```

This script fetches bugs for `scalac` and `dotty` from
<https://api.github.com>, it saves the URLs of the scripts
in `$DOWNLOADS/bugs/scala.txt`, the description and the summary for each
bug (with id: scala-XXXX or dotty-XXXX) in
`$DOWNLOADS/bugs/fixes/descriptions/scala/scala-XXXX`, and it saves
statistics such as `created` timestamp, `resolution` timestamp, and `reporter`
in `$DOWNLOADS/bugs/scala.json`.

5. Clone compilers' repositories.

```bash
./scripts/fetch/clone.sh $DOWNLOADS/repos
```

This script downloads a number of repositories that we need to get the fixes
of the analyzed bugs in `$DOWNLOADS/repos` directory. More specifically, it
downloads the following repositories.

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

6. Detect fixes of the downloaded bugs.

```
./scripts/fetch/find_fixes.sh $DOWNLOADS/bugs \
        $DOWNLOADS/bugs/fixes/descriptions $DOWNLOADS/repos \
        $DOWNLOADS/bugs/fixes $GH_TOKEN 2>&1 | tee $DOWNLOADS/logs
```

This script is responsible for detecting the fixes for the bugs we fetched with
the previous scripts. To do so, for each bug, it first searches in
the corresponding repository for commits with its bug id in the commit message.
If that fails and the repository is hosted in GitHub, then it searches for
PRs that have tagged the bug id. Then it saves the URLs of the bug ids, along
with their fixes in `$DOWNLOADS/bugs/fixes/{groovy,kotlin,java,scala}.txt`.


* Print stats of the download data.

```bash
./scripts/data_collection_stats.sh downloads/bugs
```

The above script prints the totals for the bugs collected in the previous step.
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

* Download and copy data for selected bugs in `data/iterations` (4.5 min).

```bash
./scripts/get_data_for_selected_bugs.sh downloads data
```
Finally, we need to get the fixes and the statistics for the selected bugs
of our dataset. This script takes as input the `download directory, which
includes the initial dataset, and the `data` directory, which must contain
an `iterations` directory` with the selected bugs. Specifically, in this
directory, some files contain bugs associated with their fixes.
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

## Reproduce Paper results

In the following section, we provide scripts that reproduce the results
presented in the paper using the dataset from `data` directory.

Collecting Bugs & Fixes (Section 2.1)
-------------------------------------

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


RQ1: Symptoms (Section 3.1)
---------------------------

For the first research question, we will use a script reproduce Fig 1 that
shows the distribution of symptom categories. To do so, run:

```bash
python scripts/rq1.py data/bugs.json --output figures/symptoms.pdf
```

This produces `symptoms.pdf` in the `figures` directory.
It also prints a table in standard output that presents the total values
and the percentages of symptoms per language. Specifically, it will print
the following.

```
Symptom                                Groovy           Java         Kotlin          Scala          Total
---------------------------------------------------------------------------------------------------------
Unexpected Compile-Time Error      59 (73.8%)     38 (47.5%)     30 (37.5%)     36 (45.0%)    163 (50.9%)
Internal Compiler Error            10 (12.5%)     25 (31.2%)     18 (22.5%)     26 (32.5%)     79 (24.7%)
Unexpected Runtime Behavior         9 (11.2%)     11 (13.8%)     22 (27.5%)     11 (13.8%)     53 (16.6%)
Misleading Report                    2 (2.5%)       4 (5.0%)       7 (8.8%)       5 (6.2%)      18 (5.6%)
Compilation Performance Issue        0 (0.0%)       2 (2.5%)       3 (3.8%)       2 (2.5%)       7 (2.2%)
```

RQ2: Bug Patterns (Section 3.2)
-------------------------------

For the second research question, first we will reproduce Figures 7a and 7b.
These figures demonstrates the distribution of bug patterns with regards to
the languages and the symptoms. Second, we will produce two tables, one for
each figure that display the total values and the percentages of the patterns.

```bash
python scripts/rq2.py data/bugs.json --patterns figures/patterns.pdf \
    --patterns-symptoms figures/patterns_symptoms.pdf
```

The above command produce the figures `figures/patterns.pdf` and
`figures/patterns_symptoms.pdf`, and it prints the following in the
standard output.

```
Pattern                                Groovy        Java      Kotlin       Scala       Total
---------------------------------------------------------------------------------------------
Type-related Bugs                  37 (46.2%)  34 (42.5%)  31 (38.8%)  27 (33.8%) 129 (40.3%)
Semantic Analysis Bugs             17 (21.2%)  16 (20.0%)  20 (25.0%)  24 (30.0%)  77 (24.1%)
Resolution & Environment Bugs      24 (30.0%)  17 (21.2%)  22 (27.5%)  14 (17.5%)  77 (24.1%)
Error Handling & Reporting Bugs      1 (1.2%)  10 (12.5%)    5 (6.2%)    6 (7.5%)   22 (6.9%)
AST Transformation Bugs              1 (1.2%)    3 (3.8%)    2 (2.5%)   9 (11.2%)   15 (4.7%)

Pattern                                Unexpected        Internal      Unexpected      Misleading     Compilation           Total
---------------------------------------------------------------------------------------------------------------------------------
Type-related Bugs                      90 (28.1%)       23 (7.2%)       10 (3.1%)        3 (0.9%)        3 (0.9%)     129 (40.3%)
Semantic Analysis Bugs                  24 (7.5%)       21 (6.6%)       27 (8.4%)        3 (0.9%)        2 (0.6%)      77 (24.1%)
Resolution & Environment Bugs          44 (13.8%)       11 (3.4%)       16 (5.0%)        5 (1.6%)        1 (0.3%)      77 (24.1%)
Error Handling & Reporting Bugs          0 (0.0%)       15 (4.7%)        0 (0.0%)        7 (2.2%)        0 (0.0%)       22 (6.9%)
AST Transformation Bugs                  5 (1.6%)        9 (2.8%)        0 (0.0%)        0 (0.0%)        1 (0.3%)       15 (4.7%)
```


RQ3: Bug Fixes (Section 3.3)
----------------------------

In the third research question, we study the duration and the fixes of the bugs.
Hence, we will produce Fig 13a, Fig 13b, and Fig 14. We will also print in
the standard output the mean, median, standard deviation, max, and min per
language for files number, lines number, and duration of the fixes.


```bash
python scripts/rq3.py data/diffs/ data/ --directory figures
```

The previous command saves Fig 13a in `figures/lines.pdf`, Fig 13b in
`figures/files.pdf`, and Fig 14 in `figures/duration.pdf`.
Note that you can use `--all` option to add lines for all languages in
the figures `lines.pdf` and `files.pdf`.
It also prints the following tables.

```
                         Lines
============================================================
          Mean      Median    SD        Min       Max
------------------------------------------------------------
Java      30        16        40        1         190
Kotlin    56        21        144       1         1177
Groovy    49        23        89        1         706
Scala     73        9         379       1         3381
------------------------------------------------------------
Total     52        16        208       1         3381

                         Files
============================================================
          Mean      Median    SD        Min       Max
------------------------------------------------------------
Java      1         1         1         1         5
Kotlin    2         2         2         1         15
Groovy    1         1         0         1         5
Scala     2         1         5         1         45
------------------------------------------------------------
Total     2         1         3         1         45

                      Duration
============================================================
          Mean      Median    SD        Min       Max
------------------------------------------------------------
Java      131       21        284       0         1621
Kotlin    164       34        296       0         1337
Groovy    122       8         278       0         1472
Scala     328       55        628       0         3209
------------------------------------------------------------
Total     186       24        407       0         3209
```

RQ4: Test Case Characteristics (Section 3.4)
--------------------------------------------

```bash
python scripts/rq4.py data/characteristics.json data/bugs.json data/test_cases/ \
    --output figures/characteristics.pdf
python scripts/lift.py data/bugs.json data/ data/diffs/
```

The first command produces Figure 15 (`figures/characteristics.pdf`) and prints
in standard output Tables 2, 3, and 4.
The second command prints the lift scores reported in Section 3.4.2.
