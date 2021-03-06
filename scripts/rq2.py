#! /usr/bin/env python3
import argparse
import json

from collections import defaultdict, OrderedDict

import matplotlib.pylab as plt
import seaborn as sns
import pandas as pd


LANG2COMP = {
    'Groovy': 'groovyc',
    'Java': 'javac',
    'Kotlin': 'kotlinc',
    'Scala': 'scalac & Dotty'
}


def get_args():
    parser = argparse.ArgumentParser(
        description='Generate patterns figure.')
    parser.add_argument("data", help="JSON with bugs.")
    parser.add_argument(
            "--patterns",
            default="patterns.pdf",
            help="Filename to save the symptoms figure.")
    parser.add_argument(
            "--patterns-symptoms",
            default="patterns_symptoms.pdf",
            help="Filename to save the patterns symptoms figure.")
    return parser.parse_args()


def construct_dataframes(bugs):
    data_lang = defaultdict(lambda: 0)
    data_symptoms = defaultdict(lambda: 0)
    for bug in bugs.values():
        data_lang[(LANG2COMP[bug['language']], bug['bug_cause']['category'])] += 1
        data_symptoms[(bug['symptom'], bug['bug_cause']['category'])] += 1
    framedata_langs = []
    for (comp, category), value in data_lang.items():
        framedata_langs.append({
            "Bug Cause": category,
            "Compiler": comp,
            "Number of bugs": value
        })
    framedata_symptoms = []
    for (symptom, category), value in data_symptoms.items():
        framedata_symptoms.append({
            "Bug Cause": category,
            "Symptom": symptom,
            "Number of bugs": value
        })
    return (
        pd.DataFrame(framedata_langs),
        pd.DataFrame(framedata_symptoms),
        data_lang,
        data_symptoms
    )


def plot_fig(df, data, color_map, categories, output):
    plt.style.use('ggplot')
    sns.set(style="whitegrid")
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['figure.figsize'] = (9, 2.5 if len(color_map) == 4 else 3.5)
    plt.rcParams['axes.labelsize'] = 17
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['font.serif'] = 'DejaVu Sans'
    plt.rcParams['font.monospace'] = 'Inconsolata Medium'
    plt.rcParams['legend.fontsize'] = 12 if len(color_map) == 4 else 10
    plt.rcParams['axes.labelweight'] = 'bold'
    ax = df.plot.barh(width=0.3,
                      color=[color_map[c] for c in df.columns],
                      stacked=True)

    sums = []
    for c in categories:
        v = sum(data[(k, c)] for k in color_map.keys())
        sums.append(v)

    start_index = (len(color_map) - 1) * 5
    for i, p in enumerate(ax.patches[start_index:]):
        ax.annotate("{} / 320".format(int(sums[i])),
                    (p.get_x() + p.get_width(), p.get_y()),
                    xytext=(5, 10), textcoords='offset points')
    ax.set_ylabel('')
    patches, labels = ax.get_legend_handles_labels()
    plt.savefig(output, format='pdf', bbox_inches='tight',
                pad_inches=0)


def get_row(df, pattern, dimension, lim):
    total = 0
    res = [pattern]
    for lang in dimension:
        n = int(df[lang][pattern])
        total += n
        res.append("{} ({:.2f}%)".format(
           n, (n/lim) * 100
        ))
    res.append("{} ({:.2f}%)".format(
       total, (total/320) * 100
    ))
    return res


def print_stats(df, dimension, lim, trim_dimensions=False):
    df = df.fillna(0)
    row1 = get_row(df, 'Type-related Bugs', dimension, lim)
    row2 = get_row(df, 'Semantic Analysis Bugs', dimension, lim)
    row3 = get_row(df, 'Resolution Bugs', dimension, lim)
    row4 = get_row(df, 'Bugs Related to Error Handling & Reporting', dimension,
                   lim)
    row5 = get_row(df, 'AST Transformation Bugs', dimension, lim)
    if trim_dimensions:
        dimension = [d.split(' ')[0] for d in dimension]
    header = ["Bug Cause"] + dimension + ["Total"]
    spaces = "{:>" + str(len(max(header, key=len)) + 5) + "}"
    columns = len(dimension) + 1
    header_format = "{:<33}" + spaces * columns
    row_format = "{:<33}" + spaces * columns
    print(header_format.format(*header))
    print((33 + (len(max(header, key=len)) + 5) * columns) * "-")
    print(row_format.format(*row1))
    print(row_format.format(*row2))
    print(row_format.format(*row3))
    row4[0] = 'Error Handling & Reporting'
    print(row_format.format(*row4))
    print(row_format.format(*row5))


def main():
    args = get_args()
    with open(args.data, 'r') as f:
        json_data = json.load(f)
    df_l, df_s, data_l, data_s = construct_dataframes(json_data)
    df_l = df_l.groupby(
        ['Compiler', 'Bug Cause'])['Number of bugs'].sum().unstack('Compiler')
    df_s = df_s.groupby(
        ['Symptom', 'Bug Cause'])['Number of bugs'].sum().unstack('Symptom')
    categories = [
        'AST Transformation Bugs',
        'Bugs Related to Error Handling & Reporting',
        'Resolution Bugs',
        'Semantic Analysis Bugs',
        'Type-related Bugs',
    ]
    df_l, df_s = df_l.reindex(categories), df_s.reindex(categories)
    compilers = ["groovyc", "javac", "kotlinc", "scalac & Dotty"]
    print_stats(df_l, compilers, 80)
    print()
    symptoms = ['Unexpected Compile-Time Error',
                'Internal Compiler Error',
                'Unexpected Runtime Behavior',
                'Misleading Report',
                'Compilation Performance Issue']
    print_stats(df_s, symptoms, 320, True)
    langs = OrderedDict([
        ('groovyc', '#e69f56'),
        ('javac', '#b07219'),
        ('kotlinc', '#f18e33'),
        ('scalac & Dotty', '#c22d40')
    ])
    plot_fig(df_l, data_l, langs, categories, args.patterns)
    symptoms = OrderedDict([
        ('Unexpected Compile-Time Error', '#336600'),
        ('Internal Compiler Error', '#b07219'),
        ('Unexpected Runtime Behavior', '#c22d40'),
        ('Misleading Report', '#f18e33'),
        ('Compilation Performance Issue', '#666699')
    ])
    df_s = df_s.reindex(symptoms.keys(), axis=1)
    plot_fig(df_s, data_s, symptoms, categories, args.patterns_symptoms)


if __name__ == "__main__":
    main()
