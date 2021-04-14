#! /usr/bin/env python3
import argparse
import os
import csv
import json
from datetime import datetime
from collections import defaultdict


def boostrap():
    return {
        "total": defaultdict(lambda: []),
        "java": defaultdict(lambda: []),
        "kotlin": defaultdict(lambda: []),
        "groovy": defaultdict(lambda: []),
        "scala": defaultdict(lambda: [])
    }


DURATION = boostrap()
LINES = boostrap()
FILES = boostrap()
ROOT_CAUSES = boostrap()
CHARACTERISTICS = boostrap()
CHARACTERISTICS_CATEGORIES = boostrap()
CATEGORIES = boostrap()
SYMPTOMS = boostrap()
KEYWORDS=["test", "Test"]
SOURCE_FILES=[".java", ".kt", ".scala", ".groovy"]


def get_args():
    parser = argparse.ArgumentParser(
        description='Lift correlations')
    parser.add_argument(
        "bugs",
        help="File with the bugs")
    parser.add_argument(
        "stats", help="Directory that contains the stats for the bugs.")
    parser.add_argument(
        "diffs", help="Directory that contains the diffs of the bug fixes.")
    parser.add_argument("--threshold", type=float,
                        default=5,
                        help="Threshold for lift.")
    parser.add_argument("--ithreshold", type=int,
                        default=10,
                        help="Intersections threshold for lift.")
    parser.add_argument("--limit", type=int,
                        default=5,
                        help="Max entries to show per pair.")
    parser.add_argument("--all", action='store_true',
                        help="Print lift score for all categories")
    return parser.parse_args()


def files_lookup(files):
    if files == 1:
        return "1"
    if files <= 3:
        return "2-3"
    if files <= 5:
        return "3-5"
    return "5+"


def lines_lookup(lines):
    if lines <= 3:
        return "0-3"
    if lines <= 10:
        return "3-10"
    if lines <= 25:
        return "10-25"
    if lines <= 100:
        return "25-100"
    return "100+"


def duration_lookup(duration):
    if duration <= 7:
        return "0-7"
    if duration <= 60:
        return "7-60"
    if duration <= 365:
        return "60-365"
    return "365+"


def read_data(args):
    with open(args.bugs) as jf:
        bugs = json.load(jf)
    for l in ("groovy", "java", "kotlin", "scala"):
        with open(os.path.join(args.stats, l + ".json")) as jf:
            stats = json.load(jf)
            for bug, values in stats.items():
                # Duration
                created = stats[bug]["created"]
                resolution = stats[bug]["resolution"]
                try:
                    created = datetime.strptime(
                        created, '%Y-%m-%d %H:%M:%S%z')
                    resolution = datetime.strptime(
                        resolution, '%Y-%m-%d %H:%M:%S%z')
                except ValueError:
                    created = datetime.strptime(
                        created, '%Y-%m-%d %H:%M:%S.%f')
                    resolution = datetime.strptime(
                        resolution, '%Y-%m-%d %H:%M:%S.%f')
                duration = (resolution - created).days
                cluster = duration_lookup(duration)
                # Lines - Files
                diffstats = os.path.join(args.diffs, l, bug, "stats.csv")
                try:
                    with open(diffstats) as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        # skip column names: INSERTED,DELETED,MODIFIED,FILENAME
                        next(csv_reader)
                        fix_lines = 0
                        fix_files = 0
                        for row in csv_reader:
                            if (any(x in row[3] for x in KEYWORDS) or
                                    not any(x in row[3]
                                    for x in SOURCE_FILES)):
                                continue
                            fix_files += 1
                            fix_lines += int(row[0]) + int(row[1])
                        lines_cluster = lines_lookup(fix_lines)
                        files_cluster = files_lookup(fix_files)
                except FileNotFoundError:
                    print("Warning {} not found (file)".format(bug))
                    continue
                bug = bug.replace('dotty', 'Dotty').replace('scala', 'Scala2')
                try:
                    DURATION["total"][cluster].append(bug)
                    DURATION[l][cluster].append(bug)
                    LINES["total"][lines_cluster].append(bug)
                    LINES[l][lines_cluster].append(bug)
                    FILES["total"][files_cluster].append(bug)
                    FILES[l][files_cluster].append(bug)
                    root_cause = bugs[bug]['root_cause']['category']
                    ROOT_CAUSES["total"][root_cause].append(bug)
                    ROOT_CAUSES[l][root_cause].append(bug)
                    category = bugs[bug]['pattern']['category']
                    CATEGORIES["total"][category].append(bug)
                    CATEGORIES[l][category].append(bug)
                    symptom = bugs[bug]['symptom']
                    SYMPTOMS["total"][symptom].append(bug)
                    SYMPTOMS[l][symptom].append(bug)
                    chars = bugs[bug]['chars']['characteristics']
                    char_categories = bugs[bug]['chars']['categories']
                    for char in chars:
                        CHARACTERISTICS["total"][char].append(bug)
                        CHARACTERISTICS[l][char].append(bug)
                    for cat in char_categories:
                        CHARACTERISTICS_CATEGORIES["total"][cat].append(bug)
                        CHARACTERISTICS_CATEGORIES[l][cat].append(bug)
                except KeyError:
                    print("Cannot find {}".format(bug))


def compute(keyword, a, b, threshold=False, ithreshold=False, limit=None):
    """https://stackabuse.com/association-rule-mining-via-apriori-algorithm-in-python/
    """
    size = sum(len(i) for i in a["total"].values())
    # Support B
    support_b = defaultdict(lambda: [])
    for k, v in b[keyword].items():
        support_b[k] = len(v) / size
    # Confidence A->B
    confidence_a_b = defaultdict(lambda: [])
    for a_name, a_value in a[keyword].items():
        for b_name, b_value in b[keyword].items():
            key = a_name + "->" + b_name
            confidence = len(set(a_value) & set(b_value)) / len(a_value)
            confidence_a_b[key] = confidence
    # Lift A->B
    lift_a_b = defaultdict(lambda: [])
    max_a = max(len(i.split("->")[0]) for i in confidence_a_b.keys())
    max_b = max(len(i.split("->")[1]) for i in confidence_a_b.keys())
    res = []
    for key, confidence in confidence_a_b.items():
        b_key = key.split("->")[-1]
        lift = confidence / support_b[b_key]
        lift_a_b[key] = lift
        # Print Result
        a_key = key.split("->")[0]
        intersection = len(set(a[keyword][a_key]) & set(b[keyword][b_key]))
        if threshold and lift < threshold:
            continue
        if ithreshold and intersection < ithreshold:
            continue
        if a_key == b_key:
            continue
        res.append((a_key, b_key, lift, confidence, support_b[b_key],
                    len(a[keyword][a_key]), len(b[keyword][b_key]),
                    intersection, max_a, max_b))
    res.sort(reverse=True, key=lambda x: x[2])
    res = res[:limit] if limit else res
    for r in res:
        print(("Lift {:>{x}} -> {:<{y}}: {:.4f} (Confidence A->B: {:.4f}, "
               "Support B: {:.4f}) -- Totals A: {}, B: {}, A-B: {}").format(
                r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7],
                intersection,
                x=r[8], y=r[9]))


def main():
    args = get_args()
    read_data(args)
    if args.all:
        print("Duration -> Lines")
        compute("total", DURATION, LINES, args.threshold, args.ithreshold,
                args.limit)
        print("Lines -> Duration")
        compute("total", LINES, DURATION, args.threshold, args.ithreshold,
                args.limit)
        print("Root cause -> Duration")
        compute("total", ROOT_CAUSES, DURATION, args.threshold,
                args.ithreshold, args.limit)
        print("Root cause -> Lines")
        compute("total", ROOT_CAUSES, LINES, args.threshold, args.ithreshold,
                args.limit)
        print("Root cause -> FILES")
        compute("total", ROOT_CAUSES, FILES, args.threshold, args.ithreshold,
                args.limit)
        print("Characteristics -> Characteristics")
        compute("total", CHARACTERISTICS, CHARACTERISTICS, args.threshold,
                args.ithreshold, args.limit)
        print("Char Categories -> Char Categories")
        compute("total", CHARACTERISTICS_CATEGORIES,
                CHARACTERISTICS_CATEGORIES, args.threshold, args.ithreshold,
                args.limit)
        print("Symptom -> Characteristics")
        compute("total", SYMPTOMS, CHARACTERISTICS, args.threshold,
                args.ithreshold, args.limit)
        print("Category -> Root Cause")
        compute("total", CATEGORIES, ROOT_CAUSES, args.threshold,
                args.ithreshold, args.limit)
    else:
        print("Char Categories -> Char Categories")
        compute("total", CHARACTERISTICS_CATEGORIES,
                CHARACTERISTICS_CATEGORIES, args.threshold,
                args.ithreshold, args.limit)
        print("Characteristics -> Characteristics")
        compute("total", CHARACTERISTICS, CHARACTERISTICS, args.threshold,
                args.ithreshold, args.limit)


if __name__ == "__main__":
    main()
