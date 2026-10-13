from utils import bake_in_temp_dir


def _server_block(zope_ini):
    """Return the [server:main] section body up to the next section header."""
    out = []
    in_block = False
    for line in zope_ini.split("\n"):
        if line.strip() == "[server:main]":
            in_block = True
            continue
        if in_block and line.startswith("["):
            break
        if in_block:
            out.append(line)
    return "\n".join(out)


def _zope_ini(result):
    return (result.project_path / "etc" / "zope.ini").read_text()


def test_default_server_block_is_waitress(cookies):
    """Feature off: the waitress block renders exactly as before."""
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0, result.exception
        block = _server_block(_zope_ini(result))
        assert "use = egg:waitress#main" in block
        assert "listen = localhost:8080" in block
        assert "threads = 4" in block
        assert "clear_untrusted_proxy_headers = false" in block
        assert "max_request_body_size = 1073741824" in block
        assert "channel_timeout" not in block


def test_generic_server_renders_use_and_options_verbatim(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "wsgi_server_use": "egg:pyruvate#main",
            "wsgi_server_options": {"socket": "localhost:8080", "workers": "2"},
        },
    ) as result:
        assert result.exit_code == 0, result.exception
        block = _server_block(_zope_ini(result))
        assert "use = egg:pyruvate#main" in block
        assert "socket = localhost:8080" in block
        assert "workers = 2" in block
        assert "waitress" not in block
        assert "threads" not in block
        assert "max_request_body_size" not in block


def test_generic_server_without_options_renders_only_use(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={"wsgi_server_use": "egg:gunicorn#main"},
    ) as result:
        assert result.exit_code == 0, result.exception
        block = _server_block(_zope_ini(result))
        assert block.strip() == "use = egg:gunicorn#main"


def test_options_without_use_fail(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={"wsgi_server_options": {"socket": "localhost:8080"}},
    ) as result:
        assert result.exit_code != 0


def test_use_with_fast_listen_fails(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "wsgi_server_use": "egg:pyruvate#main",
            "wsgi_fast_listen": "localhost:8080",
        },
    ) as result:
        assert result.exit_code != 0


def test_use_key_inside_options_fails(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "wsgi_server_use": "egg:pyruvate#main",
            "wsgi_server_options": {"use": "egg:waitress#main"},
        },
    ) as result:
        assert result.exit_code != 0


def test_waitress_options_are_ignored_with_warning(cookies):
    """Setting waitress options alongside wsgi_server_use warns but bakes."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "wsgi_server_use": "egg:pyruvate#main",
            "wsgi_threads": "8",
        },
    ) as result:
        assert result.exit_code == 0, result.exception
        block = _server_block(_zope_ini(result))
        assert "threads" not in block
