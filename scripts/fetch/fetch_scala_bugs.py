"""Fetch scala/dotty bugs.

"""
import argparse
import requests
import os
import json
from datetime import datetime


SCALA_LABELS = [
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
]
SCALA_LABELS = "labels=" + "&labels=".join(SCALA_LABELS)
DOTTY_TYPE_LABELS = ["itype:bug", "itype:crash"]
DOTTY_AREA_LABELS = [
    "area:typer",
    "area:overloading",
    "area:gadt",
    "area:implicts",
    "area:f-bounds",
    "area:match-types",
    "itype:performance",
    "area:erasure"
]


def filter_scala(x):
    return (any(l['name'] in SCALA_LABELS for l in x['labels']) and
            not any(l['name'] in ("won't fix", "backend ")
                    for l in x['labels']))


def filter_dotty(x):
    return (any(l['name'] in DOTTY_TYPE_LABELS for l in x['labels']) and
            any(l['name'] in DOTTY_AREA_LABELS for l in x['labels']) and
            not any(l['name'] == "label:stat:wontfix" for l in x['labels']))


# Rate limit is 5000 requests per hour
def get_data(descriptions, token, repo):
    name = "scala" if "scala" in repo else "dotty"
    filter_func = filter_scala if repo == "scala/bug" else filter_dotty
    headers = {'Authorization': f'token {token}'}
    data = []
    statistics = {}
    page = 1
    max_per_request = 100
    temp_data = []
    first = True
    while len(temp_data) == max_per_request or first:
        first = False
        # repo format: owner/repo_name
        base = "https://api.github.com/repos/{}/issues".format(repo)
        url = "{base}?state=closed&per_page={pp}&page={p}".format(
            base=base,
            pp=max_per_request,
            p=page
        )
        response = requests.get(url, headers=headers).json()
        temp_data = response
        filtered = list(filter(filter_func, temp_data))
        res = []
        for item in filtered:
            created = datetime.strptime(
                item['created_at'], "%Y-%m-%dT%H:%M:%S%z")
            resolution = datetime.strptime(
                item['closed_at'], "%Y-%m-%dT%H:%M:%S%z")
            passed = resolution - created
            reporter = item['user']['login']
            if item['assignee']:
                assignee = item['assignee']['login']
            else:
                assignee = ""
            comments = int(item['comments'])
            stats = {
                "created": str(created),
                "resolution": str(resolution),
                "passed": str(passed),
                "comments": comments,
                "reporter": reporter,
                "assignee": assignee,
                "reporter_is_assigned": reporter == assignee
            }
            statistics[name + '-' + str(item['number'])] = stats
            res.append(item['html_url'])
            description = item['body']
            description = description if description is not None else ""
            filename = name + '-' + str(item['number'])
            with open(os.path.join(descriptions, filename), 'w') as out:
                out.write(description)
        data.extend(res)
        page += 1
    return data, statistics


def get_args():
    parser = argparse.ArgumentParser(
        description='Fetch scala/dotty front-end bugs.')
    parser.add_argument("output", help="File to save the bugs.")
    parser.add_argument(
        "descriptions", help="Directory to save files with descriptions")
    parser.add_argument(
        "statistics", help="File to save stats")
    parser.add_argument("token", help="Github token.")
    return parser.parse_args()


def main():
    args = get_args()
    os.makedirs(args.descriptions, exist_ok=True)
    scala_data, statistics = get_data(
        args.descriptions, args.token, "scala/bug")
    dotty_data, dotty_stats = get_data(
        args.descriptions, args.token, "lampepfl/dotty")
    statistics.update(dotty_stats)
    data = scala_data + dotty_data
    print('writing data')
    directory, _ = os.path.split(args.output)
    stats_dir, _ = os.path.split(args.statistics)
    if directory:
        os.makedirs(directory, exist_ok=True)
    if stats_dir:
        os.makedirs(stats_dir, exist_ok=True)
    with open(args.output, 'w') as f:
        for url in data:
            f.write(url + "\n")
    with open(args.statistics, 'w') as f:
        json.dump(statistics, f, indent=4)


if __name__ == "__main__":
    main()
