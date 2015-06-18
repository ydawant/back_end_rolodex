#!/usr/bin/env python
import subprocess
import argparse

import sys
import re
from rolodex.models import Rolodex

def run(input_file,rolodex):
    with open(input_file, 'r') as f:
        index = 0
        while True:
            line = f.readline()
            #check if EOF
            if len(line) > 0:
                #Takes each line, splits on commas, and if it contains digits, strip all non numerical characters
                rolodex.add_rolodex_entry((index, [re.sub(r'\W+', '', x) if _contains_digits(x) else x for x in line.strip().split(", ")]))
                index += 1
            if not line:
                print rolodex.all_entries()
                break

_digits = re.compile('\d')
def _contains_digits(d):
    return bool(_digits.search(d))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true",help="Use this to run the tests")
    parser.add_argument("--run", help="Use this to run Rolodex, need file as well Ex. --run file.txt")

    args = parser.parse_args()

    if args.test:
        subprocess.call([sys.executable, '-m', 'unittest', 'discover'])
    if args.run:
        rolodex = Rolodex("common_first_names.csv", "last_suffix.csv")
        run(args.run, rolodex)