#! /usr/bin/env python3
import argparse
import json

from collections import defaultdict

import matplotlib.pylab as plt
import seaborn as sns
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(
        description='Compute stats and produce figure for RQ 1 (symptoms).'
    )
    parser.add_argument("data", help="JSON with bugs.")
    parser.add_argument(
            "--output",
            default="symptoms.pdf",
            help="Filename to save the figure."
    )
    return parser.parse_args()


def construct_dataframe(bugs):
    data = defaultdict(lambda: 0)
    for bug in bugs.values():
        data[(bug['language'], bug['symptom'])] += 1
    framedata = []
    for (lang, symptom), value in data.items():
        framedata.append({
            "Symptom": symptom,
            "Language": lang,
            "Number of bugs": value
        })
    return pd.DataFrame(framedata), data


def plot_fig(df, data, categories, output):
    plt.style.use('ggplot')
    sns.set(style="whitegrid")
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['figure.figsize'] = (9, 2.5)
    plt.rcParams['axes.labelsize'] = 17
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['font.serif'] = 'DejaVu Sans'
    plt.rcParams['font.monospace'] = 'Inconsolata Medium'
    plt.rcParams['axes.labelweight'] = 'bold'
    ax = df.plot.barh(width=0.3,
                      color=['#e69f56', '#b07219', '#f18e33', '#c22d40'],
                      stacked=True)

    sums = []
    for c in categories:
        v = sum(data[(lang, c)]
                for lang in ['Groovy', 'Java', 'Kotlin', 'Scala'])
        sums.append(v)

    for i, p in enumerate(ax.patches[15:]):
        ax.annotate("{} / 320".format(int(sums[i])),
                    (p.get_x() + p.get_width(), p.get_y()),
                    xytext=(5, 10), textcoords='offset points')
    ax.set_ylabel('')
    patches, labels = ax.get_legend_handles_labels()
    plt.savefig(output, format='pdf', bbox_inches='tight',
                pad_inches=0)


def get_row(df, symptom):
    total = 0
    langs = ["Groovy", "Java", "Kotlin", "Scala"]
    res = [symptom]
    for lang in langs:
        n = int(df[lang][symptom])
        total += n
        res.append("{} ({:.1f}%)".format(
           n, (n/80) * 100
        ))
    res.append("{} ({:.1f}%)".format(
       total, (total/320) * 100
    ))
    return res


def print_stats(df):
    df = df.fillna(0)
    header = ["Symptom", "Groovy", "Java", "Kotlin", "Scala", "Total"]
    row1 = get_row(df, 'Unexpected Compile-Time Error')
    row2 = get_row(df, 'Internal Compiler Error')
    row3 = get_row(df, 'Unexpected Runtime Behavior')
    row4 = get_row(df, 'Misleading Report')
    row5 = get_row(df, 'Compilation Performance Issue')
    header_format = "{:<30}" + "{:>15}" * 5
    row_format = "{:<30}" + "{:>15}" * 5
    print(header_format.format(*header))
    print(row_format.format(*row1))
    print(row_format.format(*row2))
    print(row_format.format(*row3))
    print(row_format.format(*row4))
    print(row_format.format(*row5))


def main():
    args = get_args()
    with open(args.data, 'r') as f:
        json_data = json.load(f)
    df, data = construct_dataframe(json_data)
    df = df.groupby(['Language', 'Symptom'])['Number of bugs'].sum().unstack(
        'Language')
    categories = [
        'Compilation Performance Issue',
        'Misleading Report',
        'Unexpected Runtime Behavior',
        'Internal Compiler Error',
        'Unexpected Compile-Time Error',
    ]
    df = df.reindex(categories)
    plot_fig(df, data, categories, args.output)
    print_stats(df)


if __name__ == "__main__":
    main()
