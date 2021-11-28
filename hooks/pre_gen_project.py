# invariant checks

# check database mode direct and blobs not cache
if (
    "{{ cookiecutter.database }}" == "direct"
    and "{{ cookiecutter.blobs_mode }}" == "cache"
):
    print("Error: A 'direct' database must be configured with 'shared' blobs_mode!")
    exit(1)

# check database mode not direct and blobs not shared
if (
    "{{ cookiecutter.database }}" == "relstorage"
    and "{{ cookiecutter.blobs_mode }}" == "shared"
):
    print("Warning: A 'relstorage' database is better used with 'cache' blobs_mode!\n")

# minimal sanity check for password
password = "{{ cookiecutter.initial_user_password }}"
if 0 < len(password) < 10:
    print("Warning: initial user's password must be at least 10 characters long!\n")
