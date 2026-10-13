"""Tests for up-front validation of cookiecutter config overrides.

Cookiecutter's :func:`apply_overwrites_to_context` short-circuits on the first
invalid override (e.g. an unparseable boolean), caught one frame up as a
``UserWarning`` and silently discards all remaining overrides. The generated
project ends up with a mix of user-set values and ``cookiecutter.json``
defaults, as reported in
https://github.com/plone/cookiecutter-zope-instance/issues/43.

``local_extensions`` validates the raw ``default_context`` in-process and
aborts before any file is generated. The CLI tests cover the invocation styles
a pre-generation hook cannot see (``--config-file``, relative and cloned
templates).
"""

from cookiecutter.exceptions import FailedHookException
from cookiecutter.main import cookiecutter
from pathlib import Path

import os
import pytest
import shutil
import subprocess
import sys
import yaml


TEMPLATE = Path(__file__).resolve().parent.parent


def _write_config(user_dir, default_context):
    (user_dir / "cc_dir").mkdir(parents=True, exist_ok=True)
    (user_dir / "replay").mkdir(exist_ok=True)
    config_file = user_dir / "config.yaml"
    config_file.write_text(
        yaml.safe_dump(
            {
                "cookiecutters_dir": str(user_dir / "cc_dir"),
                "replay_dir": str(user_dir / "replay"),
                "default_context": default_context,
            }
        )
    )
    return config_file


@pytest.fixture
def bake(tmp_path, monkeypatch):
    # Make sure validation does not depend on the config being discoverable
    # from the environment.
    monkeypatch.delenv("COOKIECUTTER_CONFIG", raising=False)

    def _bake(default_context):
        config_file = _write_config(tmp_path / "user", default_context)
        output = tmp_path / "out"
        output.mkdir(exist_ok=True)
        return cookiecutter(
            str(TEMPLATE),
            no_input=True,
            output_dir=str(output),
            config_file=str(config_file),
        )

    return _bake


@pytest.mark.parametrize("value", ["", "maybe", "nope", "2", "   "])
def test_unparseable_boolean_default_aborts(bake, value):
    with pytest.raises(FailedHookException, match="log_syslog"):
        bake({"log_syslog": value})


@pytest.mark.parametrize(
    "value", ["true", "True", "yes", "Y", "on", "false", "False", "n", "0", "OFF"]
)
def test_parseable_boolean_string_default_succeeds(bake, value):
    bake({"log_syslog": value})


def test_real_boolean_default_succeeds(bake):
    bake({"log_syslog": False})


def test_invalid_choice_default_aborts(bake):
    with pytest.raises(FailedHookException, match="db_storage"):
        bake({"db_storage": "sqlserver"})


def test_valid_choice_default_succeeds(bake):
    bake({"db_storage": "zeo"})


def test_no_default_context_succeeds(bake):
    bake({})


def test_all_invalid_overrides_are_reported(bake):
    with pytest.raises(FailedHookException) as excinfo:
        bake({"log_syslog": "", "db_storage": "sqlserver", "debug_mode": "maybe"})
    message = str(excinfo.value)
    assert "log_syslog" in message
    assert "db_storage" in message
    assert "debug_mode" in message


def _run_cli(tmp_path, template, cwd=None):
    """Run the cookiecutter CLI the way the docs and Makefiles do."""
    config_file = _write_config(
        tmp_path / "user",
        {"log_syslog": "", "zcml_package_includes": "my.pkg"},
    )
    output = tmp_path / "out"
    env = dict(os.environ, HOME=str(tmp_path / "user"))
    # The template under test must be imported from its own location, not
    # from the checkout on PYTHONPATH.
    env.pop("PYTHONPATH", None)
    env.pop("COOKIECUTTER_CONFIG", None)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "cookiecutter",
            "-f",
            "--no-input",
            "--config-file",
            str(config_file),
            "-o",
            str(output),
            str(template),
        ],
        cwd=cwd or tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    return result, output


def _assert_aborted(result, output):
    assert result.returncode == 1, result.stdout + result.stderr
    assert "log_syslog" in result.stdout + result.stderr
    assert not (output / "instance").exists()


def test_cli_config_file_absolute_template_aborts(tmp_path):
    _assert_aborted(*_run_cli(tmp_path, TEMPLATE))


def test_cli_config_file_relative_template_aborts(tmp_path):
    shutil.copytree(
        TEMPLATE,
        tmp_path / "tpl",
        ignore=shutil.ignore_patterns(".git", ".venv", ".tox", "__pycache__"),
    )
    _assert_aborted(*_run_cli(tmp_path, "tpl", cwd=tmp_path))


def test_cli_config_file_cloned_template_aborts(tmp_path):
    """Covers gh:plone/cookiecutter-zope-instance, the canonical invocation."""
    repo = tmp_path / "repo"
    shutil.copytree(
        TEMPLATE,
        repo,
        ignore=shutil.ignore_patterns(".git", ".venv", ".tox", "__pycache__"),
    )
    git = ["git", "-c", "user.name=test", "-c", "user.email=test@example.com"]
    subprocess.run([*git, "init", "-q"], cwd=repo, check=True)
    subprocess.run([*git, "add", "-A"], cwd=repo, check=True)
    subprocess.run([*git, "commit", "-q", "-m", "template"], cwd=repo, check=True)
    _assert_aborted(*_run_cli(tmp_path, f"git+file://{repo}"))
