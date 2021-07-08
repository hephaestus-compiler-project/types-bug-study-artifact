"""Fetch kotlin bugs.
"""
import argparse
import requests
import os
import json
from datetime import datetime


def get_data(descriptions):
    data = []
    first = True
    skip = 0
    top = 2500
    statistics = {}
    temp_data = []
    while len(temp_data) > 0 or first:
        first = False
        base = "https://youtrack.jetbrains.com/api/issues"
        search_terms = [
            "project: Kotlin",
            "Type: Bug, {Performance Problem}",
            "State: Fixed",
            ("Subsystems: {Frontend. Resolution and Inference}, "
             "{Frontend. Data-flow analysis}, "
             "{Frontend. Control-flow analysis}, "
             "{Frontend. Declarations}, "
             "Frontend")
        ]
        query = "%20".join(map(lambda x: x.replace(" ", "%20"), search_terms))
        fields = "idReadable,description,created,reporter(login),resolved,"
        fields += "comments,fields(value(login))"
        url = "{base}?query={query}&fields={fields}&$skip={skip}&$top={top}"
        url = url.format(
            base=base,
            query=query,
            fields=fields,
            skip=skip,
            top=top
        )
        response = requests.get(url)
        youtrack_url = "https://youtrack.jetbrains.com/issue/"
        temp_data = [youtrack_url + item['idReadable']
                     for item in response.json()]
        temp_data = []
        for item in response.json():
            created = datetime.utcfromtimestamp(int(item['created']) / 1000.0)
            resolution = datetime.utcfromtimestamp(
                int(item['resolved']) / 1000.0)
            passed = resolution - created
            reporter = item['reporter']['login']
            try:
                assignee = item['fields'][4]['value']['login']
            except TypeError:
                assignee = ""
            comments = len(list(filter(lambda x: x['$type'] == "IssueComment",
                                       item['comments'])))
            stats = {
                "created": str(created),
                "resolution": str(resolution),
                "passed": str(passed),
                "comments": comments,
                "reporter": reporter,
                "assignee": assignee,
                "reporter_is_assigned": reporter == assignee
            }
            statistics[item['idReadable']] = stats
            temp_data.append(youtrack_url + item['idReadable'])
            description = item['description']
            description = description if description is not None else ""
            with open(os.path.join(descriptions, item['idReadable']), 'w') as out:
                out.write(description)
        data.extend(temp_data)
        skip += top
    return data, statistics


def get_args():
    parser = argparse.ArgumentParser(
        description='Fetch kotlin front-end bugs.')
    parser.add_argument("output", help="File to save the bugs.")
    parser.add_argument(
        "descriptions", help="Directory to save files with descriptions")
    parser.add_argument(
        "statistics", help="File to save stats")
    return parser.parse_args()

def main():
    args = get_args()
    os.makedirs(args.descriptions, exist_ok=True)
    data, statistics = get_data(args.descriptions)
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
