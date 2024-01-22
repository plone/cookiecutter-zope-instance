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
    print("Warning: initial user's password is insecure, it should be at least 10 characters long!\n")

# version 2 config changes check
if "{{ 'zcml' in cookiecutter.__dict__ }}" == "True":
    print("Warning: 'zcml' dict setting is removed in 2.0, use 'zcml_' prefix variables instead!\n")
