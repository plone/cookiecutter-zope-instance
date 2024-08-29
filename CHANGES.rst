Changelog
=========

2.1.2 (unreleased)
------------------

- Fix typo in docs: it is not ``zcml_package_meta`` singular, but ``zcml_package_metas`` plural.
  [@mauritsvanrees, 2024-08-29]

- Fix typo in deprecation warning: there was never a ``zcml`` dict setting, only ``load_zcml`.
  [@mauritsvanrees, 2024-08-29]

2.1.1
-----

- Fix broken handling of `blob-cache-size` and `blob-cache-size-check`.
  [@jensens, 2024-07-01]

- Fix: Introduce consistent naming of all `db_blob_*` and deprecate all `db_blobs_*`.
  [@jensens, 2024-07-01]

- Add a footer to all generated files to make clear where they come from, include version of `cookiecutter-zope-instance`.
  [@jensens, 2024-07-01]

2.1.0
-----

- Feature: Add cors support by generating a `cors.zcml` if enabled.
  [@jensens, 2024-03-06]

2.0.1
-----

- Fix: Implement a fallback to old zcml configurations Fixes #18.
  [@ericof, 2024-03-01]

2.0
---

- Feature: Implement #14 Generate RelStorage specific pack/import/export configuration.
  [@jensens, 2024-02-21]

- Feature: Helper script to transform an input configuration file for
  cookie-cutter-zopeinstance from environment variables with a given prefix
  and output the result to a file.
  [@jensens, 2024-01-22]

- Feature: Generate absolute paths in outputs.
  Fixes https://github.com/plone/cookiecutter-zope-instance/issues/5
  [@me-kell, @jensens, 2024-01-22]

- Breaking: Flatten zcml variables dict to multiple variables prefixed with zcml.
  This allows for modification of variables in Docker entry points.
  [@jensens, 2024-01-21]

- Bugfix: Boolean values in configuration are always true or false (bool).
  Unified for verbose_security and debug_mode.
  [@jensens, 2024-01-21]

- Bugfix: typo `db_relstorage_orcale_*` in `cookiecutter.json` fixed.
  [@mliebischer, @jensens, 2024-02-28]

- Bugfix: `profile_repoze_*` settings were not taken into account.
  [@mliebischer, @jensens, 2024-02-28]

- Bugfix: Remove unused setting `deprecation_warnings` from `cookiecutter.json`.
  [@mliebischer, @jensens, 2024-02-28]


1.0
---

- Feature: Add `dos_protection_*` settings for feature introduced in https://github.com/zopefoundation/Zope/pull/1142
  [@jensens, 2023-10-25]

- Bugfix: Loading of `overrides.zcml`` and `meta.zcml`.
  [@jensens, 2022-02-07]

- Initial work.
  [@jensens]
