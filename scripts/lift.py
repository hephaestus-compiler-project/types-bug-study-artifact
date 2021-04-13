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
        "iterations",
        help="Directory that contains the iterations.")
    parser.add_argument(
        "bugs",
        help="Directory that contains bugs.")
    parser.add_argument(
        "diffs", help="Directory that contains the diffs of the bug fixes.")
    parser.add_argument("--threshold", type=float, help="Threshold for lift.")
    parser.add_argument("--ithreshold", type=int,
                        help="Intersections threshold for lift.")
    parser.add_argument("--root-causes", help="JSON with root causes")
    parser.add_argument("--characteristics", help="JSON with characteristics")
    parser.add_argument("--symptoms", help="JSON with symptoms")
    parser.add_argument("--categories", help="JSON with categories")
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
    root_causes = {}
    if args.root_causes:
        with open(args.root_causes, 'r') as fp:
            root_causes = json.load(fp)
    characteristics = {}
    if args.characteristics:
        with open(args.characteristics, 'r') as fp:
            characteristics = json.load(fp)
    symptoms = {}
    if args.symptoms:
        with open(args.symptoms, 'r') as fp:
            symptoms = json.load(fp)
    categories = {}
    if args.categories:
        with open(args.categories, 'r') as fp:
            categories = json.load(fp)
    for d in list(os.walk(args.iterations))[1:]:
        if "4" in d[0]:
            continue
        for f in d[2]:
            filename = os.path.join(d[0], f)
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    lang = ""
                    bug = ""
                    if "JDK" in row[0]:
                        lang = "java"
                        bug = row[0].split("/")[-1]
                    elif "GROOVY" in row[0]:
                        lang = "groovy"
                        bug = row[0].split("/")[-1]
                    elif "KT" in row[0]:
                        lang = "kotlin"
                        bug = row[0].split("/")[-1]
                    elif "scala" in row[0]:
                        lang = "scala"
                        bug = "scala-" + row[0].split("/")[-1]
                    elif "dotty" in row[0]:
                        lang = "scala"
                        bug = "dotty-" + row[0].split("/")[-1]
                    with open(os.path.join(args.bugs, lang + ".json")) as jf:
                        stats = json.load(jf)
                    # Duration
                    try:
                        created = stats[bug]["created"]
                        resolution = stats[bug]["resolution"]
                    except KeyError:
                        print("Warning {} not found (duration)".format(bug))
                        continue
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
                    diffstats = os.path.join(args.diffs, lang, bug, "stats.csv")
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
                    DURATION["total"][cluster].append(bug)
                    DURATION[lang][cluster].append(bug)
                    LINES["total"][lines_cluster].append(bug)
                    LINES[lang][lines_cluster].append(bug)
                    FILES["total"][files_cluster].append(bug)
                    FILES[lang][files_cluster].append(bug)
                    if args.root_causes:
                        try:
                            root_cause = root_causes[bug][0]
                            ROOT_CAUSES["total"][root_cause].append(bug)
                            ROOT_CAUSES[lang][root_cause].append(bug)
                        except KeyError:
                            print("Warning {} not found (root_cause)".format(
                                bug))
                            continue
                    if args.categories:
                        try:
                            category = categories[bug][0]
                            CATEGORIES["total"][category].append(bug)
                            CATEGORIES[lang][category].append(bug)
                        except KeyError:
                            print("Warning {} not found (category)".format(
                                bug))
                            continue
                    if args.symptoms:
                        try:
                            symptom = symptoms[bug][0]
                            SYMPTOMS["total"][symptom].append(bug)
                            SYMPTOMS[lang][symptom].append(bug)
                        except KeyError:
                            print("Warning {} not found (symptom)".format(
                                bug))
                            continue
                    if args.characteristics:
                        try:
                            chars = characteristics[bug]["characteristics"]
                            char_categories = characteristics[bug]["categories"]
                            for char in chars:
                                CHARACTERISTICS["total"][char].append(bug)
                                CHARACTERISTICS[lang][char].append(bug)
                            for cat in char_categories:
                                CHARACTERISTICS_CATEGORIES["total"][cat].append(bug)
                                CHARACTERISTICS_CATEGORIES[lang][cat].append(bug)
                        except KeyError:
                            print("Warning {} not found (char)".format(
                                bug))
                            continue


def compute(keyword, a, b, threshold=False, ithreshold=False):
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
        print(("Lift {:>{x}} -> {:<{y}}: {:.4f} (Confidence A->B: {:.4f}, "
               "Support B: {:.4f}) -- Totals A: {}, B: {}, A-B: {}").format(
                a_key, b_key, lift, confidence, support_b[b_key],
                len(a[keyword][a_key]), len(b[keyword][b_key]),
                intersection,
                x=max_a, y=max_b))


def main():
    args = get_args()
    read_data(args)
    print("Duration -> Lines")
    compute("total", DURATION, LINES, args.threshold, args.ithreshold)
    print("Lines -> Duration")
    compute("total", LINES, DURATION, args.threshold, args.ithreshold)
    if args.root_causes:
        print("Root cause -> Duration")
        compute("total", ROOT_CAUSES, DURATION, args.threshold, args.ithreshold)
        print("Root cause -> Lines")
        compute("total", ROOT_CAUSES, LINES, args.threshold, args.ithreshold)
        print("Root cause -> FILES")
        compute("total", ROOT_CAUSES, FILES, args.threshold, args.ithreshold)
    if args.characteristics:
        print("Characteristics -> Characteristics")
        compute("total", CHARACTERISTICS, CHARACTERISTICS, args.threshold,
                args.ithreshold)
        print("Char Categories -> Char Categories")
        compute("total", CHARACTERISTICS_CATEGORIES,
                CHARACTERISTICS_CATEGORIES, args.threshold, args.ithreshold)
    if args.characteristics and args.symptoms:
        print("Symptom -> Characteristics")
        compute("total", SYMPTOMS, CHARACTERISTICS, args.threshold,
                args.ithreshold)
    if args.root_causes and args.categories:
        print("Category -> Root Cause")
        compute("total", CATEGORIES, ROOT_CAUSES, args.threshold, args.ithreshold)


if __name__ == "__main__":
    main()
