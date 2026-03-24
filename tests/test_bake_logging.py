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
