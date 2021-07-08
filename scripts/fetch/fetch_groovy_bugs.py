"""Fetch groovy bugs.
"""
import argparse
import requests
import os
import json
from datetime import datetime


def get_data(descriptions):
    data = []
    start_at = 0
    max_results = 50
    total = 0
    temp_data = []
    statistics = {}
    first = True
    while start_at < total or first:
        first = False
        base = "https://issues.apache.org/jira/rest/api/latest/search"
        search_terms = [
            "project = Groovy",
            "AND type = bug",
            "AND resolution = fixed",
            "AND status in (Resolved, Closed)",
            "AND component = \"Static Type Checker\""
        ]
        query = "%20".join(map(lambda x: x.replace(" ", "%20"), search_terms))
        fields = "key,description"
        fields = "key,description,resolutiondate,created,reporter,assignee"
        url = "{base}?jql={query}&fields={fields}&startAt={s}&maxResults={m}"
        url = url.format(
            base=base,
            query=query,
            fields=fields,
            s=start_at,
            m=max_results
        )
        response = requests.get(url).json()
        total = response['total']
        groovy_jira_url = "https://issues.apache.org/jira/browse/"
        temp_data = []
        for item in response['issues']:
            created = datetime.strptime(
                item['fields']['created'], "%Y-%m-%dT%H:%M:%S.%f%z")
            resolution = datetime.strptime(
                item['fields']['resolutiondate'], "%Y-%m-%dT%H:%M:%S.%f%z")
            passed = resolution - created
            reporter = item['fields']['reporter']['name']
            if item['fields'].get('assignee'):
                assignee = item['fields']['assignee']['name']
            else:
                assignee = ""
            stats = {
                "created": str(created),
                "resolution": str(resolution),
                "passed": str(passed),
                "comments": None,
                "reporter": reporter,
                "assignee": assignee,
                "reporter_is_assigned": reporter == assignee
            }
            statistics[item['key']] = stats
            temp_data.append(groovy_jira_url + item['key'])
            description = item['fields']['description']
            with open(os.path.join(descriptions, item['key']), 'w') as out:
                out.write(description)
        data.extend(temp_data)
        start_at += max_results
    return data, statistics


def get_args():
    parser = argparse.ArgumentParser(
        description='Fetch groovy front-end bugs.')
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
