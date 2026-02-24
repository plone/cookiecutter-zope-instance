# Why Cookiecutter for Zope Configuration?

<!-- diataxis: explanation -->

This page explains the rationale behind using
[cookiecutter](https://cookiecutter.readthedocs.io) as the configuration
engine for Zope instances, replacing the older buildout-based approach.

## The problem: replacing buildout

For many years, the Plone and Zope community used
[buildout](https://www.buildout.org/) with the
[plone.recipe.zope2instance](https://pypi.org/project/plone.recipe.zope2instance/)
recipe to generate Zope instance configurations. While functional, this
approach had drawbacks:

- Buildout is a complex tool with a steep learning curve
- The recipe used Python string templates that were not intuitive to write or
  maintain
- Configuration generation was tightly coupled to the buildout execution model
- The broader Python ecosystem has moved away from buildout toward standard
  packaging tools (pip, setuptools, etc.)

## The idea: cookiecutter

[Cookiecutter](https://cookiecutter.readthedocs.io) is a widely used,
well-maintained utility for creating text-based file-system structures from
templates. It uses Jinja2 templating and accepts configuration via YAML
files, making it a natural fit for generating Zope configuration files.

The `cookiecutter-zope-instance` template wraps cookiecutter with the
specific knowledge needed to produce correct `zope.conf`, `zope.ini`,
`site.zcml`, and related files.

## Differences from the old recipe

### Variable names

Variable names have been redesigned to use a consistent namespace convention.
As the Zen of Python says: *"Namespaces are one honking great idea -- let's
do more of those!"*

Variables are grouped by prefix:

- `db_*` -- Database settings
- `db_relstorage_*` -- RelStorage-specific settings
- `db_zeo_*` -- ZEO-specific settings
- `db_pgjsonb_*` -- PGJsonb-specific settings
- `cors_*` -- CORS settings
- `zcml_*` -- ZCML inclusion settings
- `wsgi_*` -- WSGI server settings

### Sentry integration

The old recipe included built-in Sentry configuration. This has been removed
in favor of using
[collective.sentry](https://pypi.org/project/collective.sentry/), which
provides a much better integration as a standalone package.

### The `ctl.py` script

The old recipe generated a control script. For modern workflows, consider
using [mxmake](https://pypi.org/project/mxmake/), which already has built-in
support for `cookiecutter-zope-instance`.

## Contributors

The idea and initial implementation came from Jens Klein
([Klein & Partner KG](https://kleinundpartner.at) of
[BlueDynamics Alliance](https://bluedynamics.com)). The project was then
donated to the Plone Foundation and is maintained by the Plone community.

See the
[contributors graph](https://github.com/plone/cookiecutter-zope-instance/graphs/contributors)
for all contributors.
