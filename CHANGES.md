# Changelog

## 2.4.1 (unreleased)

- No changes yet.

## 2.4.0 (2026-02-25)

- Feature: Add `trusted_proxy` setting for reverse proxy IP configuration
  (renders as `trusted-proxy` directives in `zope.conf`).
  [@jensens]

- Feature: Add `product_config` setting (dict of dicts) for Zope
  `<product-config>` addon configuration sections.
  [@jensens]

- Feature: Add `datetime_format` setting for Zope `datetime-format` directive
  (`us` or `international`).
  [@jensens]

- Feature: Add `dos_protection_form_part_limit` setting for the maximum number
  of parts in multipart POST requests (Zope 5.10+).
  [@jensens]

- Feature: Add `db_pool_timeout` setting for ZODB connection pool idle timeout.
  [@jensens]

- Feature: Add `db_filestorage_create` and `db_filestorage_read_only` settings
  for FileStorage.
  [@jensens]

- Feature: Add `db_relstorage_name` and `db_relstorage_pack_gc` settings
  for RelStorage.
  [@jensens]

- Feature: Add `db_zeo_client_label`, `db_zeo_storage`, and `db_zeo_wait`
  settings for ZEO client configuration.
  [@jensens]

- Feature: Add `wsgi_channel_timeout` setting for Waitress idle connection
  timeout.
  [@jensens]

- Feature: Add optional `locale` setting to configure the Zope `locale`
  directive in `zope.conf`.
  Closes [#29](https://github.com/plone/cookiecutter-zope-instance/issues/29).
  [@jensens]

- Fix: Oracle RelStorage configuration was broken -- `db_relstorage_oracle_password`
  had a typo (`oraclce`) in `cookiecutter.json` and `db_relstorage_oracle_driver`
  was missing entirely.
  [@jensens]

- Fix: Deprecated `db_blobs_location` was ignored for `direct` (filestorage)
  backend -- the macro call passed `cookiecutter.db_blob_location` directly
  instead of the fallback variable. `relstorage` and `zeo` were not affected.
  Closes [#25](https://github.com/plone/cookiecutter-zope-instance/issues/25).
  [@jensens]

- Fix: Add `pythonpath = .` to `pytest.ini` so tests also work when running
  `pytest` directly (not only via `tox`).

## 2.3.0 (2026-02-24)

- Feature: Add `zodb-s3blobs` support as an S3 blob storage wrapper for
  `direct`, `relstorage`, and `zeo` backends. Enable via
  `db_z3blobs_enabled: true`. Not compatible with `pgjsonb` (which handles
  blobs natively).
  [@jensens]

- Feature: Add `pgjsonb` as a new database storage backend using
  `zodb-pgjsonb` with PostgreSQL JSONB and optional S3 blob tiering.
  Closes [#30](https://github.com/plone/cookiecutter-zope-instance/issues/30).
  [@jensens]

- Feature: Migrate documentation from monolithic README.rst to Sphinx with
  Diataxis framework (tutorials, how-to guides, reference, explanation).
  Published via GitHub Pages with `llms.txt` for AI agent discovery.
  [@jensens]

## 2.2.1 (2025-03-25)

- Fix: For Zope versions below 5.13 the setting `enable_xmlrpc` should not be
  set since it does not exist. It now renders only if set to false.
  [@jensens, 2025-03-25]

## 2.2.0 (2025-03-25)

- Feature: Introduce settings: http_realm, max_conflict_retries,
  webdav_source_port, enable_xmlrpc, enable_ms_public_header,
  debug_exceptions.
  [@jensens, 2025-03-25]

## 2.1.3 (2025-03-03)

- Feature: configurable `wsgi_app_entrypoint`.
  [@jensens, 2025-03-03]

## 2.1.2

- Fix typo in docs: it is not `zcml_package_meta` singular, but
  `zcml_package_metas` plural.
  [@mauritsvanrees, 2024-08-29]

- Fix typo in deprecation warning: there was never a `zcml` dict setting,
  only `load_zcml`.
  [@mauritsvanrees, 2024-08-29]

## 2.1.1

- Fix broken handling of `blob-cache-size` and `blob-cache-size-check`.
  [@jensens, 2024-07-01]

- Fix: Introduce consistent naming of all `db_blob_*` and deprecate all
  `db_blobs_*`.
  [@jensens, 2024-07-01]

- Add a footer to all generated files to make clear where they come from,
  include version of `cookiecutter-zope-instance`.
  [@jensens, 2024-07-01]

## 2.1.0

- Feature: Add cors support by generating a `cors.zcml` if enabled.
  [@jensens, 2024-03-06]

## 2.0.1

- Fix: Implement a fallback to use `load_zcml` dict configuration,
  effectively making the breaking change of its removal in 2.0.0 a
  deprecation instead. Fixes #18.
  [@ericof, 2024-03-01]

## 2.0

- Feature: Implement #14 Generate RelStorage specific pack/import/export
  configuration.
  [@jensens, 2024-02-21]

- Feature: Helper script to transform an input configuration file for
  cookiecutter-zope-instance from environment variables with a given prefix
  and output the result to a file.
  [@jensens, 2024-01-22]

- Feature: Generate absolute paths in outputs.
  Fixes https://github.com/plone/cookiecutter-zope-instance/issues/5
  [@me-kell, @jensens, 2024-01-22]

- Breaking: Flatten zcml variables dict to multiple variables prefixed with
  zcml. This allows for modification of variables in Docker entry points.
  [@jensens, 2024-01-21]

- Bugfix: Boolean values in configuration are always true or false (bool).
  Unified for verbose_security and debug_mode.
  [@jensens, 2024-01-21]

- Bugfix: typo `db_relstorage_orcale_*` in `cookiecutter.json` fixed.
  [@mliebischer, @jensens, 2024-02-28]

- Bugfix: `profile_repoze_*` settings were not taken into account.
  [@mliebischer, @jensens, 2024-02-28]

- Bugfix: Remove unused setting `deprecation_warnings` from
  `cookiecutter.json`.
  [@mliebischer, @jensens, 2024-02-28]

## 1.0

- Feature: Add `dos_protection_*` settings for feature introduced in
  https://github.com/zopefoundation/Zope/pull/1142
  [@jensens, 2023-10-25]

- Bugfix: Loading of `overrides.zcml` and `meta.zcml`.
  [@jensens, 2022-02-07]

- Initial work.
  [@jensens]
