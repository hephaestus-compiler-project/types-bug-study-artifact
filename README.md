# Artifact for Well-Typed Programs Can Go Wrong: A Study of Typing-Related Bugs in JVM Compilers

This is the artifact for the paper titled
"Well-Typed Programs Can Go Wrong:
A Study of Typing-Related Bugs in JVM Compilers".

An archived version of the artifact will also be available on Zenodo,
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
* `data/bugs.json` contains all bugs from our study. Each bug has the following
fields:
    * `language`
    * `compiler`
    * `is_correct`: `True` if the test case is compilable. In case the test is
non-compilable, the value of this field is `False`.
    * `symptom`: the effect of this bug.
    * `pattern`: The category of this bug.
    * `root_cause`: The cause the introduced this bug.
    * `chars`: The characteristics of the test case that trigger the bug.
* `data/characteristics.json`: The categories and the sub-categories of
the characteristics that trigger the bugs in our dataset.
* `data/{groovy,java,kotlin,scala}.json`: data about the timestamp,
the reporter, the assignee, and the number of comments for each bug.
* `data/diffs/{groovy,java,kotlin,scala}/bug_id/*.diff`: The diff of the fix.
* `data/diffs/{groovy,java,kotlin,scala}/bug_id/stats.csv`: The LoC of the fix.
* `data/test_cases/{groovy,java,kotlin,scala}/bug_id/*.{kt,java,scala,groovy}`:
The test case of the fix.
* `data/test_cases/{groovy,java,kotlin,scala}/bug_id/stats.json`:
statistics for the fix (number of declarations, method/function calls, LoCs.
* `data/iterations/1/{groovy,java,kotlin,scala}.txt`: bugs analyzed in each
iteration, each line contains the URL for the bug report and the URL for the
fix of the bugs, separated by a comma.
* `data/collection`: Phase 2 dataset (4.153 bugs).


Requirements
------------

* A Unix-like operating system (tested on Ubuntu and Debian) with python3,
and the following packages installed.

```bash
apt install curl jq git mercurial diffstat cloc
pip install requests matplotlib pandas seaborn
```

* Otherwise, you can use Docker (see below).


Docker
------

```bash
docker build . -t bug-study
docker run -it \
    -v $(pwd)/scripts:/home/scripts \
    -v $(pwd)/downloads:/home/downloads \
    -v $(pwd)/data:/home/data \
    -v $(pwd)/figures:/home/figures \
    bug-study /bin/bash
```

Download the Data from sources
------------------------------

* Download data (~18 hours).

```bash
./scripts/fetch/fetch.sh downloads $GH_TOKEN
```

* Print stats for download data.

```bash
./scripts/data_collection_stats.sh downloads/bugs
```

* Download and copy data for selected bugs in `data/iterations` (4.5 min).

```bash
./scripts/get_data_for_selected_bugs.sh downloads data
```

Reproduce Paper results
-----------------------

* Bug collection stats (Section 2.1 -- Table 1).

```bash
./scripts/data_collection_stats.sh data/collection
```

* RQ1: symptoms (Section 3.1 -- Figure 1).

```bash
python scripts/rq1.py data/bugs.json --output figures/symptoms.pdf
```

The above command prints the distribution of symptoms per language and
it will save Figure 1 in `figures/symptoms.pdf`.

* RQ2: Bug Patterns (Section 3.2 -- Figure 7a and Figure 7b.

```bash
python scripts/rq2.py data/bugs.json --patterns figures/patterns.pdf \
    --patterns-symptoms figures/patterns_symptoms.pdf
```

This command prints the distribution of patterns per language and
it will save Figures 7a and 7b in `figures/patterns.pdf` and
`figures/patterns_symptoms.pdf`.

* RQ3: Bug Fixes (Section 3.3 -- Figure 13a, Figure 13b, and Figure 14).

```bash
python scripts/rq3.py data/diffs/ data/ --directory figures
```

The previous command prints statistics for the lines, files, and duration of
each bug fix. It also creates figures 13a, 13b, and 14 in
`figures/{files,lines,duration}.pdf`.

* RQ4: Test Case Characteristics (Section 3.4 -- Figure 14, Table 2, Table 3,
and Table 4).

```
python scripts/rq4.py data/characteristics.json data/bugs.json data/test_cases/ \
    --output figures/characteristics.pdf
python scripts/lift.py data/bugs.json data/ data/diffs/
```

The first command produces Figure 15 (`figures/characteristics.pdf`) and prints
in standard output Tables 2, 3, and 4.
The second command prints the lift scores reported in Section 3.4.2.
