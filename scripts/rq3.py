#! /usr/bin/env python3
import argparse
import statistics
import csv
import os
import json

from collections import defaultdict
from datetime import datetime

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


KEYWORDS = ["test", "Test"]
SOURCE_FILES = [".java", ".kt", ".scala", ".groovy"]

plt.style.use('ggplot')
sns.set(style="whitegrid")
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (8, 5)
plt.rcParams['axes.labelsize'] = 19
plt.rcParams['xtick.labelsize'] = 17
plt.rcParams['ytick.labelsize'] = 17
plt.rcParams['font.serif'] = 'DejaVu Sans'
plt.rcParams['font.monospace'] = 'Inconsolata Medium'
plt.rcParams['axes.labelweight'] = 'bold'


def get_args():
    parser = argparse.ArgumentParser(
        description='Compute stats for RQ3 (fixes and duration).')
    parser.add_argument(
        "diffs", help="Directory that contains the diffs of the bug fixes.")
    parser.add_argument(
        "stats", help="Directory that contains the stats for the bugs.")
    parser.add_argument(
        "--directory",
        help="Directory to save figures")
    parser.add_argument(
        "--all",
        help="Add lines for all languages in plots of fixes",
        action="store_true")
    parser.add_argument(
        "--print-all-points",
        help="Print numbers of all points in of figures",
        action="store_true")
    return parser.parse_args()


def print_stats(stats, title):
    def print_line(stats, row):
        row_format = "{:<10}" * 6
        print(row_format.format(
            row, stats["mean"], stats["median"],
            stats["sd"], stats["min"], stats["max"]
        ))
    header = ["", "Mean", "Median", "SD", "Min", "Max"]
    row_format = "{:<10}" * 6
    print("{:>30}".format(title))
    print((10 * 6) * "=")
    print(row_format.format(*header))
    print((10 * 6) * "-")
    print_line(stats["java"], "Java")
    print_line(stats["kotlin"], "Kotlin")
    print_line(stats["groovy"], "Groovy")
    print_line(stats["scala"], "Scala")
    print((10 * 6) * "-")
    print_line(stats["total"], "Total")
    print()


def get_fractions(x, total=320, print_all_points=False):
    x_dict = defaultdict(lambda: 0)
    for l in x:
        x_dict[l] += 1
    number_of_x = sorted(x_dict.keys())
    number_of_bugs = [x_dict[k] for k in number_of_x]
    x_fractions = [sum(number_of_bugs[:i]) / total
                   for i in range(1, len(number_of_bugs)+1)]
    if print_all_points:
        for fr, l in zip(x_fractions, number_of_x):
            print(l, fr)
    return number_of_x, x_fractions


def plot_fig(data, all_langs, directory, fig, print_all_points):
    def plot(duration, fractions, color, style='--'):
        line, = ax.plot(
            duration, fractions, marker=None, linestyle=style, c=color,
            linewidth=2.5
        )
        return line
    number, fractions = get_fractions(data["total"], 320, print_all_points)
    number_java, fractions_java = get_fractions(
        data["java"], 80, print_all_points)
    number_kotlin, fractions_kotlin = get_fractions(
        data["kotlin"], 80, print_all_points)
    number_groovy, fractions_groovy = get_fractions(
        data["groovy"], 80, print_all_points)
    number_scala, fractions_scala = get_fractions(
        data["scala"], 80, print_all_points)
    f, ax = plt.subplots()
    if fig == "duration":
        width = 3
    else:
        width = 3 if all_langs else 5
    total, = ax.plot(
        number,
        fractions,
        marker=None,
        linestyle="-", linewidth=width)
    if all_langs:
        java = plot(number_java, fractions_java, "#b07219")
        kotlin = plot(number_kotlin, fractions_kotlin, "#f18e33",
                      style=':')
        groovy = plot(number_groovy, fractions_groovy, "#e69f56",
                      style='-.')
        scala = plot(number_scala, fractions_scala, "#c22d40")
        ax.legend([total, java, kotlin, groovy, scala],
                  ["All", "javac", "kotlinc", "groovyc", "scalac & Dotty"],
                  loc="lower right")
    if fig == "lines":
        ax.scatter(5, 0.265625, c='blue')
        ax.annotate("(5, 0.27)", xy=(5.5, 0.25), xycoords='data',
                    xytext=(+20, -30), textcoords='offset points',
                    arrowprops=dict(arrowstyle="-", color='black'),
                    fontsize=16)
        ax.scatter(100, 0.890625, c='blue')
        ax.annotate("(100, 0.89)", xy=(110, 0.87), xycoords='data',
                    xytext=(+20, -30), textcoords='offset points',
                    arrowprops=dict(arrowstyle="-", color='black'),
                    fontsize=16)
    plt.xscale("log")
    if fig == "lines":
        ax.set_xticks([1, 3, 5, 10, 25, 50, 100, 200, 1000, 3000])
    elif fig == "files":
        ax.set_xticks([1, 2, 3, 4, 5, 10, 15, 45])
    else:
        ax.set_xticks([1, 10, 20, 30, 60, 180, 365, 730, 3000])
    ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
    plt.ylim([0, 1.0])
    if fig == "lines":
        plt.xlabel('Number of Lines of Code in a Fix')
    elif fig == "files":
        plt.xlabel('Number of Files in a Fix')
    else:
        plt.xlabel('Duration of Bugs in Days')
    plt.ylabel('Percentage of Bugs')
    if directory:
        filename = os.path.join(directory, fig + ".pdf")
    else:
        filename = fig + ".pdf"
    f.savefig(filename, bbox_inches='tight')


def create_dict():
    return {"total": [], "java": [], "groovy": [], "kotlin": [],
            "scala": []}


def get_lang(l):
    if "java" in l:
        return "java"
    if "groovy" in l:
        return "groovy"
    if "kotlin" in l:
        return "kotlin"
    return "scala"


def get_stats(data):
    res = {}
    for k in data.keys():
        res[k] = {
            "max": max(data[k]),
            "min": min(data[k]),
            "mean": int(statistics.mean(data[k])),
            "median": int(statistics.median(data[k])),
            "sd": int(statistics.stdev(data[k]))}
    return res


def compute_fixes(args):
    lines = create_dict()
    files = create_dict()
    for f in filter(lambda x: x[0].count("/") == 3, os.walk(args.diffs)):
        lang = get_lang(f[0])
        with open(os.path.join(f[0], "stats.csv")) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # skip column names: INSERTED,DELETED,MODIFIED,FILENAME
            next(csv_reader)
            fix_lines = 0
            fix_files = 0
            for row in csv_reader:
                if (any(x in row[3] for x in KEYWORDS) or
                        not any(x in row[3] for x in SOURCE_FILES)):
                    continue
                fix_files += 1
                fix_lines += int(row[0]) + int(row[1])
            lines["total"].append(fix_lines)
            files["total"].append(fix_files)
            lines[lang].append(fix_lines)
            files[lang].append(fix_files)
    lines_stats = create_dict()
    files_stats = create_dict()
    lines_stats = get_stats(lines)
    files_stats = get_stats(files)
    print_stats(lines_stats, "Lines")
    print_stats(files_stats, "Files")
    plot_fig(files, args.all, args.directory, "files",
             args.print_all_points)
    plot_fig(lines, args.all, args.directory, "lines",
             args.print_all_points)


def compute_duration(args):
    durations = create_dict()
    for l in ("groovy", "java", "kotlin", "scala"):
        filename = os.path.join(args.stats, l + ".json")
        with open(filename, 'r') as f:
            stats = json.load(f)
            for value in stats.values():
                try:
                    created = datetime.strptime(
                        value["created"], '%Y-%m-%d %H:%M:%S%z')
                    resolution = datetime.strptime(
                        value["resolution"], '%Y-%m-%d %H:%M:%S%z')
                except ValueError:
                    created = datetime.strptime(
                        value["created"], '%Y-%m-%d %H:%M:%S.%f')
                    resolution = datetime.strptime(
                        value["resolution"], '%Y-%m-%d %H:%M:%S.%f')
                duration = (resolution - created).days
                durations["total"].append(duration)
                durations[l].append(duration)
    duration_stats = get_stats(durations)
    print_stats(duration_stats, "Duration")
    plot_fig(durations, True, args.directory, "duration",
             args.print_all_points)


def main():
    args = get_args()
    compute_fixes(args)
    compute_duration(args)


if __name__ == "__main__":
    main()
