from utils import bake_in_temp_dir


def _pipeline_block(zope_ini):
    """Return the lines of the [pipeline:main] pipeline = ... block."""
    lines = zope_ini.split("\n")
    out = []
    in_block = False
    for line in lines:
        if line.strip() == "[pipeline:main]":
            in_block = True
            continue
        if in_block:
            if line.startswith("[") and line.strip() != "pipeline =":
                break
            out.append(line)
    return "\n".join(out)


def test_generic_outer_filter_in_pipeline_and_block(cookies):
    """A user filter (default position=outer) appears before httpexceptions and gets a filter block."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "wsgi_filters": {
                "observability": {"use": "egg:plone.observability#observability"},
            },
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        pipeline = _pipeline_block(zope_ini)
        # appears in the pipeline, before the fixed httpexceptions entry
        assert "observability" in pipeline
        assert pipeline.index("observability") < pipeline.index("egg:Zope#httpexceptions")
        # outer => before built-in translogger (access_log default on)
        assert pipeline.index("observability") < pipeline.index("translogger")
        # filter block exists
        assert "[filter:observability]" in zope_ini
        assert "use = egg:plone.observability#observability" in zope_ini


def test_generic_inner_filter_after_translogger(cookies):
    """position=inner puts the filter after translogger, right before httpexceptions."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "wsgi_filters": {
                "dbg": {"use": "egg:foo#bar", "position": "inner"},
            },
        },
    ) as result:
        assert result.exit_code == 0
        pipeline = _pipeline_block((result.project_path / "etc" / "zope.ini").read_text())
        assert pipeline.index("translogger") < pipeline.index("dbg")
        assert pipeline.index("dbg") < pipeline.index("egg:Zope#httpexceptions")


def test_generic_filter_options_rendered_verbatim(cookies):
    """options keys render as verbatim key = value lines in the filter block."""
    with bake_in_temp_dir(
        cookies,
        extra_context={
            "wsgi_filters": {
                "myfilter": {"use": "egg:foo#bar", "options": {"threshold": "5", "mode": "fast"}},
            },
        },
    ) as result:
        assert result.exit_code == 0
        zope_ini = (result.project_path / "etc" / "zope.ini").read_text()
        assert "[filter:myfilter]" in zope_ini
        assert "use = egg:foo#bar" in zope_ini
        assert "threshold = 5" in zope_ini
        assert "mode = fast" in zope_ini
