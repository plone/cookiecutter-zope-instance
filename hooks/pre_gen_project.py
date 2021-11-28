# invarant checks

# check database mode direct and blobs not cache
if (
    "{{ cookiecutter.database }}" == "direct"
    and "{{ cookiecutter.blobs_mode }}" == "cache"
):
    print("Error: A 'direct' database must be configured with 'shared' blobs_mode")
    exit(1)

# sane check for password
password = "{{ cookiecutter.initial_user_password }}"
if 0 < len(password) < 10:
    print("Error: initial user's password must be at least 10 characters long.")
    exit(1)
