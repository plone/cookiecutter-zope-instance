from binascii import b2a_base64
from cookiecutter.utils import work_in
from hashlib import sha1
from pathlib import Path

import random
import string


cwd = Path.cwd()
basedir = cwd.parent
etc = cwd / "etc"


# post generation step 1: generate initial user
username = "{{ cookiecutter.initial_user_name }}" or "admin"
password = "{{ cookiecutter.initial_user_password }}"

inituser_filename = cwd / "inituser"

if not inituser_filename.exists():
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
    inituser_filename.chmod(0o644)


# post generation step 2: generate directories
with work_in(basedir):
    Path("{{ cookiecutter.location_clienthome }}").mkdir(parents=True, exist_ok=True)
    Path("{{ cookiecutter.location_log }}").mkdir(parents=True, exist_ok=True)
    Path("{{ cookiecutter.db_blob_location }}").mkdir(parents=True, exist_ok=True)
    Path("{{ cookiecutter.environment['CHAMELEON_CACHE'] }}").mkdir(
        parents=True, exist_ok=True
    )
    if "{{ cookiecutter.db_storage }}" == "direct":
        filepath = Path("{{ cookiecutter.db_filestorage_location }}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
    if "{{ cookiecutter.db_storage }}" == "direct":
        filepath = Path("{{ cookiecutter.db_filestorage_location }}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
    if "{{ cookiecutter.db_storage }}" == "relstorage":
        # import
        db_relstorage_import_blobs_location = (
            "{{ cookiecutter.db_relstorage_import_blobs_location | abspath }}"
        )
        if db_relstorage_import_blobs_location:
            filepath = Path(db_relstorage_import_blobs_location)
            filepath.mkdir(parents=True, exist_ok=True)
        db_relstorage_import_filestorage_location = (
            "{{ cookiecutter.db_relstorage_import_filestorage_location | abspath }}"
        )
        if db_relstorage_import_filestorage_location:
            filepath = Path(db_relstorage_import_filestorage_location)
            filepath.parent.mkdir(parents=True, exist_ok=True)

        # export
        db_relstorage_export_blobs_location = (
            "{{ cookiecutter.db_relstorage_export_blobs_location | abspath }}"
        )
        if db_relstorage_export_blobs_location:
            filepath = Path(db_relstorage_export_blobs_location)
            filepath.mkdir(parents=True, exist_ok=True)
        db_relstorage_export_filestorage_location = (
            "{{ cookiecutter.db_relstorage_export_filestorage_location | abspath }}"
        )
        if db_relstorage_export_filestorage_location:
            filepath = Path(db_relstorage_export_filestorage_location)
            filepath.parent.mkdir(parents=True, exist_ok=True)
    if "{{ cookiecutter.db_storage }}" == "pgjsonb":
        blob_temp_dir = "{{ cookiecutter.db_pgjsonb_blob_temp_dir }}"
        if blob_temp_dir:
            Path(blob_temp_dir).mkdir(parents=True, exist_ok=True)
        blob_cache_dir = "{{ cookiecutter.db_pgjsonb_blob_cache_dir }}"
        if blob_cache_dir:
            Path(blob_cache_dir).mkdir(parents=True, exist_ok=True)
    if "{{ cookiecutter.db_z3blobs_enabled }}" in ("True", "true"):
        z3blobs_cache_dir = "{{ cookiecutter.db_z3blobs_cache_dir }}"
        if z3blobs_cache_dir:
            Path(z3blobs_cache_dir).mkdir(parents=True, exist_ok=True)
    if "{{ cookiecutter.db_storage }}" != "relstorage":
        # cleanup relstorage files if no relstorage is configured
        (etc / "relstorage-export.conf").unlink()
        (etc / "relstorage-import.conf").unlink()
        (etc / "relstorage-pack.conf").unlink()

# 3: remove unused files
if "{{ cookiecutter.cors_enabled }}" == "False":
    (etc / "cors.zcml").unlink()
