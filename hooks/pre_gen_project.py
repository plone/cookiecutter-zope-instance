from collections import OrderedDict
from pathlib import Path

import json
import os

try:
    import yaml
except ImportError:  # pragma: no cover — cookiecutter depends on PyYAML
    yaml = None


# Up-front validation of cookiecutter config overrides.
#
# cookiecutter.generate.apply_overwrites_to_context short-circuits on the
# first invalid override (e.g. an empty string for a boolean, or an unknown
# choice). The exception is caught as a UserWarning and ALL remaining
# overrides in default_context are silently dropped, leaving the project
# partially configured — incomplete etc/* files. See issue #43.
#
# We re-read the cookiecutter config file and validate every override
# against the declared types in cookiecutter.json, aborting loudly before
# cookiecutter can silently fry things.
_YES_NO = {
    "1", "true", "t", "yes", "y", "on",
    "0", "false", "f", "no", "n", "off",
}


def _validate_default_context():
    if yaml is None:
        return []
    config_path = os.environ.get("COOKIECUTTER_CONFIG") or os.path.expanduser(
        "~/.cookiecutterrc"
    )
    if not os.path.isfile(config_path):
        return []
    try:
        cfg = yaml.safe_load(Path(config_path).read_text()) or {}
    except Exception as exc:
        return [f"could not parse cookiecutter config {config_path}: {exc}"]
    default_ctx = cfg.get("default_context") or {}
    if not isinstance(default_ctx, dict):
        return []
    template_dir = Path(r"{{ cookiecutter._template }}")
    cc_json = template_dir / "cookiecutter.json"
    if not cc_json.is_file():
        return []
    try:
        defaults = json.loads(cc_json.read_text())
    except Exception:
        return []
    errors = []
    for var, val in default_ctx.items():
        declared = defaults.get(var)
        if isinstance(declared, bool):
            if isinstance(val, bool):
                continue
            if not isinstance(val, str) or val.strip().lower() not in _YES_NO:
                errors.append(
                    f"{var}={val!r} cannot be parsed as boolean "
                    f"(use true/false/yes/no/on/off/0/1)"
                )
        elif isinstance(declared, list) and declared:
            # Choice variable. Also treat lists of dicts (nested) as free-form.
            if all(isinstance(c, (str, int, float, bool)) for c in declared):
                if val not in declared:
                    errors.append(
                        f"{var}={val!r} is not in allowed choices {declared}"
                    )
    return errors


_override_errors = _validate_default_context()
if _override_errors:
    print(
        "Error: invalid override(s) in cookiecutter default_context detected.\n"
        "Cookiecutter would silently drop these (and every subsequent override)\n"
        "via UserWarning, producing incomplete etc/* files.\n"
        "See https://github.com/plone/cookiecutter-zope-instance/issues/43\n"
    )
    for err in _override_errors:
        print(f"  - {err}")
    exit(1)


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

# wsgi_filters validation
RESERVED_FILTERS = {"zope", "profile", "translogger", "httpexceptions", "main"}
VALID_POSITIONS = {"outer", "inner"}

wsgi_filters = {{ cookiecutter.wsgi_filters }}
for name, _f in wsgi_filters.items():
    if name in RESERVED_FILTERS:
        print(f"Error: wsgi_filter name '{name}' is reserved!")
        exit(1)
    if not isinstance(_f, dict):
        print(f"Error: wsgi_filter '{name}' must be a mapping, got {_f!r}!")
        exit(1)
    if not _f.get("use"):
        print(f"Error: wsgi_filter '{name}' is missing required 'use'!")
        exit(1)
    position = _f.get("position", "outer")
    if position not in VALID_POSITIONS:
        print(f"Error: wsgi_filter '{name}' has invalid position '{position}' (outer|inner)!")
        exit(1)
