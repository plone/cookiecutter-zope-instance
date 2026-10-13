from utils import bake_in_temp_dir

import xml.etree.ElementTree as ET


def _site_zcml(result):
    return (result.project_path / "etc" / "site.zcml").read_text()


def test_site_zcml_is_well_formed_by_default(cookies):
    """The generated site.zcml parses with no options set."""
    with bake_in_temp_dir(cookies) as result:
        assert result.exit_code == 0
        ET.fromstring(_site_zcml(result))


def test_resources_directory_declares_the_plone_prefix(cookies):
    """zcml_resources_directory_location renders <plone:static/>, so the
    plone: prefix has to be bound or the file is not well-formed XML and
    Zope will not start."""
    with bake_in_temp_dir(
        cookies,
        extra_context={"zcml_resources_directory_location": "/some/dir"},
    ) as result:
        assert result.exit_code == 0
        zcml = _site_zcml(result)
        assert "plone:static" in zcml
        ET.fromstring(zcml)


def test_locales_directory_declares_the_i18n_prefix(cookies):
    """Likewise zcml_locales_directory_location renders
    <i18n:registerTranslations/>."""
    with bake_in_temp_dir(
        cookies,
        extra_context={"zcml_locales_directory_location": "/some/locales"},
    ) as result:
        assert result.exit_code == 0
        zcml = _site_zcml(result)
        assert "i18n:registerTranslations" in zcml
        ET.fromstring(zcml)
