from collections import OrderedDict

# invariant checks
# check database mode direct and blobs not cache
if (
    "{{ cookiecutter.db_storage }}" == "direct"
    and "{{ cookiecutter.db_blobs_mode or cookiecutter.db_blob_mode }}" == "cache"
):
    print("Error: A 'direct' database must be configured with 'shared' db_blob_mode!")
    exit(1)

# check database mode not direct and blobs not shared
db_blob_mode = "{{ cookiecutter.db_blobs_mode }}"
if db_blob_mode == "":
    db_blob_mode = "{{ cookiecutter.db_blob_mode }}"
if (
    "{{ cookiecutter.db_storage }}" == "relstorage" and db_blob_mode == "shared"
):
    print("Warning: A 'relstorage' database is better used with 'cache' db_blob_mode!\n")

# minimal sanity check for password
password = "{{ cookiecutter.initial_user_password }}"
if 0 < len(password) < 10:
    print(
        "Warning: initial user's password is insecure, it should be at least 10 characters long!\n"
    )

# version 2 config changes check
upgrade_warnings = []
upgrade_errors = []
load_zcml = {{ cookiecutter.load_zcml }}
has_old_zcml = bool([value for value in load_zcml.values() if value])
if has_old_zcml:
    upgrade_warnings.append(
        "The 'load_zcml' dict setting is deprecated in 2.0, use 'zcml_' prefix variables instead!"
    )

if "{{ cookiecutter.debug_mode in [True, False] }}" != "True":
    upgrade_errors.append(
        "The 'debug_mode' setting must be boolean in 2.0, please fix your configuration!\n"
    )

if "{{ cookiecutter.verbose_security in [True, False] }}" != "True":
    upgrade_errors.append(
        "The 'verbose_security' setting must be boolean in 2.0, please fix your configuration!\n"
    )

if "{{ cookiecutter.db_blobs_mode }}" != "":
    upgrade_warnings.append(
        "The 'db_blobs_mode' setting was renamed to 'db_blob_mode', please fix your configuration!"
    )

if "{{ cookiecutter.db_blobs_location }}" != "":
    upgrade_warnings.append(
        "The 'db_blobs_location' setting was renamed to 'db_blob_location', please fix your configuration!"
    )

if upgrade_errors:
    print("The following errors prevent cookiecutter-zope-instance from continuing, please fix them:")
    for error_msg in upgrade_errors:
        print(f" - Error: {error_msg}")
    exit(1)

elif upgrade_warnings:
    print("Please review the following warning messages and fix them at your earliest convenience:")
    for warning_msg in upgrade_warnings:
        print(f" - Warning: {warning_msg}")
    print()
