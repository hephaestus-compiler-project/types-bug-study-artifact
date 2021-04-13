#! /usr/bin/env python3
import argparse
import statistics
import os
import json
from pprint import pprint


def get_args():
    parser = argparse.ArgumentParser(
        description='Compute stats for the test cases of the bugs.')
    parser.add_argument(
        "test_cases", help="Directory that contains the test cases of the bugs.")
    return parser.parse_args()


def get_stats(data):
    stats = {}
    for k in data.keys():
        stats[k] = {
            "max": max(data[k]),
            "min": min(data[k]),
            "mean": statistics.mean(data[k]),
            "median": int(statistics.median(data[k])),
            "sd": statistics.stdev(data[k])
        }
    return stats


def create_dict():
    return {"total": [], "java": [], "groovy": [], "kotlin": [], "scala": []}


def find_lang(string):
    if "java" in string:
        return "java"
    elif "groovy" in string:
        return "groovy"
    elif "kotlin" in string:
        return "kotlin"
    else:
        return "scala"


def main():
    declarations = create_dict()
    classes = create_dict()
    methods = create_dict()
    variables = create_dict()
    type_parameters = create_dict()
    calls = create_dict()
    locs = create_dict()
    args = get_args()
    for f in filter(lambda x: x[0].count("/") == 4, os.walk(args.test_cases)):
        lang = find_lang(f[0])
        stats_file = os.path.join(f[0], "stats_locs.json")
        with open(stats_file, 'r') as f:
            data = json.load(f)
            loc = int(data['loc'])
            data = data['declarations']
            decls = data['classes'] + data['methods/functions'] + \
                data['variables'] + data['type_parameters']
            calls_n = data['calls']
            declarations["total"].append(decls)
            declarations[lang].append(decls)
            classes["total"].append(data['classes'])
            classes[lang].append(data['classes'])
            methods["total"].append(data['methods/functions'])
            methods[lang].append(data['methods/functions'])
            variables["total"].append(data['variables'])
            variables[lang].append(data['variables'])
            type_parameters["total"].append(data['type_parameters'])
            type_parameters[lang].append(data['type_parameters'])
            calls["total"].append(calls_n)
            calls[lang].append(calls_n)
            locs["total"].append(loc)
            locs[lang].append(loc)
    classes_stats = get_stats(classes)
    methods_stats = get_stats(methods)
    variables_stats = get_stats(variables)
    type_parameters_stats = get_stats(type_parameters)
    declarations_stats = get_stats(declarations)
    calls_stats = get_stats(calls)
    locs_stats = get_stats(locs)
    print("Declarations")
    pprint(declarations_stats)
    print("Class Declarations")
    pprint(classes_stats)
    print("Method Declarations")
    pprint(methods_stats)
    print("Variables")
    pprint(variables_stats)
    print("Type Parameters")
    pprint(type_parameters_stats)
    print("Declarations")
    pprint(declarations_stats)
    print("Calls")
    pprint(calls_stats)
    print("Locs")
    pprint(locs_stats)


if __name__ == "__main__":
    main()
