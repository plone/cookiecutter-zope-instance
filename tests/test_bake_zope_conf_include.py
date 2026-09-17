from utils import bake_in_temp_dir


def _zope_conf(result):
    return (result.project_path / "etc" / "zope.conf").read_text()


def test_no_include_by_default(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0, result.exception
        assert "%include" not in _zope_conf(result)


def test_absolute_include_path_renders_verbatim(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "zope_conf_include_file_location": "/srv/extra/zope-extra.conf"
        },
    ) as result:
        assert result.exit_code == 0, result.exception
        conf = _zope_conf(result)
        assert "%include /srv/extra/zope-extra.conf" in conf
        # rendered at the end, after the main database section
        assert conf.index("</zodb_db>") < conf.index("%include")


def test_relative_include_path_is_anchored_at_output_dir(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={"zope_conf_include_file_location": "etc/extra.conf"},
    ) as result:
        assert result.exit_code == 0, result.exception
        expected = (
            result.project_path.parent / "etc" / "extra.conf"
        ).resolve().as_posix()
        assert f"%include {expected}" in _zope_conf(result)
