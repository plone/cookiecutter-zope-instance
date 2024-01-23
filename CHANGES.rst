Changelog
=========

2.0
---

- Feature: Helper script to transform an input configuration file for
  cookie-cutter-zopeinstance from environment variables with a given prefix
  and output the result to a file.
  [@jensens, 2024-01-22]

- Generate absolute paths in outputs.
  Fixes https://github.com/plone/cookiecutter-zope-instance/issues/5
  [@me-kell, @jensens, 2024-01-22]

- Flatten zcml variables dict to multiple variables prefixed with zcml.
  This allows for modification of variables in Docker entry points.
  [@jensens, 2024-01-21]

- Boolean values in configuration are always true or false (bool).
  Unified for verbose_security and debug_mode.
  [@jensens, 2024-01-21]


1.0
---

- Add `dos_protection_*` settings for feature introduced in https://github.com/zopefoundation/Zope/pull/1142
  [@jensens, 2023-10-25]

- Fix loading of `overrides.zcml`` and `meta.zcml`.
  [@jensens, 2022-02-07]

- Initial work.
  [@jensens]
