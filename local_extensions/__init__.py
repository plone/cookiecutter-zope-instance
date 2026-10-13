from cookiecutter.exceptions import FailedHookException
from jinja2 import pass_context
from jinja2.ext import Extension
from pathlib import Path

import inspect
import json


# Validation of cookiecutter config overrides, see issue #43.
#
# cookiecutter.generate.apply_overwrites_to_context stops at the first invalid
# override (e.g. an empty string for a boolean, or an unknown choice). The
# caller turns the ValueError into a UserWarning and every remaining override
# in default_context is silently dropped, leaving incomplete etc/* files.
#
# A pre-generation hook cannot catch this reliably: hooks neither see
# --config-file nor know where the template lives when it was cloned. This
# extension is loaded in the cookiecutter process after the context was built
# and before any file is written, so it validates the raw default_context as
# cookiecutter loaded it, however the config was passed.
YES_NO_VALUES = {
    "1",
    "true",
    "t",
    "yes",
    "y",
    "on",
    "0",
    "false",
    "f",
    "no",
    "n",
    "off",
}
COOKIECUTTER_JSON = Path(__file__).resolve().parent.parent / "cookiecutter.json"


def _raw_default_context():
    """Return default_context from the running cookiecutter() call, or None.

    Relies on the local name ``config_dict`` in ``cookiecutter.main.cookiecutter``
    (present since at least cookiecutter 2.1.1). If it is not found, the check is
    skipped; the CLI tests in tests/test_bake_invalid_overrides.py fail then.
    """
    frame = inspect.currentframe()
    try:
        while frame is not None:
            if (
                frame.f_globals.get("__name__") == "cookiecutter.main"
                and frame.f_code.co_name == "cookiecutter"
            ):
                if frame.f_locals.get("replay"):
                    # Replay ignores default_context.
                    return None
                config_dict = frame.f_locals.get("config_dict") or {}
                return config_dict.get("default_context") or {}
            frame = frame.f_back
    finally:
        del frame
    return None


def _override_errors(default_context, declared):
    errors = []
    for var, val in default_context.items():
        default = declared.get(var)
        if isinstance(default, bool):
            if isinstance(val, bool):
                continue
            if not isinstance(val, str) or val.strip().lower() not in YES_NO_VALUES:
                errors.append(
                    f"{var}={val!r} cannot be parsed as boolean "
                    "(use true/false/yes/no/on/off/0/1)"
                )
        elif (
            isinstance(default, list)
            and default
            and all(isinstance(c, (str, int, float, bool)) for c in default)
        ):
            # Choice variable.
            if val not in default:
                errors.append(f"{var}={val!r} is not one of {default}")
    return errors


def validate_default_context():
    default_context = _raw_default_context()
    if not default_context or not isinstance(default_context, dict):
        return
    declared = json.loads(COOKIECUTTER_JSON.read_text())
    errors = _override_errors(default_context, declared)
    if errors:
        lines = "\n".join(f"  - {error}" for error in errors)
        raise FailedHookException(
            "Error: invalid override(s) in the cookiecutter config "
            "(default_context).\n"
            f"{lines}\n"
            "Cookiecutter would drop these and every override after them, "
            "producing incomplete etc/* files.\n"
            "See https://github.com/plone/cookiecutter-zope-instance/issues/43"
        )


class ZopeExtensions(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        validate_default_context()
        environment.filters["abspath"] = ZopeExtensions.abspath

    @pass_context
    def abspath(context, path, append_path=""):
        try:
            _context_cookiecutter = context.get("cookiecutter")
            if _context_cookiecutter:
                _output_dir = _context_cookiecutter.get("_output_dir")
                if _output_dir:
                    new_path = Path(_output_dir, path, append_path).resolve().as_posix()
                else:
                    raise ValueError("No _output_dir in cookiecutter context")
            else:
                raise ValueError("No cookiecutter context")
        except Exception as e:
            raise Exception(f"Failed to filter {context.name}") from e

        return f"{new_path}"
