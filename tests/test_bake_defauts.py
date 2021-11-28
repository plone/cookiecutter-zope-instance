from .utils import bake_in_temp_dir


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project_path.is_dir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.name for f in result.project_path.iterdir()]
        assert 'etc' in found_toplevel_files
        etc_path = result.project_path / "etc"
        assert etc_path.is_dir()
        etc_files = [f.name for f in etc_path.iterdir()]
        assert 'zope.conf' in etc_files
        assert 'zope.ini' in etc_files
        assert 'site.zcml' in etc_files

