#! /usr/bin/env python3
import argparse
import statistics
import csv
import json
import os

def get_args():
    parser = argparse.ArgumentParser(
        description='Copy stats for the bugs in iterations')
    parser.add_argument(
        "iterations",
        help="Directory that contains the iterations.")
    parser.add_argument(
        "downloads",
        help="Directory with JSONs that contains the stats")
    parser.add_argument(
        "output",
        help="Directory to save the results")
    return parser.parse_args()


def load_json(directory, filename):
    json_filename = os.path.join(directory, filename)
    with open(json_filename, 'r') as f:
        return json.load(f)


def save_json(directory, filename, data):
    json_filename = os.path.join(directory, filename)
    with open(json_filename, 'w') as f:
        return json.dump(data, f, indent=4)


def main():
    args = get_args()
    java_res = {}
    kotlin_res = {}
    groovy_res = {}
    scala_res = {}
    java_data = load_json(args.downloads, "java.json")
    kotlin_data = load_json(args.downloads, "kotlin.json")
    groovy_data = load_json(args.downloads, "groovy.json")
    scala_data = load_json(args.downloads, "scala.json")
    for d in list(os.walk(args.iterations))[1:]:
        for l in d[2]:
            lang_txt = os.path.join(d[0], l)
            with open(lang_txt, 'r') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    if l == "scala.txt":
                        prefix = 'scala' if 'scala' in row[0] else 'dotty'
                        bug_id = prefix + '-' + row[0].split('/')[-1]
                        scala_res[bug_id] = scala_data[bug_id]
                    else:
                        bug_id = row[0].split('/')[-1]
                        if l == "java.txt":
                            java_res[bug_id] = java_data[bug_id]
                        elif l == "kotlin.txt":
                            kotlin_res[bug_id] = kotlin_data[bug_id]
                        else:
                            groovy_res[bug_id] = groovy_data[bug_id]
    save_json(args.output, "java.json", java_res)
    save_json(args.output, "kotlin.json", kotlin_res)
    save_json(args.output, "groovy.json", groovy_res)
    save_json(args.output, "scala.json", scala_res)


if __name__ == "__main__":
    main()
