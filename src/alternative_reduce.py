#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths', nargs='+', required=True)
parser.add_argument('--hashtags', nargs='+', required=True)
args = parser.parse_args()

# imports
import os
import json
from collections import Counter, defaultdict
import re
import matplotlib.pyplot as plt

# helper function
def extract_date_pattern(filename):
    match = re.search(r'\d{2}-\d{2}-\d{2}', filename)
    return match.group(0) if match else None

# initialize total
total = defaultdict(lambda: Counter())

# scan through all input files
for path in args.input_paths:
    date = extract_date_pattern(path)
    with open(path) as f:
        tmp = json.load(f)
        for hashtag in args.hashtags:
            if hashtag in tmp:
                total[date][hashtag] = sum(tmp[hashtag].values())

# extract dates in chronological order
dates = sorted(total.keys())

# prepare plot data
hashtag_counts = {
    tag: [total[date].get(tag, 0) for date in dates]
    for tag in args.hashtags
}

# plot
plt.figure(figsize=(10, 5))
for tag, counts in hashtag_counts.items():
    plt.plot(dates, counts, marker='o', label=tag)

# formatting
plt.xlabel("Date")
plt.ylabel("Count")
plt.title("Hashtag Frequency Over Time")
plt.xticks(dates[::20], rotation=45, fontsize=8)
plt.legend()
plt.grid(True)

# save the plot as a PNG file
plt.savefig("hashtag_trend.png", dpi=300, bbox_inches="tight")
plt.close()
