#! /usr/bin/env python3
import argparse
import json
import statistics
import os

from collections import defaultdict

import matplotlib.pylab as plt
import matplotlib.offsetbox as offsetbox
import seaborn as sns
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(
        description='Generate figures and tables of RQ4 (characteristics).')
    parser.add_argument("characteristics", help="JSON with characteristics.")
    parser.add_argument("bugs", help="JSON with bugs.")
    parser.add_argument(
        "test_cases",
        help="Directory that contains the test cases of the bugs.")
    parser.add_argument(
            "--output",
            default="characteristics.pdf",
            help="Filename to save the figure.")
    parser.add_argument(
            "--all",
            action="store_true",
            help="Print table with all characteristics")
    parser.add_argument(
            "--frequency",
            type=int,
            default=5,
            help="Number of most/least frequent characteristics (default: 5)")
    parser.add_argument(
            "--most",
            type=int,
            default=5,
            help="Number of most frequent characteristics per language (default: 5)")
    return parser.parse_args()


def construct_dataframe(data):
    characteristics = []
    dataframes = {}
    for key, value in data.items():
        framedata = []
        for subkey, subvalue in value['subcategories'].items():
            framedata.append({
                'Characteristic': subkey,
                'Bug prevalence': 100 * (int(subvalue['total']) / 320),
            })
            if 'is_common' not in subvalue:
                print(subkey)
            if subvalue['is_common']:
                characteristics.append((subkey, subvalue['is_common'],
                                        100 * (int(subvalue['total']) / 320)))
        framedata = sorted(framedata, key=lambda k: k['Bug prevalence'],
                           reverse=True)[:4]
        percentage = str(round((int(value['total']) / 320) * 100, 2))
        dataframes[key + " (" + percentage + "%)"] = pd.DataFrame(framedata)
    return dataframes, characteristics


def plot_fig(dataframes, output):
    plt.style.use('ggplot')
    sns.set(style="whitegrid")
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['figure.figsize'] = (8, 4.5)
    plt.rcParams['axes.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 6.8
    plt.rcParams['xtick.labelsize'] = 6
    plt.rcParams['font.serif'] = 'DejaVu Sans'
    plt.rcParams['font.monospace'] = 'Inconsolata Medium'
    plt.rcParams['axes.labelweight'] = 'bold'

    fig, axs = plt.subplots(nrows=8, sharex=True)

    for i, (key, dataframe) in enumerate(dataframes.items()):
        dataframe = dataframe.sort_values(
            'Bug prevalence', ascending=True)
        dataframe.plot.barh(x='Characteristic', y='Bug prevalence',
                            color='grey', ax=axs[i])
        ob = offsetbox.AnchoredText(key, loc=1,
                                    prop=dict(color='black', fontsize=7))
        ob.patch.set(boxstyle='round', color='lightgrey', alpha=1)
        axs[i].add_artist(ob)
        axs[i].set_ylabel('')
        axs[i].set_xlabel('Bug prevalence (%)')
        axs[i].get_legend().remove()
        axs[i].set_xlim([0, 70])
        for line in axs[i].get_xgridlines():
            line.set_linewidth(0.3)
        for line in axs[i].get_ygridlines():
            line.set_linewidth(0.3)
        [i.set_linewidth(0.3) for i in axs[i].spines.values()]
    plt.savefig(output, format='pdf', bbox_inches='tight',
                pad_inches=0)


def print_table(data):
    res = []
    for category, values in data.items():
        for subcategory, cat_values in values['subcategories'].items():
            res.append((subcategory, category, cat_values['total'],
                        cat_values['is_common']))
            for subsubcat, total in cat_values['subcategories'].items():
                if subsubcat == "is_common":
                    continue
                res.append((subsubcat, category, total, True))
    res = sorted(res, key=lambda x: (x[1], -x[2]))
    print("\\begin{tabular}{l l l c c}")
    print("\\hline")
    print("{\\bf Feature} & {\\bf Category} & {\\bf Total} & {\\bf Common} \\\\")
    print("\\hline")
    for row in res:
        print("{} & {} & {} & {}\\\\".format(
            row[0], row[1], row[2], row[3]
        ))
    print("\\hline")
    print("\\end{tabular}")


def print_generic_stats_table(compilable, non_compilable, locs, classes,
                              methods, calls):
    print("General statistics on test case characteristics")
    row_format = "{:<33}" + "{:>30}"
    print(63 * "=")
    print(row_format.format(
        "Compilable test cases",
        "{} / 320 ({:.2f}%)".format(compilable, (compilable / 320) * 100)))
    print(row_format.format(
        "Non-compilable test cases",
        "{} / 320 ({:.2f}%)".format(
            non_compilable, (non_compilable / 320) * 100)))
    print(63 * "-")
    print(row_format.format("LoC (mean)", "{:.2f}".format(locs["mean"])))
    print(row_format.format("LoC (median)", locs["median"]))
    print(63 * "-")
    print(row_format.format(
        "Number of class decls (mean)", "{:.2f}".format(classes["mean"])))
    print(row_format.format(
        "Number of class decls (median)", classes["median"]))
    print(63 * "-")
    print(row_format.format(
        "Number of method decls (mean)", "{:.2f}".format(methods["mean"])))
    print(row_format.format(
        "Number of method decls (median)", methods["median"]))
    print(row_format.format(
        "Number of method calls (mean)", "{:.2f}".format(calls["mean"])))
    print(row_format.format(
        "Number of method calls (median)", calls["median"]))
    print(63 * "-")
    print()


def print_most_least_chars_table(characteristics, limit):
    row_format = "{:<33}" + "{:>30}"
    print("Most frequent features")
    print(63 * "=")
    most = characteristics[-limit:]
    most.sort(reverse=True, key=lambda x: x[2])
    for char in most:
        print(row_format.format(char[0], "{:.2f}%".format(char[2])))
    print()
    print("Least frequent features")
    print(63 * "=")
    least = characteristics[:limit]
    least.sort(reverse=True, key=lambda x: x[2])
    for char in least:
        print(row_format.format(char[0], "{:.2f}%".format(char[2])))
    print()


def print_most_per_lang(data, limit):
    row_format = ("{:<30}" + "{:>7}") * 4
    print("Most bug-triggering features per language")
    print(155 * "=")
    data = list(zip(data.items()))
    lang1 = data[0][0][1]
    lang1_name = data[0][0][0]
    lang1.sort(reverse=True, key=lambda x: x[1])
    lang2 = data[1][0][1]
    lang2_name = data[1][0][0]
    lang2.sort(reverse=True, key=lambda x: x[1])
    lang3 = data[2][0][1]
    lang3_name = data[2][0][0]
    lang3.sort(reverse=True, key=lambda x: x[1])
    lang4 = data[3][0][1]
    lang4_name = data[3][0][0]
    lang4.sort(reverse=True, key=lambda x: x[1])
    print("{}{}{}{}".format(
        lang1_name.center(38), lang2_name.center(38),
        lang3_name.center(38), lang4_name.center(38)
    ))
    print(155 * "-")
    for i, _ in enumerate(lang1[:limit]):
        print(row_format.format(
            lang1[i][0], "{:.2f}% | ".format(lang1[i][1]),
            lang2[i][0], "{:.2f}% | ".format(lang2[i][1]),
            lang3[i][0], "{:.2f}% | ".format(lang3[i][1]),
            lang4[i][0], "{:.2f}% | ".format(lang4[i][1])
        ))
    print()


def print_categories_stats(categories):
    row_format = "{:<33}" + "{:>7}"
    print("Most frequent characteristic categories")
    print(40 * "=")
    for row in categories:
        print(row_format.format(row[0], "{:.2f}%".format(row[1])))
    print()


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


def get_compilable_non_compilable(json_bugs):
    compilable = sum(1 for v in json_bugs.values() if v['is_correct'])
    non_compilable = sum(1 for v in json_bugs.values() if not v['is_correct'])
    return compilable, non_compilable


def compute_test_cases_stats(test_cases):
    locs = create_dict()
    classes = create_dict()
    methods = create_dict()
    calls = create_dict()
    for f in filter(lambda x: x[0].count("/") == 3, os.walk(test_cases)):
        lang = find_lang(f[0])
        stats_file = os.path.join(f[0], "stats_locs.json")
        with open(stats_file, 'r') as f:
            data = json.load(f)
            loc = int(data['loc'])
            data = data['declarations']
            calls_n = data['calls']
            classes["total"].append(data['classes'])
            classes[lang].append(data['classes'])
            methods["total"].append(data['methods/functions'])
            methods[lang].append(data['methods/functions'])
            calls["total"].append(calls_n)
            calls[lang].append(calls_n)
            locs["total"].append(loc)
            locs[lang].append(loc)
    locs_stats = get_stats(locs)
    classes_stats = get_stats(classes)
    methods_stats = get_stats(methods)
    calls_stats = get_stats(calls)
    return locs_stats, classes_stats, methods_stats, calls_stats


def compute_chars_per_lang(bugs):
    chars = {
        "Java": defaultdict(lambda: 0),
        "Groovy": defaultdict(lambda: 0),
        "Kotlin": defaultdict(lambda: 0),
        "Scala": defaultdict(lambda: 0)
    }
    stats = {
        "Java": [],
        "Groovy": [],
        "Kotlin": [],
        "Scala": []
    }
    for values in bugs.values():
        for char in values["chars"]["characteristics"]:
            chars[values["language"]][char] += 1
    for lang, characteristics in chars.items():
        for c, total in characteristics.items():
            stats[lang].append((c, (total/80.0) * 100))
    return stats


def get_categories_stats(chars):
    res = [(category, (values['total'] / 320) * 100)
           for category, values in chars['Bug Causes'].items()]
    res.sort(reverse=True, key=lambda x: x[1])
    return res


def main():
    args = get_args()
    with open(args.bugs, 'r') as f:
        json_bugs = json.load(f)
    with open(args.characteristics, 'r') as f:
        json_chars = json.load(f)

    compilable, non_compilable = get_compilable_non_compilable(json_bugs)
    locs, classes, methods, calls = compute_test_cases_stats(args.test_cases)
    stats_per_lang = compute_chars_per_lang(json_bugs)
    categories = get_categories_stats(json_chars)

    dataframes, characteristics = construct_dataframe(json_chars['Bug Causes'])
    characteristics = sorted(characteristics, key=lambda tup: tup[2])

    print_generic_stats_table(compilable, non_compilable,
                              locs['total'], classes['total'],
                              methods['total'], calls['total'])
    print_most_least_chars_table(characteristics, args.frequency)
    print_most_per_lang(stats_per_lang, args.most)
    print_categories_stats(categories)

    plot_fig(dataframes, args.output)

    if args.all:
        print_table(json_chars['Bug Causes'])


if __name__ == "__main__":
    main()
