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
    print("Error: Please 'python -m pip install pyyaml' first!")
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


def handle_value(value):
    if isinstance(value, str) and value.lower() in ("true", "false"):
        value = value.lower() == "true"
    return value


_DICT_DELIMITER = "_DICT_"


def handle_dict(key, value, cfg):
    """Handles a dict from environment and insert value in cfg

    In order to define dicts (and sub-dicts) in (flat) environment variables,
    we use a convention where we separate keys by _DICT_.
    This can be recursive, so we need to handle that.

    Flat Example: "environment_DICT_foo=bar results in cfg['environment'] = {'foo': 'bar'}
    Recursive Example: "environment_DICT_foo_DICT_bar=baz results in cfg['environment'] = {'foo': {'bar': 'baz'}}

    If the key is not in the cfg, we create a new dict, other wise we update the existing one.
    """
    main_key, sub_key = key.split(_DICT_DELIMITER, 1)
    if not sub_key:
        print(
            f"Error: {_DICT_DELIMITER} in key must be followed by a sub-key, got: {envkey}"
        )
        exit(1)

    main_key = main_key.lower()
    if main_key not in cfg:
        cfg[main_key] = {}
    if _DICT_DELIMITER in sub_key:
        value = handle_dict(sub_key, value, cfg[main_key])
    print(f"Set from dict {envkey}: {key}={value}")
    cfg[main_key][sub_key] = handle_value(value)


# set values from environment
for envkey, value in os.environ.items():
    if not envkey.startswith(args.prefix):
        continue
    key = envkey[len(args.prefix) :]
    if _DICT_DELIMITER in key:
        handle_dict(key, value, cfg)
        continue
    key = key.lower()
    print(f"Set from env {envkey}: {key}={value}")
    cfg[key] = handle_value(value)

# write file
with open(args.outfile, "w") as fio:
    yaml.dump(instance, fio)

print(f"{args.outfile} written, done!")
