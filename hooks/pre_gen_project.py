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

# pgjsonb requires a DSN
if (
    "{{ cookiecutter.db_storage }}" == "pgjsonb"
    and not "{{ cookiecutter.db_pgjsonb_dsn }}"
):
    print("Error: 'pgjsonb' storage requires 'db_pgjsonb_dsn' to be set!")
    exit(1)

# z3blobs wrapper validation
if "{{ cookiecutter.db_z3blobs_enabled }}" in ("True", "true"):
    if "{{ cookiecutter.db_storage }}" == "pgjsonb":
        print(
            "Error: 'db_z3blobs_enabled' cannot be used with 'pgjsonb' storage!"
            " PGJsonb handles blobs natively (bytea/S3)."
        )
        exit(1)
    if not "{{ cookiecutter.db_z3blobs_bucket_name }}":
        print("Error: 'db_z3blobs_enabled' requires 'db_z3blobs_bucket_name' to be set!")
        exit(1)
    if not "{{ cookiecutter.db_z3blobs_cache_dir }}":
        print("Error: 'db_z3blobs_enabled' requires 'db_z3blobs_cache_dir' to be set!")
        exit(1)
    if (
        "{{ cookiecutter.db_z3blobs_s3_sse_customer_key }}"
        and "{{ cookiecutter.db_z3blobs_s3_use_ssl }}" in ("False", "false")
    ):
        print("Error: 'db_z3blobs_s3_sse_customer_key' requires 's3-use-ssl' to be true!")
        exit(1)

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
        "The 'load_zcml' dict setting was deprecated in version 2.0. Instead use the name of its keys prefixed with 'zcml_' as the new variable names."
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

# logging configuration validation
log_format = "{{ cookiecutter.log_format }}".lower()
if log_format not in ("text", "json"):
    print(f"Error: 'log_format' must be 'text' or 'json', got '{log_format}'!")
    exit(1)

log_stdout = "{{ cookiecutter.log_stdout }}"
log_file = "{{ cookiecutter.log_file }}"
log_syslog = "{{ cookiecutter.log_syslog }}"
if log_stdout == "False" and log_file == "False" and log_syslog == "False":
    print("Error: At least one log handler must be enabled (log_stdout, log_file, or log_syslog)!")
    exit(1)

log_stdout_stream = "{{ cookiecutter.log_stdout_stream }}"
if log_stdout_stream not in ("stdout", "stderr"):
    print(f"Error: 'log_stdout_stream' must be 'stdout' or 'stderr', got '{log_stdout_stream}'!")
    exit(1)

log_syslog_protocol = "{{ cookiecutter.log_syslog_protocol }}"
if log_syslog_protocol not in ("udp", "tcp"):
    print(f"Error: 'log_syslog_protocol' must be 'udp' or 'tcp', got '{log_syslog_protocol}'!")
    exit(1)

log_syslog_facility = {{ cookiecutter.log_syslog_facility }}
if not (0 <= log_syslog_facility <= 23):
    print(f"Error: 'log_syslog_facility' must be 0-23, got {log_syslog_facility}!")
    exit(1)

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
