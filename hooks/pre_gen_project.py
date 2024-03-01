from collections import OrderedDict

# invariant checks
# check database mode direct and blobs not cache
if (
    "{{ cookiecutter.db_storage }}" == "direct"
    and "{{ cookiecutter.db_blobs_mode }}" == "cache"
):
    print("Error: A 'direct' database must be configured with 'shared' blobs_mode!")
    exit(1)

# check database mode not direct and blobs not shared
if (
    "{{ cookiecutter.db_storage }}" == "relstorage"
    and "{{ cookiecutter.db_blobs_mode }}" == "shared"
):
    print("Warning: A 'relstorage' database is better used with 'cache' blobs_mode!\n")

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
has_old_zcml = True if [value for value in load_zcml.values() if value] else False
if has_old_zcml:
    upgrade_warnings.append(
        "The 'zcml' dict setting is removed in 2.0, use 'zcml_' prefix variables instead!"
    )

if "{{ cookiecutter.debug_mode in [True, False] }}" != "True":
    upgrade_errors.append(
        "The 'debug_mode' setting must be boolean in 2.0, please fix your configuration!\n"
    )

if "{{ cookiecutter.verbose_security in [True, False] }}" != "True":
    upgrade_errors.append(
        "The'verbose_security' setting must be boolean in 2.0, please fix your configuration!\n"
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