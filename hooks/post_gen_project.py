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
    # Handle log directory — deprecation of location_log
    log_file_path = "{{ cookiecutter.log_file_path }}"
    location_log = "{{ cookiecutter.location_log }}"
    log_file_enabled = "{{ cookiecutter.log_file }}" == "True"

    if log_file_enabled:
        if log_file_path:
            # log_file_path is explicitly set — use it, create parent dir
            log_dir = Path(log_file_path).parent
        elif location_log:
            # Deprecated fallback
            print(
                f"Warning: 'location_log' is deprecated and will be removed "
                f"in the next major version.\n"
                f"         Use 'log_file_path' instead.\n"
                f"         Falling back to '{location_log}/instance.log'.\n"
            )
            log_dir = Path(location_log)
        else:
            # Computed default
            log_dir = Path("{{ cookiecutter.target }}", "var", "log")
        log_dir.mkdir(parents=True, exist_ok=True)
    else:
        # Even when file logging is off, location_log dir may be needed
        # by profile_repoze settings
        if location_log:
            Path(location_log).mkdir(parents=True, exist_ok=True)
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
    if "{{ cookiecutter.db_storage }}" != "direct":
        # generic convert import directories
        db_convert_import_blobs = (
            "{{ cookiecutter.db_convert_import_blobs_location | abspath }}"
        )
        if db_convert_import_blobs:
            Path(db_convert_import_blobs).mkdir(parents=True, exist_ok=True)
        db_convert_import_fs = (
            "{{ cookiecutter.db_convert_import_filestorage_location | abspath }}"
        )
        if db_convert_import_fs:
            Path(db_convert_import_fs).parent.mkdir(parents=True, exist_ok=True)
        # generic convert export directories
        db_convert_export_blobs = (
            "{{ cookiecutter.db_convert_export_blobs_location | abspath }}"
        )
        if db_convert_export_blobs:
            Path(db_convert_export_blobs).mkdir(parents=True, exist_ok=True)
        db_convert_export_fs = (
            "{{ cookiecutter.db_convert_export_filestorage_location | abspath }}"
        )
        if db_convert_export_fs:
            Path(db_convert_export_fs).parent.mkdir(parents=True, exist_ok=True)
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
    if "{{ cookiecutter.db_storage }}" == "direct":
        # cleanup convert files — filestorage doesn't need conversion configs
        (etc / "convert-import.conf").unlink()
        (etc / "convert-export.conf").unlink()
    if "{{ cookiecutter.db_storage }}" != "relstorage":
        # cleanup relstorage files if no relstorage is configured
        (etc / "relstorage-export.conf").unlink()
        (etc / "relstorage-import.conf").unlink()
        (etc / "relstorage-pack.conf").unlink()

# 3: remove unused files
if "{{ cookiecutter.cors_enabled }}" == "False":
    (etc / "cors.zcml").unlink()
