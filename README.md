# cookiecutter-zope-instance

Cookiecutter template to create a full and complex configuration for a
[Zope](https://zope.org) 5 WSGI instance.

## Features

- Creates basic file-system structure with `zope.conf`, `zope.ini`, `site.zcml` and initial user
- Set Zope's main configuration options
- Configure different database backends: direct filestorage, RelStorage, ZEO, or PGJsonb
- CORS configuration for REST API usage
- Development and profiling options
- Environment-variable helper for containerized deployments

All non-ancient features of
[plone.recipe.zope2instance](https://pypi.org/project/plone.recipe.zope2instance/)
are provided plus new features.

## Quick Start

1. Install cookiecutter: `pip install cookiecutter`
2. Create an `instance.yaml`:

```yaml
default_context:
    initial_user_name: 'admin'
    initial_user_password: 'admin'
    zcml_package_includes: my.awesome.addon
    db_storage: direct
```

3. Run:

```bash
cookiecutter -f --no-input --config-file instance.yaml \
    gh:plone/cookiecutter-zope-instance
```

## Documentation

Full documentation is available at
**<https://plone.github.io/cookiecutter-zope-instance/>**

- [Tutorials](https://plone.github.io/cookiecutter-zope-instance/tutorials/) -- Step-by-step lessons
- [How-To Guides](https://plone.github.io/cookiecutter-zope-instance/how-to/) -- Task-focused solutions
- [Reference](https://plone.github.io/cookiecutter-zope-instance/reference/) -- All configuration options
- [Explanation](https://plone.github.io/cookiecutter-zope-instance/explanation/) -- Architecture and rationale

## Source Code & Contributions

- Repository: <https://github.com/plone/cookiecutter-zope-instance>
- Issues: <https://github.com/plone/cookiecutter-zope-instance/issues>
- Changelog: [CHANGES.md](CHANGES.md)

## License

GPL-2.0
