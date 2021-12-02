# post generation step 1: replace relative with absolute path
# theres no way to get this path while generating the files

from binascii import b2a_base64
from cookiecutter.utils import work_in
from hashlib import sha1
from pathlib import Path

import os
import random
import re
import string


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


# post generation step 2: generate initial user
username = "{{ cookiecutter.initial_user_name }}" or "admin"
password = "{{ cookiecutter.initial_user_password }}"

inituser_filename = os.path.join(cwd, "inituser")

if not os.path.exists(inituser_filename):
    if not password:
        choices = list(string.ascii_letters + string.digits + "!#$%*(){}[]-")
        random.shuffle(choices)
        password = [random.choice(choices) for x in range(15)]
        random.shuffle(password)
        password = "".join(password)
        print(f"Generated password for initial user '{username}' is: {password}")
    with open(inituser_filename, "w") as fp:
        pw = b2a_base64(sha1(password.encode("utf-8")).digest())[:-1]
        fp.write("%s:{SHA}%s\n" % (username, pw.decode("ascii")))
    os.chmod(inituser_filename, 0o644)


# post generation step 3: generate directories
with work_in(basedir):
    Path("{{ cookiecutter.var_location }}").mkdir(parents=True, exist_ok=True)
    Path("{{ cookiecutter.log_location }}").mkdir(parents=True, exist_ok=True)
    Path("{{ cookiecutter.blobs_location }}").mkdir(parents=True, exist_ok=True)
    if "{{ cookiecutter.database }}" == "direct":
        Path("{{ cookiecutter.filestorage_location }}").mkdir(
            parents=True, exist_ok=True
        )
