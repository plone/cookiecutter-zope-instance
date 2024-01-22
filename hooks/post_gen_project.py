from binascii import b2a_base64
from cookiecutter.utils import work_in
from hashlib import sha1
from pathlib import Path

import os
import random
import string


cwd = Path.cwd()
basedir = cwd.parent


# post generation step 1: generate initial user
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


# post generation step 2: generate directories
with work_in(basedir):
    Path("{{ cookiecutter.location_clienthome }}").mkdir(parents=True, exist_ok=True)
    Path("{{ cookiecutter.location_log }}").mkdir(parents=True, exist_ok=True)
    Path("{{ cookiecutter.db_blobs_location }}").mkdir(parents=True, exist_ok=True)
    Path("{{ cookiecutter.environment['CHAMELEON_CACHE'] }}").mkdir(parents=True, exist_ok=True)
    if "{{ cookiecutter.db_storage }}" == "direct":
        filepath = Path("{{ cookiecutter.db_filestorage_location }}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
