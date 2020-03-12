import argparse
import random
import os
from os.path import join

"""
A utility for creating train test splits
"""

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', help='source')
    parser.add_argument('-t', nargs='+', help='targets')
    parser.add_argument('-r', nargs='+', help='sampling ratios', type=float)
    parser.add_argument('-root', help='where the target folders are located')

    args = parser.parse_args()
    return args

def split(source, targets, ratios, root):
    files = os.listdir(source)
    random.shuffle(files)

    last_idx = 0
    for target, ratio in zip(targets, ratios):
        num = int(ratio * len(files))
        for file in files[last_idx:last_idx+num]:
            os.rename(join(source, file), join(root, target, file))
        last_idx = num

if __name__ == '__main__':
    args = parse_args()
    split(args.s, args.t, args.r, args.root)
