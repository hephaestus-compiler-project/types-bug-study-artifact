# Artifact for "Well-Typed Programs Can Go Wrong: A Study of Typing-Related Bugs in JVM Compilers"

This is the artifact for the conditionally accepted
OOPSLA'21 paper titled
"Well-Typed Programs Can Go Wrong:
A Study of Typing-Related Bugs in JVM Compilers".

An archived version of the artifact will also be published on Zenodo,
upon the paper's publication.

# Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
  * [Setup](#setup)
    + [Option1: Ubuntu/Debian Installation](#option1-ubuntudebian-installation)
    + [Option2: Docker Image Installation](#option2-docker-image-installation)
  * [Downloading Bugs &amp; Fixes from Sources (Optionally)](#downloading-bugs--fixes-from-sources-optionally)
    + [Fetching Groovy Bugs](#fetching-groovy-bugs)
    + [Fetching Kotlin Bugs](#fetching-kotlin-bugs)
    + [Fetching Java bugs](#fetching-java-bugs)
    + [Fetching Scala bugs](#fetching-scala-bugs)
    + [Cloning Compilers' Repositories](#cloning-compilers-repositories)
    + [Detecting Bug Fixes](#detecting-bug-fixes)
  * [Downloading the 320 Typing-Related Bugs (Optionally)](#downloading-the-320-typing-related-bugs-optionally)
- [Selected Bugs](#selected-bugs)
  * [Details Regarding the Proposed Categorization](#details-regarding-the-proposed-categorization)
- [Step-by-Step Instructions](#step-by-step-instructions)
  * [Collecting Bugs &amp; Fixes (Section 2.1)](#collecting-bugs--fixes-section-21)
  * [RQ1: Symptoms (Section 3.1)](#rq1-symptoms-section-31)
  * [RQ2: Bug Patterns (Section 3.2)](#rq2-bug-patterns-section-32)
  * [RQ3: Bug Fixes (Section 3.3)](#rq3-bug-fixes-section-33)
  * [RQ4: Test Case Characteristics (Section 3.4)](#rq4-test-case-characteristics-section-34)
    + [Frequency of Test Case Characteristics](#frequency-of-test-case-characteristics)
    + [Correlation of Test Case Characteristics](#correlation-of-test-case-characteristics)
- [Other Utilities (Optionally)](#other-utilities-optionally)

# Overview

The purpose of this artifact is
(1) to reproduce the results
presented in our paper,
and (2) to document our dataset
and the proposed categorization in order to
facilitate further research.
Specifically,
the artifact has the following structure:

* `scripts/`: This is the directory that contains the scripts needed to
reproduce the results, the figures, and the tables presented in our paper.

* `scripts/fetch/`: This is the directory that contains the scripts needed
to construct the dataset of typing-related bugs
as described in Section 2.1 of our paper
(i.e., this directory actually contains the code of our _bug collection_
and _post filtering_ phases).

* `data/`: This is the "pre-baked" dataset of the 320 typing-related bugs
  under study (for more details about the selected bugs, please read section
  [Selected Bugs](#selected-bugs) of our artifact).


# Requirements

* A Unix-like operating system (tested on Ubuntu and Debian).

* An installation of Python3.

* (**Optionally**) An installation of Docker.
  If you are *not* running an Ubuntu/Debian OS, you are able to use
  the provided Docker image (found in `Dockerfile`) to download bugs
  and run the corresponding scripts in a reproducible way.

* (**Optionally**) At least 20GB of available disk space.
  You will need that space *only* if you decide to re-collect typing-related
  bugs (and their fixes) from the corresponding sources
  (for more details, see Section
  [Downloading Bugs &amp; Fixes from Sources](#downloading-bugs--fixes-from-sources-optionally)).

* (**Optionally**) A Github access token (see [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token))
  for interacting with the Github API.
  You will need this access token *only* if you decide to execute the
  instructions included in Section
  [Downloading Bugs &amp; Fixes from Sources](#downloading-bugs--fixes-from-sources-optionally)
  of our artifact.

# Getting Started

This section includes instructions and documentation for
(1) setting up the necessary environment in order
run our scripts,
(2) re-collecting typing-related bugs
taken from the issue trackers of Java, Scala, Kotlin,
and Groovy,
(3) the bugs under study and the proposed categorization.
The final output of this step is the directory `data/`,
which is ultimately used for answering our research questions.

## Setup

There are two options for reproducing the results of the paper.
If you are running an Ubuntu/Debian OS,
we provide instructions for installing the required
`apt` packages and libraries
used for running the scripts of the artifact.
Otherwise,
if you do not have an Ubuntu/Debian installation,
this artifact provides you with a Docker image
(defined in `Dockerfile`)
that contains the required environment
for executing the scripts
and reproducing the results of our paper.

#### Option1: Ubuntu/Debian Installation

**NOTE**: If you are not running an Ubuntu/Debian OS, please jump to the
Section [Option2: Docker Image Installation](#option2-docker-image-installation).

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

We provide a `Dockerfile` to build an image
that contains:

* The necessary `apt` packages (e.g., `cloc`) for running the
  scripts of our bug collection approach.
* The necessary Python packages (e.g., `matplotlib`) for running our
  evaluation scripts.
* A user named `user` with `sudo` privileges.

To build the Docker image named `bug-study` from source,
run the following command (estimated running time: ~5 min)

```bash
docker build . -t bug-study
```

Run the following command to create a new container.

```bash
docker run -it \
    --rm \
    -v $(pwd)/scripts:/home/user/scripts \
    -v $(pwd)/downloads:/home/user/downloads \
    -v $(pwd)/data:/home/user/data \
    -v $(pwd)/figures:/home/user/figures \
    bug-study /bin/bash
```

After executing the command, you will be able to enter the home directory
(i.e., `/home/user`). This directory contains
(1) the scripts for reproducing the results of the paper (see `scripts/`),
(2) the data of our bug study (see `data/`),
(3) a dedicated directory for storing the generated figures (see `figures/`),
and (4) `downloads/` which is the directory where the data
produced by the _bug collection_ and _post-filtering_ phases
will be saved (in case you decide to re-create the bug dataset).

**Further explanations**:
The option `-v` is used to mount a local volume inside the Docker container.
In this way, data produced during the execution of the container
will not be lost upon the container's exit
(e.g., the resulting figures will be stored in `$(pwd)/figures`
of your host machine).

**IMPORTANT NOTE**:
From now on,
if you chose to set up the necessary environment through Docker,
we assume that all the commands shown in the artifact below
are executed inside a Docker container
(which has been spawned by running the `docker run` on `bug-study` image).

## Downloading Bugs & Fixes from Sources (Optionally)

This section provides the instructions
to collect typing-related bugs and their fixes
(corresponding to Section 2.1 of our paper).

**IMPORTANT NOTE**:
This step requires roughly 18 hours.
For this reason,
we already provide you with the
"pre-baked" data of the selected bugs
used in our study,
along with the proposed categorization
(see the directory `data/`).
However,
if you still want to re-download the bugs from
the corresponding sources
and create the bug dataset on your own,
please continue reading this section.
Otherwise,
you can go directly to the next section
([Selected Bugs](#selected-bugs)).

To download and re-construct the initial dataset as described in
Section 2.1 of the paper, you will need at least 20 GB of available disk
space. At this point, we should note that the generated dataset will probably
contain more bugs than the dataset described in the paper because new bugs
will have been fixed from the time we downloaded the bugs until now.

Also, at this point you will need
a Github access token (see [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)).
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

The command above is a wrapper script
that executes the following six scripts
(which can be also executed as stand-alone tools).

1. `scripts/fetch/fetch_groovy_bugs.py`
2. `scripts/fetch/fetch_kotlin_bugs.py`
3. `scripts/fetch/fetch_java_bugs.py`
4. `scripts/fetch/fetch_scala_bugs.py`
5. `scripts/fetch/clone.sh`
6. `scripts/fetch/find_fixes.sh`

The first four scripts compose the _bug collection_ phase of our approach,
while the 6th script stands for the _post-filtering_ step.
Finally, the 5th script is used to clone the repositories of
compilers.
Below, you find further details regarding these scripts.


### Fetching Groovy Bugs

```bash
python scripts/fetch/fetch_groovy_bugs.py downloads/bugs/groovy.txt \
        downloads/bugs/fixes/descriptions/groovy \
        downloads/bugs/groovy.json
```

This script fetches `groovyc` bugs
using the Jira REST API
(see <https://issues.apache.org/jira/rest/api>).
It saves (1) the URLs of the retrieved bugs
in `downloads/bugs/groovy.txt`,
(2) the description and the summary of each
bug in
`downloads/bugs/fixes/descriptions/groovy/GROOVY-XXXX`
(where `XXXX` stands for the id of the bug),
and (3) some general statistics,
(such as `created` date, `resolution` date, and `reporter`)
in `downloads/bugs/groovy.json`.

This script fetches Groovy bugs from Jira by applying the following
filters (the query below is written in
[JQL](https://www.atlassian.com/blog/jira-software/jql-the-most-flexible-way-to-search-jira-14),
which is the query language of Jira):

```jql
project = "Groovy" AND
type = "bug" AND
resolution = "fixed" AND
status in ("Resolved", "Closed") AND
component = "Static Type Checker"
```

### Fetching Kotlin Bugs

```bash
python scripts/fetch/fetch_kotlin_bugs.py downloads/bugs/kotlin.txt \
        downloads/bugs/fixes/descriptions/kotlin \
        downloads/bugs/kotlin.json
```

This script fetches `kotlinc` bugs
using the YouTrack REST API
(see <https://youtrack.jetbrains.com/api/issues>).
The script stores
(1) the URLs of the retrieved `kotlinc` bugs
in `downloads/bugs/kotlin.txt`,
(2) the description and the summary for each
bug in
`downloads/bugs/fixes/descriptions/kotlin/KT-XXXX`,
and (3) some general statistics
(such as `created` date, `resolution` date, and `reporter`)
in `downloads/bugs/kotlin.json`.

To fetch `kotlinc` typing-related bugs,
the script above performs the following query:

```jql
project = "Kotlin" AND
Type in "("Bug", "Performance Problem") AND,
"State" = "Fixed" AND
Subsystems in (
  "Frontend. Resolution and Inference",
  "Frontend. Data-flow analysis",
  "Frontend. Control-flow analysis",
  "Frontend. Declarations",
  "Frontend"
)
```

### Fetching Java bugs

```bash
python scripts/fetch/fetch_java_bugs.py downloads/bugs/java.txt \
        downloads/bugs/fixes/descriptions/java \
        downloads/bugs/java.json
```

This script fetches `javac` bugs
using the Jira REST API
(see <https://bugs.openjdk.java.net/rest/api>),
The script saves
(1) the URLs of the retrieved bugs
in `downloads/bugs/java.txt`,
(2) the description and the summary for each bug in
`downloads/bugs/fixes/descriptions/java/JDK-XXXX`,
(3) some general statistics
(such as `created` date, `resolution` date, and `reporter`)
in `downloads/bugs/java.json`.

The script above fetches `javac` bugs by applying the following
query:

```jql
project = "JDK" AND
type = "bug" AND
resolution = "fixed" AND
status in ("Resolved", "Closed") AND,
component = "tools" AND
Subcomponent = "javac" AND
priority in ("P1", "P2", "P3")" AND (
  affectedVersion in (7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17) OR (
    fixVersion in (7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17) AND
    affectedVersion is EMPTY
  )
)
```

### Fetching Scala bugs

```bash
python scripts/fetch/fetch_scala_bugs.py downloads/bugs/scala.txt \
        downloads/bugs/fixes/descriptions/scala \
        downloads/bugs/scala.json $GH_TOKEN
```

This script fetches bugs related to `scalac` and `dotty`
using the Github REST API
(see <https://api.github.com>).
The script saves
(1) the URLs of the scripts
in `downloads/bugs/scala.txt`,
(2) the description and the summary for each bug in
`downloads/bugs/fixes/descriptions/scala/scala-XXXX`,
and (3) some general
statistics
(such as `created` date, `resolution` date, and `reporter`)
in `downloads/bugs/scala.json`.

For fetching Scala2 bugs that are relevant
to our study,
the script above filters bugs as follows:

```jql
label in (
  "typer",
  "infer",
  "should compile",
  "should not compile",
  "patmat",
  "overloading",
  "dependent types",
  "structural types",
  "existential",
  "gadt",
  "implicit classes",
  "implicit",
  "valueclass",
  "typelevel",
  "compiler crash"
) AND
label not in ("backend", "won't fix")
```

For filtering Dotty bugs,
the scripts applies the following filters:

```jql
label in ("itype:bug", "itype:crash", "itype:performance") AND
label in (
  "area:typer",
  "area:overloading",
  "area:gadt",
  "area:implicts",
  "area:f-bounds",
  "area:match-types",
  "itype:performance",
  "area:erasure"
) AND
label != "stat:wontfix"
```

### Cloning Compilers' Repositories

```bash
./scripts/fetch/clone.sh downloads/repos
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

### Detecting Bug Fixes

```bash
./scripts/fetch/find_fixes.sh downloads/bugs \
  downloads/bugs/fixes/descriptions downloads/repos \
  downloads/bugs/fixes $GH_TOKEN 2>&1 |
tee downloads/logs
```

This script is responsible for detecting fixes
associated with the bugs fetched by
the previous scripts.
To do so,
for each bug,
it first searches over
the corresponding repository for commits containing
the ID of the bug in the commit's message.
If that fails and the repository is hosted in GitHub,
then the script searches for
pull requests that have tagged the given bug ID.
The output of the script is
`downloads/bugs/fixes/{groovy,kotlin,java,scala}.txt`,
which contains the URL of each bug report and fix.


Finally,
to print some general statistics regarding
our bug collection approach run

```bash
./scripts/data_collection_stats.sh downloads/bugs
```

The above script prints the total number of bugs collected
in the previous step
reproducing Table 1 of our paper,
i.e., the output of the script is similar to the following.

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

## Downloading the 320 Typing-Related Bugs (Optionally)

**IMPORTANT NOTE:**
You have to complete the previous step in order
to proceed with this one.

To download the data associated with
the *specific* 320 typing-related that
were manually examined in our study,
run the following script (estimated running time: 4--5 min).

```bash
./scripts/fetch/get_data_for_selected_bugs.sh downloads data
```
The above script takes as input the `downloads/` directory
that includes the entire dataset of bugs,
and the `data/` directory that contains
an `iterations/` directory with the bugs examined in our study.
Note that the directory `iterations/` includes the bugs
that were selected and manually analyzed in each iteration
as described in Section 2.2 of our paper.
For example,
the file `data/iterations/1/java.txt` shows the `javac` bugs
that we manually studied in the first iteration
of our bug analysis.

Regarding its execution,
the script `scripts/fetch/get_data_for_selected_bugs.sh`
first downloads the revisions of bug fixes
corresponding to each of the selected bugs,
and then stores some general statistics for these fixes in
the `data/diffs/{groovy,java,kotlin,scala}/bug_id/` directory.
Each generated directory contains a `.diff` and a `stats.csv` file.
The `.diff` file is the revision of the corresponding fix,
while the `stats.csv` file enumerates,
for each source file,
how many lines are inserted, deleted or modified by the revision.


# Selected Bugs

Now, we provide details regarding the 320 typing-related bugs
studied in our paper.
These details can be found in the `data/` directory,
which has the following structure:

* `data/bugs.json`: This document contains all 320 bugs examined in our study
                    and their categorization.
                    Each bug entry has the following fields:
    * `language`: The language of the compiler.
    * `compiler`: The compiler in which the bug occurred.
    * `is_correct`: `True` if the bug-revealing test case is compilable;
       `False` otherwise.
    * `symptom`: The bug's symptom.
    * `bug_cause`: The root cause of the bug. A bug cause may contain
      subcategories. The subcategory of a specific bug cause is shown
      by the the `subcategory` field. Example:
      ```json
      "bug_cause": {
        "category": "Type-related Bugs",
        "subcategory": "Incorrect Type Comparison & Bound Computation"
      }
      ```
    * `error`: This field indicates how the bug was introduced.
    * `chars`: This field contains the characteristics of the bug-revealing test case.
       This field contains two more fields: (1) `characteristics` corresponding to
       language features involved in each test case (e.g., Inheritance),
       and (2) `categories` that includes the groups to which these language
       features belong (e.g., OOP features).

* `data/characteristics.json`: This document contains the categories
   and the sub-categories of the bug-revealing test cases.

* `data/{groovy,java,kotlin,scala}.json`: Other general information
   for each bug, i.e.,
   the creation and resolution date of bug,
   the assignee of bug,
   and the number of comments associated with the corresponding bug report.

* `data/diffs/{groovy,java,kotlin,scala}/bug_id/*.diff`: The revisions associated with
   the fix of bug with ID `bug_id`.

* `data/diffs/{groovy,java,kotlin,scala}/bug_id/stats.csv`:
   For each source file affected by the fix of bug with ID `bug_id`,
   this file enumerates how many lines of code are inserted, deleted,
   or modified.

* `data/test_cases/{groovy,java,kotlin,scala}/bug_id/*.{kt,java,scala,groovy}`:
The test case that triggers the bug with ID `bug_id`.

* `data/test_cases/{groovy,java,kotlin,scala}/bug_id/stats.json`:
Statistics on the bug-revealing test case (number of declarations,
method/function calls, LoCs) associated with the bug
with ID `bug_id`.

* `data/iterations/iter/{groovy,java,kotlin,scala}.txt`: Bugs analyzed in the
iteration `iter`.
Each line contains two entries (comma separated):
(1) the URL pointing to the bug report,
and (2) the URL pointing to the fix of the bug.

* `data/collection/`: This is the entire dataset of bugs produced
 after applying the _post-filtering_ step of our bug collection approach.

## Details Regarding the Proposed Categorization

The documentation of our categorizations
(i.e., symptoms, bug causes, error types, and test case characteristics)
can be found in our OOPSLA paper or can be viewed through
your browser by opening the `docs/_build/html/index.html` file.


# Step-by-Step Instructions

In the following section, we provide instructions
for reproducing the results
presented in the paper using the data coming from the `data/` directory.


## Collecting Bugs & Fixes (Section 2.1)

Run the following script to print statistics
related to our bug collection phases.
Specifically, the script reproduces Table 1.

```bash
./scripts/data_collection_stats.sh data/collection
```

The above script prints the following

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

In the first research question,
we compute the distribution of bug symptoms.
To do so, please run:

```bash
python scripts/rq1.py data/bugs.json --output figures/symptoms.pdf
```

The above script produces
the `symptoms.pdf` file in the `figures/` directory.
For those who are running the above script inside a Docker container,
the script also prints the distribution of symptoms in a tabular format.
Specifically, it prints
the following

```
Symptom                               groovyc          javac        kotlinc scalac & Dotty          Total
---------------------------------------------------------------------------------------------------------
Unexpected Compile-Time Error     59 (73.75%)    38 (47.50%)    30 (37.50%)    36 (45.00%)   163 (50.94%)
Internal Compiler Error           10 (12.50%)    25 (31.25%)    18 (22.50%)    26 (32.50%)    79 (24.69%)
Unexpected Runtime Behavior        9 (11.25%)    11 (13.75%)    22 (27.50%)    11 (13.75%)    53 (16.56%)
Misleading Report                   2 (2.50%)      4 (5.00%)      7 (8.75%)      5 (6.25%)     18 (5.62%)
Compilation Performance Issue       0 (0.00%)      2 (2.50%)      3 (3.75%)      2 (2.50%)      7 (2.19%)
```

However, please note that Docker users are still able to examine
the resulting figure by opening the
pdf file `$(pwd)/figures/symptoms.pdf` stored in their host machine.
The same also applies for the output figures of the next research
questions.

## RQ2: Bug Patterns (Section 3.2)

For the second research question, we compute the distribution of
bug causes with regards to the examined compilers,
and bug symptoms.
This reproduces Figures 7a and 7b.
As in the first research question,
our script also reports the above distributions
in a tabular format.
Run the following command:

```bash
python scripts/rq2.py data/bugs.json \
    --patterns figures/patterns.pdf \
    --patterns-symptoms figures/patterns_symptoms.pdf
```

The above command produces the figures `figures/patterns.pdf` (Figure 7a)
and `figures/patterns_symptoms.pdf` (Figure 7b),
and it prints the following tables in the standard output.

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
Hence, we produce Figure 13a, Figure 13b, and Figure 14. We also
report the mean, median, standard deviation, max, and min
of the following metrics:
* number of files affected by a fix
* lines of code affected by a fix
* duration of a fix

To produce the aforementioned figures and metrics,
please run

```bash
python scripts/rq3.py data/diffs/ data/ --directory figures
```

The previous command takes two inputs.
The first input (i.e., `data/diffs/`)
is the revisions of bug fixes,
while the second input (i.e., `data/`)
is the directory where the JSON files
(e.g., `data/kotlin.json`)
containing
general information
(e.g., creation date, resolution date)
about the examined bugs are located.
The previous command saves Figure 13a in `figures/lines.pdf`,
Figure 13b in `figures/files.pdf`,
and Figure 14 in `figures/duration.pdf`.

The script also prints the following tables

```
                 Lines of Code
============================================================
          Mean      Median    SD        Min       Max
------------------------------------------------------------
Java      30.95     16.00     40.60     1.00      190.00
Kotlin    56.15     21.50     144.21    1.00      1177.00
Groovy    49.10     23.00     89.20     1.00      706.00
Scala     73.40     9.50      379.35    1.00      3381.00
------------------------------------------------------------
Total     52.40     16.00     208.33    1.00      3381.00

      Number of Affected Files
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

Note that this script can take an extra command-line
flag,
namely `--all`,
used for creating figures that contain plots
for every compiler
Therefore,
to re-create Figure 14 as shown in our paper,
you have to run

```bash
python scripts/rq3.py data/diffs/ data/ \
  --directory figures --all
```

and then open `figures/duration.pdf`.


## RQ4: Test Case Characteristics (Section 3.4)

For this research question,
we examine the distribution and the correlation
of test case characteristics.

### Frequency of Test Case Characteristics

To compute the frequency of test case
characteristics,
we use a script that generates Figure 15,
prints Tables 2, 3, and 4,
and reports some metrics mentioned in Sections 3.4.2
and 3.4.3 of our paper.
Please run

```bash
python scripts/rq4.py data/characteristics.json \
   data/bugs.json data/test_cases/ \
    --output figures/characteristics.pdf
```

This script takes three inputs.
The first input `data/characteristics.json` is the file
that contains the frequency of every test case characteristic.
The second input (`data/bugs.json`) is the file that
contains our categorization for every examined bug,
while the third one stands for the directory
of test cases.


The above script generates `figures/characteristics.pdf` and reports:

```
General Statistics on Test Case Characteristics (Table 2)
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

Most Frequent Features (Table 3)
===============================================================
Parameterized type                                       46.56%
Type argument inference                                  31.87%
Parameterized class                                      30.00%
Parameterized function                                   26.25%
Inheritance                                              24.06%

Least frequent features (Table 3)
===============================================================
Multiple implements                                       2.19%
This                                                      2.19%
Arithmetic Expressions                                    1.88%
Loops                                                     1.25%
Sealed Classes                                            0.94%

Most Bug-Triggering Features per Language (Table 4)
===========================================================================================================================================================
                 Java                                 Groovy                                Kotlin                                Scala
-----------------------------------------------------------------------------------------------------------------------------------------------------------
Parameterized type            51.25% | Parameterized type            41.25% | Parameterized type            36.25% | Parameterized type            57.50% |
Type argument inference       42.50% | Collection API                35.00% | Parameterized class           33.75% | Parameterized class           42.50% |
Functional interface          37.50% | Type argument inference       35.00% | Type argument inference       32.50% | Inheritance                   32.50% |
Parameterized function        35.00% | Lambda                        25.00% | Parameterized function        26.25% | Implicits                     23.75% |
Parameterized class           30.00% | Parameterized function        21.25% | Inheritance                   25.00% | Parameterized function        22.50% |

Frequency of Characteristic Categories (see Section 3.4.2)
========================================
Parametric polymorphism           57.19%
OOP features                      53.75%
Type inference                    43.44%
Type system features              36.25%
Functional programming            31.56%
Standard library                  30.63%
Standard features                 28.75%
Other                             28.75%

Comparative Analysis Stats (see Section 3.4.3)
===========================================
Scala Implicits: 23.75
Scala Higher-kinded types: 13.75
Scala Pattern matching: 21.25
Scala Algebraic Data Types: 13.75
Kotlin Nullable types: 16.25
Kotlin Extension function / property: 15.00
```

This script is useful for finding what
are the most and least bug-triggering language features.
For completeness and benefiting future researchers,
the `scripts/rq4.py` provides three extra command-line options
used for presenting the full results of our study
(some results are not presented in the paper for brevity).

#### Example: Configuring the Entries of Table 3

For displaying Table 3 with more or fewer entries,
use the `--limit` option by providing the
desired number of table entries.
For example,
to produce Table 3 that shows the 30 most and
the 30 least frequent language features
that are supported by all the examined compilers,
run

```bash
 python scripts/rq4.py data/characteristics.json \
    data/bugs.json data/test_cases/ \
        --output figures/characteristics.pdf --limit 30
```

The script produces an output that contains the following tables

```
Most Frequent Features (Table 3)
===============================================================
Parameterized type                                       46.56%
Type argument inference                                  31.87%
Parameterized class                                      30.00%
Parameterized function                                   26.25%
Inheritance                                              24.06%
Collection API                                           21.88%
Lambda                                                   19.06%
Bounded type parameters                                  17.81%
Subtyping                                                16.25%
Overriding                                               15.62%
SAM type                                                 13.44%
Overloading                                              11.25%
Function reference                                        8.75%
Parameter type inference                                  8.12%
Nested class                                              7.81%
Wildcard type                                             7.50%
Function type                                             7.50%
Conditionals                                              6.56%
Variable type inference                                   6.25%
Anonymous class                                           5.62%
Array                                                     5.62%
Use-site variance                                         5.31%
Function API                                              5.31%
Java interoperability                                     5.31%
Access modifier                                           5.00%
Cast                                                      4.69%
Property                                                  4.06%
Reflection API                                            3.75%
Import                                                    3.44%
Variable arguments                                        3.44%

Least frequent features (Table 3)
===============================================================
Subtyping                                                16.25%
Overriding                                               15.62%
SAM type                                                 13.44%
Overloading                                              11.25%
Function reference                                        8.75%
Parameter type inference                                  8.12%
Nested class                                              7.81%
Wildcard type                                             7.50%
Function type                                             7.50%
Conditionals                                              6.56%
Variable type inference                                   6.25%
Anonymous class                                           5.62%
Array                                                     5.62%
Use-site variance                                         5.31%
Function API                                              5.31%
Java interoperability                                     5.31%
Access modifier                                           5.00%
Cast                                                      4.69%
Property                                                  4.06%
Reflection API                                            3.75%
Import                                                    3.44%
Variable arguments                                        3.44%
Try / catch                                               3.12%
Augmented assignment operator                             2.50%
Multiple implements                                       2.19%
This                                                      2.19%
Enums                                                     2.19%
Arithmetic expression                                     1.88%
Loops                                                     1.25%
Sealed class                                              0.94%

```


#### Example: Configuring the Entries of Table 4

For producing a version of Table 4
containing more entries,
our scripts provides the `--top` option.
For example,
to display the 20 most bug-triggering features
per language, run

```bash
 python scripts/rq4.py data/characteristics.json \
    data/bugs.json data/test_cases/ \
        --output figures/characteristics.pdf --top 20
```

This yields an output containing the following Table

```
Most Bug-Triggering Features per Language (Table 4)
===========================================================================================================================================================
                 Java                                 Groovy                                Kotlin                                Scala
-----------------------------------------------------------------------------------------------------------------------------------------------------------
Parameterized type            51.25% | Parameterized type            41.25% | Parameterized type            36.25% | Parameterized type            57.50% |
Type argument inference       42.50% | Collection API                35.00% | Parameterized class           33.75% | Parameterized class           42.50% |
SAM type                      37.50% | Type argument inference       35.00% | Type argument inference       32.50% | Inheritance                   32.50% |
Parameterized function        35.00% | Lambda                        25.00% | Parameterized function        26.25% | Implicits                     23.75% |
Parameterized class           30.00% | Parameterized function        21.25% | Inheritance                   25.00% | Parameterized function        22.50% |
Inheritance                   22.50% | Subtyping                     21.25% | Lambda                        25.00% | Pattern matching              21.25% |
Collection API                22.50% | Parameter type inference      17.50% | Function type                 17.50% | Type argument inference       17.50% |
Subtyping                     21.25% | SAM type                      15.00% | Nullable type                 16.25% | Type definition / member      17.50% |
Lambda                        21.25% | Parameterized class           13.75% | Extension function / property 15.00% | Bounded type parameters       17.50% |
Bounded type parameters       20.00% | Inheritance                   13.75% | Collection API                13.75% | Collection API                16.25% |
Function reference            17.50% | Primitive type                12.50% | Conditionals                  13.75% | Singleton object              15.00% |
Overloading                   16.25% | Overriding                    11.25% | Function reference            13.75% | Case class                    15.00% |
Function API                  15.00% | Variable type inference       10.00% | Overriding                    13.75% | Higher-kinded type            13.75% |
Overriding                    13.75% | Property                      10.00% | Subtyping                     12.50% | Algebraic data type           13.75% |
Use-site variance             12.50% | Array                          8.75% | Flow typing                    8.75% | Function type                 12.50% |
Cast                          11.25% | Named arguments                6.25% | Bounded type parameters        8.75% | Wildcard type                 12.50% |
Nested class                  10.00% | Access modifier                6.25% | Wildcard type                  8.75% | Special method overriding     12.50% |
Conditionals                  10.00% | Java interoperability          6.25% | Java interoperability          8.75% | Overriding                    11.25% |
Array                         10.00% | Flow typing                    5.00% | Variable type inference        8.75% | Subtyping                     10.00% |
Anonymous class                8.75% | Overloading                    5.00% | Operator overloading           8.75% | Nested class                  10.00% |

```

#### Example: Showing the Distribution of All Language Features

Figure 15 (as presented in our paper)
shows the four most frequent language feature
per category.
To show the full results,
use the command-line flag `--all`
as follows

```bash
 python scripts/rq4.py data/characteristics.json \
   data/bugs.json data/test_cases/ \
    --output figures/characteristics.pdf --all
```


This dumps the following Table to standard output.
Note that this table actually corresponds to
a complete version of Figure 15.

```
Distribution of Language Features (corresponding to a complete version of Figure 15)
=============================================================================================
Feature                          Category                           # Test Cases        Common
---------------------------------------------------------------------------------------------
Lambda                           Functional programming             61                  True
SAM type                         Functional programming             43                  True
Function reference               Functional programming             28                  True
Function type                    Functional programming             24                  True
Eta expansion                    Functional programming             2                   False
Inheritance                      OOP features                       77                  True
Overriding                       OOP features                       50                  True
Overloading                      OOP features                       36                  True
Nested class                     OOP features                       25                  True
Anonymous class                  OOP features                       18                  True
Access modifier                  OOP features                       16                  True
Singleton object                 OOP features                       14                  False
Property                         OOP features                       13                  True
Case class                       OOP features                       12                  False
Special method overriding        OOP features                       10                  True
Static method                    OOP features                       9                   False
Operator overloading             OOP features                       7                   True
Multiple implements              OOP features                       7                   True
This                             OOP features                       7                   True
Secondary constructor            OOP features                       5                   False
Delegation                       OOP features                       4                   False
Sealed class                     OOP features                       3                   True
Self type                        OOP features                       3                   False
Property reference               OOP features                       3                   False
Value class                      OOP features                       2                   False
Data class                       OOP features                       1                   False
Implicits                        Other                              19                  False
Java interoperability            Other                              17                  True
Pattern matching                 Other                              17                  False
Extension function / property    Other                              12                  False
Type annotations                 Other                              9                   False
Named arguments                  Other                              7                   False
Option type                      Other                              5                   False
Elvis operator                   Other                              5                   False
Call by name                     Other                              4                   False
Inline                           Other                              4                   False
Template string                  Other                              3                   False
Safe navigation operator         Other                              2                   False
Erased parameter                 Other                              1                   False
Default initializer              Other                              1                   False
Null assertion                   Other                              1                   False
With                             Other                              1                   False
Parameterized type               Parametric polymorphism            149                 True
Parameterized class              Parametric polymorphism            96                  True
Parameterized function           Parametric polymorphism            84                  True
Bounded type parameters          Parametric polymorphism            57                  True
Use-site variance                Parametric polymorphism            17                  True
F-bounds                         Parametric polymorphism            14                  True
Declaration-site variance        Parametric polymorphism            12                  False
Higher-kinded type               Parametric polymorphism            11                  False
Multi-bounds                     Parametric polymorphism            3                   True
Conditionals                     Standard language features         21                  True
Array                            Standard language features         18                  True
Cast                             Standard language features         15                  True
Import                           Standard language features         11                  True
Variable arguments               Standard language features         11                  True
Try / catch                      Standard language features         10                  True
Augmented assignment operator    Standard language features         8                   True
Enums                            Standard language features         7                   True
Arithmetic expression            Standard language features         6                   True
Loops                            Standard language features         4                   True
Collection API                   Standard library                   70                  True
Function API                     Standard library                   17                  True
Reflection API                   Standard library                   12                  True
Coroutines API                   Standard library                   4                   False
Stream API                       Standard library                   2                   False
Delegation API                   Standard library                   1                   False
Type argument inference          Type inference                     102                 True
Parameter type inference         Type inference                     26                  True
Variable type inference          Type inference                     20                  True
Flow typing                      Type inference                     11                  False
Build-style inference            Type inference                     4                   False
Return type inference            Type inference                     2                   False
Subtyping                        Type system-related features       52                  True
Wildcard type                    Type system-related features       24                  True
Type definition / member         Type system-related features       16                  False
Primitive type                   Type system-related features       14                  False
Nullable type                    Type system-related features       13                  False
Algebraic data type              Type system-related features       11                  False
Dependent type                   Type system-related features       7                   False
Intersection type                Type system-related features       5                   False
Nothing                          Type system-related features       3                   False
Type lambdas                     Type system-related features       3                   False
Type projection                  Type system-related features       3                   False
Union type                       Type system-related features       2                   False
Opaque type                      Type system-related features       1                   False
Mixins                           Type system-related features       1                   False
Match type                       Type system-related features       1                   False

```


### Correlation of Test Case Characteristics

To compute the lift scores mentioned in Section 3.4.3
of our paper, please run the following command

```bash
python scripts/lift.py data/bugs.json data/ data/diffs/
```

This script generates the following:

```
Pair (Test Case Characteristics (Categories) -> Test Case Characteristics (Categories))    Lift Score
=================================================================================================================
Standard library -> Functional programming                                                 5.3639
Standard library -> Type inference                                                         5.1717

Pair (Test Case Characteristics -> Test Case Characteristics)                              Lift Score
=================================================================================================================
Variable arguments -> Overloading                                                          24.0282
Use-site variance -> Parameterized function                                                17.1765
Type argument inference -> Parameterized function                                          12.7034
Implicits -> Parameterized class                                                           10.926
Type argument inference -> Collection API                                                  8.5882
Type argument inference -> Parameterized type                                              6.9599
```

#### Using lift.py for Computing Various Lift Scores

Note that `lift.py` can also be used to compute various lift scores.
i.e., computing the correlation between various aspects of the
examined bugs (e.g., correlation between bug causes and lines of code
affected by a fix).

You can set the number of pairs to print
by providing the `--limit` option.
The option `--threshold` is used to display
pairs whose lift score is greater than the given option.
Finally,
`--ithreshold`
sets a population threshold that pairs must exceed.

The detailed usage guide of `lift.py` is shown below

```
.env ❯ python scripts/lift.py --help
usage: lift.py [-h] [--threshold THRESHOLD] [--ithreshold ITHRESHOLD] [--limit LIMIT] [--A {symptoms,bug_causes,duration,loc,files,errors,test_chars,test_char_cat}]
               [--B {symptoms,bug_causes,duration,loc,files,errors,test_chars,test_char_cat}]
               bugs stats diffs

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
  --A {symptoms,bug_causes,duration,loc,files,errors,test_chars,test_char_cat}
                        Name of first bug aspect
  --B {symptoms,bug_causes,duration,loc,files,errors,test_chars,test_char_cat}
                        Name of first bug aspect
```

#### Example: Using lift.py for Computing the Correlation Between Symptoms and Bug Causes

Run the following command to compute the lift scores between symptoms
and bug causes

```bash
python scripts/lift.py data/bugs.json data/ data/diffs/ \
  --A symptoms --B bug_causes \
  --threshold 1 \
  --limit 5
```

This yields


```
Pair (Symptoms -> Bug Causes)                                                              Lift Score
=================================================================================================================
Internal Compiler Error -> Bugs Related to Error Handling & Reporting                      2.7618
Unexpected Runtime Behavior -> Semantic Analysis Bugs                                      2.1171
Unexpected Compile-Time Error -> Type-related Bugs                                         1.3697
Unexpected Runtime Behavior -> Resolution Bugs                                             1.2546
Unexpected Compile-Time Error -> Resolution Bugs                                           1.1218
Internal Compiler Error -> Semantic Analysis Bugs                                          1.1047
```

By examining the output above,
we can presume that bugs related to error handling & reporting
have the strongest correlation with the symptom "Internal Compiler Error".
This is because this kind of bugs often manifest as compiler crashes.

Also notice that the provided options `--A` and `--B`
stand for the bug aspects for which we compute their lift scores.
The available options are

* `symptoms` for bug symptoms
* `bug_causes` for bug causes
* `duration` for bug duration
* `loc` for lines of code affected by bug fixes
* `files` for number of files affected by bug fixes
* `errors` for error types (e.g., algorithmic error, logic error, etc.)
* `test_chars` for test case characteristics
* `test_char_cat` for categories of test case characteristics (e.g., OOP Features,
   Functional Programming Features, etc.)


Docker users can now exit the container by running

```bash
exit
```


# Other Utilities (Optionally)

Our research artifact also offers a Docker image
that runs a MongoDB instance.
This MongoDB instance allows future researchers to
perform queries over our selected bugs and their categorization.
To spawn this MongoDB instance,
first convert our bug dataset into the desired format
so that it can be easily stored in the Mongo database.
Please execute:

```bash
python3 scripts/data-converter.py data/bugs.json data/bug-collection.json
```

This script takes the JSON file that includes the studied bugs,
and creates a collection of bugs stored in `data/bug-collection.json`.

Now, you can build the Docker image
(namely `bugdb`)
that contains an installation of Mongo,
by running
(estimated running time: ~1 min)

```bash
docker build -t bugdb -f db.Dockerfile .
```

You are ready to spawn a new MongoDB instance by
running

```bash
docker run --rm --name bug-container \
  -d -p 27017:27017 bugdb mongod
```

Then, enter a `mongo` shell of the running MongoDB instance
by executing

```bash
docker exec -i -t bug-container bash -c "mongo db"
```

Once entering the `mongo` shell,
you are now ready to perform any Mongo query over
our bug collection called (`bugs`).

## Examples

For example, count the number of bugs

```mongo
> db.bugs.count()
320
```

Display the ID of the selected bugs

```mongo
> db.bugs.find({}, {'bug_id': 1, '_id': 0})
{ "bug_id" : "JDK-8254557" }
{ "bug_id" : "JDK-8258972" }
{ "bug_id" : "JDK-8144066" }
{ "bug_id" : "JDK-7040883" }
{ "bug_id" : "JDK-8029721" }
{ "bug_id" : "JDK-8129214" }
{ "bug_id" : "JDK-8203277" }
{ "bug_id" : "JDK-8231461" }
{ "bug_id" : "JDK-6995200" }
{ "bug_id" : "JDK-8202597" }
{ "bug_id" : "JDK-8195598" }
{ "bug_id" : "JDK-8144832" }
{ "bug_id" : "JDK-6996914" }
{ "bug_id" : "JDK-8169091" }
{ "bug_id" : "JDK-8012238" }
{ "bug_id" : "JDK-8152832" }
{ "bug_id" : "JDK-8191802" }
{ "bug_id" : "JDK-6476118" }
{ "bug_id" : "JDK-8154180" }
{ "bug_id" : "JDK-8029569" }
Type "it" for more

```

Count the number of bugs that are crashes

```mongo
> db.bugs.count({symptom: 'Internal Compiler Error'})
79
```


Find Scala bugs whose test cases involve implicits
and these test cases are non-compilable

```mongo
> db.bugs.find({
    language: 'Scala',
    'chars.characteristics': 'Implicits',
    'is_correct': false
  }, {
    bug_id: 1,
    _id: 0
  })
```

This query returns three Scala bugs, namely,

```
{ "bug_id" : "Dotty-9044"  }
{ "bug_id" : "Scala2-5231"  }
{ "bug_id" : "Scala2-9231"  }
```
