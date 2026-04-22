"""Tests for up-front validation of cookiecutter config overrides.

Cookiecutter's :func:`apply_overwrites_to_context` short-circuits on the first
invalid override (e.g. an unparseable boolean), caught one frame up as a
``UserWarning`` and silently discards all remaining overrides. The generated
project ends up with a mix of user-set values and ``cookiecutter.json``
defaults — "fried" etc/* files, as reported in
https://github.com/plone/cookiecutter-zope-instance/issues/43.

The pre-generation hook inspects the cookiecutter config file directly and
aborts with an actionable error before cookiecutter can silently drop
overrides.
"""

from pathlib import Path

import pytest
import yaml
from cookiecutter.exceptions import FailedHookException
from cookiecutter.main import cookiecutter


TEMPLATE = str(Path(__file__).resolve().parent.parent)


@pytest.fixture
def bake(tmp_path, monkeypatch):
    def _bake(default_context):
        user_dir = tmp_path / "user"
        user_dir.mkdir(exist_ok=True)
        (user_dir / "cc_dir").mkdir(exist_ok=True)
        (user_dir / "replay").mkdir(exist_ok=True)
        config_file = user_dir / "config"
        config_file.write_text(
            yaml.safe_dump(
                {
                    "cookiecutters_dir": str(user_dir / "cc_dir"),
                    "replay_dir": str(user_dir / "replay"),
                    "default_context": default_context,
                }
            )
        )
        output = tmp_path / "out"
        output.mkdir(exist_ok=True)
        # COOKIECUTTER_CONFIG lets the pre-gen hook discover the same config
        # file cookiecutter uses (cookiecutter does not expose the explicit
        # --config-file argument to hooks).
        monkeypatch.setenv("COOKIECUTTER_CONFIG", str(config_file))
        return cookiecutter(
            TEMPLATE,
            no_input=True,
            output_dir=str(output),
            config_file=str(config_file),
        )

    return _bake


@pytest.mark.parametrize("value", ["", "maybe", "nope", "2", "   "])
def test_unparseable_boolean_default_aborts(bake, value):
    with pytest.raises(FailedHookException):
        bake({"log_syslog": value})


@pytest.mark.parametrize(
    "value", ["true", "True", "yes", "Y", "on", "false", "False", "n", "0", "OFF"]
)
def test_parseable_boolean_string_default_succeeds(bake, value):
    bake({"log_syslog": value})


def test_real_boolean_default_succeeds(bake):
    bake({"log_syslog": False})


def test_invalid_choice_default_aborts(bake):
    with pytest.raises(FailedHookException):
        bake({"db_storage": "sqlserver"})


def test_valid_choice_default_succeeds(bake):
    bake({"db_storage": "zeo"})


def test_no_default_context_succeeds(bake):
    bake({})
