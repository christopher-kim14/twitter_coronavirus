#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter, defaultdict
import matplotlib
matplotlib.rcParams['font.family'] = 'UnDotum'
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# sort from low to high
items = sorted(counts[args.key].items(), key=lambda item: (item[1], item[0]))

# take the top 10
top10 = items[-10:]

# get keys and values
keys = [k for k, v in top10]
values = [v for k, v in top10]

if "country" in args.input_path:
    x = "countries"
else:
    x = "languages"

# create the bar chart
plt.figure(figsize=(10, 6))
plt.bar(keys, values)
plt.xlabel(x)
plt.ylabel(f'{args.key} occurrences')
plt.title(f'Top 10 {x} by {args.key}')
plt.xticks(rotation=45)
plt.tight_layout()

# save the plot
plt.savefig(f'{args.input_path}_{args.key.replace("#", "")}.png')
