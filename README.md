Artifact for ...
================

Overview
--------

Requirements
------------


```bash
apt install curl jq git mercurial diffstat cloc
pip install requests matplotlib pandas seaborn
```

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

* Download data (~18 hours)

```bash
./scripts/fetch/fetch.sh downloads $GH_TOKEN
```

* Print stats for download data

```bash
./scripts/data_collection_stats.sh downloads/bugs
```

* Download and copy data for selected bugs in `data/iterations` (4.5 min)

```bash
./scripts/get_data_for_selected_bugs.sh downloads data
```

Reproduce Paper results
-----------------------

```bash
./scripts/data_collection_stats.sh data/collection
python scripts/rq1.py data/bugs.json --output figures/symptoms.pdf
python scripts/rq2.py data/bugs.json --patterns figures/patterns.pdf \
    --patterns-symptoms figures/patterns_symptoms.pdf
python scripts/rq3.py data/diffs/ data/ --directory figures
python scripts/rq4.py data/characteristics.json data/bugs.json data/test_cases/ \
    --output characteristics.pdf
python scripts/lift.py data/iterations/ data/ data/diffs/
```
