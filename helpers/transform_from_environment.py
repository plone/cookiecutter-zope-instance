#!/bin/env python
"""
Transform an input configuration file for cookie-cutter-zopeinstance
from environment variables with a given prefix and output the result
to a new file.
"""
import os
import argparse

try:
    import yaml
except ImportError:
    print ("Error: Please 'pip install pyyaml' first!")
    exit(1)

parser = argparse.ArgumentParser(
    description="Transforms an input configuration file for "
                "cookie-cutter-zopeinstance from environment "
                "variables with a given prefix and output the result.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "-p",
    "--prefix",
    help="Prefix of environment variables to use",
    type=str,
    default="INSTANCE_",
)
parser.add_argument(
    "-i",
    "--infile",
    help="File to read values from",
    type=str,
    default="instance.yaml",
)
parser.add_argument(
    "-o",
    "--outfile",
    help="File to write result to",
    type=str,
    default="instance-from-environment.yaml",
)
args = parser.parse_args()

# load base instance.yaml
with open(args.infile, "r") as fio:
    instance = yaml.safe_load(fio)
cfg = instance["default_context"]

# set values from enviroment
for envkey, value in os.environ.items():
    if not envkey.startswith(args.prefix):
        continue

    # handle boolean values.
    if value.lower() in ("true", "false"):
        value = value.lower() == "true"

    key = envkey[len(args.prefix) :].lower()
    print(f"Set from env {envkey}: {key}={value}")
    cfg[key] = value


# write file
with open(args.outfile, "w") as fio:
    yaml.dump(instance, fio)

print(f"{args.outfile} written, done!")
