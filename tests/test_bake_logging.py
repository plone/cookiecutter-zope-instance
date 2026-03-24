from utils import bake_in_temp_dir


def test_invalid_log_format_aborts(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"log_format": "xml"}
    ) as result:
        assert result.exit_code != 0


def test_all_handlers_disabled_aborts(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "log_stdout": False,
            "log_file": False,
            "log_syslog": False,
        },
    ) as result:
        assert result.exit_code != 0


def test_invalid_log_syslog_protocol_aborts(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "log_syslog": True,
            "log_syslog_protocol": "http",
        },
    ) as result:
        assert result.exit_code != 0


def test_invalid_log_stdout_stream_aborts(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={"log_stdout_stream": "stdin"},
    ) as result:
        assert result.exit_code != 0


def test_valid_log_format_json_succeeds(cookies):
    with bake_in_temp_dir(
        cookies, extra_context={"log_format": "json"}
    ) as result:
        assert result.exit_code == 0


def test_valid_syslog_tcp_succeeds(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "log_syslog": True,
            "log_syslog_protocol": "tcp",
        },
    ) as result:
        assert result.exit_code == 0


# === Formatter tests ===


def test_default_text_formatter(cookies):
    """Default config generates generic text formatter."""
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[formatter_generic]" in zope_ini
        assert "%(asctime)s %(levelname)-7.7s" in zope_ini


def test_json_formatter(cookies):
    """JSON format generates pythonjsonlogger formatter."""
    with bake_in_temp_dir(
        cookies, extra_context={"log_format": "json"}
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[formatter_json]" in zope_ini
        assert "pythonjsonlogger.jsonlogger.JsonFormatter" in zope_ini
        assert "[formatter_generic]" not in zope_ini


def test_custom_formatter(cookies):
    """Custom formatter class generates custom section."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "log_format_class": "mypackage.MyFormatter",
            "log_format_string": "%(message)s",
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[formatter_custom]" in zope_ini
        assert "mypackage.MyFormatter" in zope_ini


# === Handler tests ===


def test_default_stdout_handler(cookies):
    """Default config generates console handler to stderr only."""
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[handler_console]" in zope_ini
        assert "args = (sys.stderr,)" in zope_ini
        assert "[handler_eventlog]" not in zope_ini
        assert "[handler_accesslog]" not in zope_ini


def test_stdout_to_stdout(cookies):
    """log_stdout_stream=stdout sends to sys.stdout."""
    with bake_in_temp_dir(
        cookies, extra_context={"log_stdout_stream": "stdout"}
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "args = (sys.stdout,)" in zope_ini


def test_file_handler(cookies):
    """log_file=true generates file handlers."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "log_file": True,
            "log_file_path": "/tmp/plone-test-logs/instance.log",
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[handler_eventlog]" in zope_ini
        assert "/tmp/plone-test-logs/instance.log" in zope_ini
        assert "[handler_accesslog]" in zope_ini
        assert "/tmp/plone-test-logs/instance-access.log" in zope_ini


def test_file_handler_no_access_log(cookies):
    """access_log_enabled=false omits accesslog handler."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "log_file": True,
            "log_file_path": "/tmp/plone-test-logs/instance.log",
            "access_log_enabled": False,
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[handler_eventlog]" in zope_ini
        assert "[handler_accesslog]" not in zope_ini


def test_syslog_handler_udp(cookies):
    """log_syslog=true generates SysLogHandler with UDP."""
    with bake_in_temp_dir(
        cookies, extra_context={"log_syslog": True}
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[handler_syslog]" in zope_ini
        assert "logging.handlers.SysLogHandler" in zope_ini
        assert ", 2)" in zope_ini  # SOCK_DGRAM = 2


def test_syslog_handler_tcp(cookies):
    """log_syslog=true with tcp generates SOCK_STREAM."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "log_syslog": True,
            "log_syslog_protocol": "tcp",
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[handler_syslog]" in zope_ini
        # facility=1, socktype=1 (TCP)
        assert "1, 1)" in zope_ini


def test_no_stdout_handler(cookies):
    """log_stdout=false omits console handler."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "log_stdout": False,
            "log_file": True,
            "log_file_path": "/tmp/plone-test-logs/instance.log",
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[handler_console]" not in zope_ini


# === Logger tests ===


def test_default_loggers(cookies):
    """Default config generates root + default logging_loggers + wsgi."""
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[logger_root]" in zope_ini
        assert "[logger_plone]" in zope_ini
        assert "[logger_waitress_queue]" in zope_ini
        assert "[logger_waitress]" in zope_ini
        assert "[logger_wsgi]" in zope_ini


def test_custom_loggers_merged(cookies):
    """Custom logging_loggers adds loggers (merged with defaults)."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "logging_loggers": {
                "plone.restapi": "DEBUG",
                "sqlalchemy.engine": "WARNING",
            },
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        # Custom loggers are added
        assert "[logger_plone_restapi]" in zope_ini
        assert "qualname = plone.restapi" in zope_ini
        assert "[logger_sqlalchemy_engine]" in zope_ini
        assert "qualname = sqlalchemy.engine" in zope_ini
        # Default loggers still present (dict merge)
        assert "[logger_plone]" in zope_ini
        assert "[logger_waitress]" in zope_ini


def test_root_logger_level(cookies):
    """log_level controls root logger level."""
    with bake_in_temp_dir(
        cookies, extra_context={"log_level": "WARNING"}
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        lines = zope_ini.split("\n")
        for i, line in enumerate(lines):
            if "[logger_root]" in line:
                assert "level = WARNING" in lines[i + 1]
                break


def test_reserved_keys_ignored(cookies):
    """root and wsgi keys in logging_loggers are silently ignored."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "logging_loggers": {
                "root": "DEBUG",
                "wsgi": "DEBUG",
                "plone": "INFO",
            },
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert zope_ini.count("[logger_root]") == 1
        assert "[logger_plone]" in zope_ini


def test_access_log_disabled_no_wsgi_logger(cookies):
    """access_log_enabled=false omits wsgi logger and translogger."""
    with bake_in_temp_dir(
        cookies, extra_context={"access_log_enabled": False}
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[logger_wsgi]" not in zope_ini
        assert "translogger" not in zope_ini


def test_wsgi_logger_gets_console_handler(cookies):
    """wsgi logger gets console handler explicitly when stdout-only."""
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        in_wsgi = False
        for line in zope_ini.split("\n"):
            if "[logger_wsgi]" in line:
                in_wsgi = True
            elif in_wsgi and line.startswith("handlers"):
                assert "console" in line
                break
            elif in_wsgi and line.startswith("["):
                break


# === Integration tests ===


def test_full_cloud_native_config(cookies):
    """JSON to stdout, no files, no access log."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "log_format": "json",
            "log_stdout": True,
            "log_stdout_stream": "stdout",
            "log_file": False,
            "access_log_enabled": False,
            "log_level": "WARNING",
            "logging_loggers": {
                "plone": "INFO",
                "waitress.queue": "WARNING",
                "waitress": "WARNING",
            },
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "pythonjsonlogger.jsonlogger.JsonFormatter" in zope_ini
        assert "[formatter_generic]" not in zope_ini
        assert "[handler_console]" in zope_ini
        assert "args = (sys.stdout,)" in zope_ini
        assert "[handler_eventlog]" not in zope_ini
        assert "translogger" not in zope_ini
        assert "[logger_wsgi]" not in zope_ini


def test_full_traditional_config(cookies):
    """Text to files, access log, no stdout."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "log_stdout": False,
            "log_file": True,
            "log_file_path": "/tmp/plone-test-logs/instance.log",
            "access_log_enabled": True,
            "logging_loggers": {
                "plone": "INFO",
                "waitress": "WARNING",
            },
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[handler_console]" not in zope_ini
        assert "[handler_eventlog]" in zope_ini
        assert "[handler_accesslog]" in zope_ini
        assert "translogger" in zope_ini
        assert "[logger_wsgi]" in zope_ini


def test_full_hybrid_config(cookies):
    """stdout + syslog."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "log_stdout": True,
            "log_syslog": True,
            "log_syslog_host": "logserver.internal",
            "log_syslog_protocol": "tcp",
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[handler_console]" in zope_ini
        assert "[handler_syslog]" in zope_ini
        assert "logserver.internal" in zope_ini
        assert "1, 1)" in zope_ini  # facility=1, socktype=1 (TCP)


def test_location_log_fallback_path(cookies):
    """When log_file_path empty, use location_log fallback."""
    with bake_in_temp_dir(
        cookies,
        extra_context={"log_file": True},
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "instance.log" in zope_ini
        assert "[handler_eventlog]" in zope_ini


def test_log_file_path_overrides_location_log(cookies):
    """When log_file_path is set, it takes precedence."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "log_file": True,
            "log_file_path": "/tmp/plone-test-logs/instance.log",
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "/tmp/plone-test-logs/instance.log" in zope_ini
