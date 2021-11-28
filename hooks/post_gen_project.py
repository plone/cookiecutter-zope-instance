# post generation step: replace relative with absolute path
# theres no way to get this path while generating the files

import os
import re

from cookiecutter.utils import work_in

target = """{{ cookiecutter.target }}"""
cwd = os.path.abspath(os.getcwd())
basedir = cwd[: -len(target)]


with work_in(basedir):
    for dir, subdirs, files in os.walk(cwd):
        for filename in files:
            infile = os.path.join(dir, filename)
            lines = []
            with open(infile) as fio:
                for line in fio:
                    mo = re.match(r".*ABSPATH\((.*?)\).*", line)
                    if mo:
                        for path in mo.groups():
                            line = line.replace(
                                f"ABSPATH({path})", os.path.abspath(path)
                            )
                    lines.append(line)

            with open(infile, "w") as fio:
                fio.truncate()
                for line in lines:
                    fio.writelines(line)
