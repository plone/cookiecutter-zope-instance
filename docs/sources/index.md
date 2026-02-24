# cookiecutter-zope-instance

<!-- diataxis: landing -->

Cookiecutter template to create a full and complex configuration for a
[Zope](https://zope.org) 5 WSGI instance.

**Key capabilities:**

- Creates `zope.conf`, `zope.ini`, `site.zcml` and initial user
- Configures WSGI server (Waitress) settings
- Supports four database backends: direct filestorage, RelStorage, ZEO, PGJsonb
- CORS configuration for REST API usage
- Development and profiling options
- Environment-variable helper for containerized deployments

All non-ancient features of [plone.recipe.zope2instance](https://pypi.org/project/plone.recipe.zope2instance/) are provided plus new features.

**Requirements:** Python 3.10+, [cookiecutter](https://cookiecutter.readthedocs.io)

## Documentation

::::{grid} 2
:gutter: 3

:::{grid-item-card} Tutorials
:link: tutorials/index
:link-type: doc

**Learning-oriented** -- Step-by-step lessons to build skills.

*Start here if you are new to cookiecutter-zope-instance.*
:::

:::{grid-item-card} How-To Guides
:link: how-to/index
:link-type: doc

**Goal-oriented** -- Solutions to specific problems.

*Use these when you need to accomplish something.*
:::

:::{grid-item-card} Reference
:link: reference/index
:link-type: doc

**Information-oriented** -- All configuration options documented.

*Consult when you need detailed information.*
:::

:::{grid-item-card} Explanation
:link: explanation/index
:link-type: doc

**Understanding-oriented** -- Architecture and design decisions.

*Read to deepen your understanding of how it works.*
:::

::::

## Quick Start

1. Install cookiecutter: `pip install cookiecutter`
2. Create an `instance.yaml` with your settings
3. Run: `cookiecutter -f --no-input --config-file instance.yaml gh:plone/cookiecutter-zope-instance`

See {doc}`tutorials/first-zope-instance` for a complete walkthrough.

```{toctree}
---
maxdepth: 3
caption: Documentation
titlesonly: true
hidden: true
---
tutorials/index
how-to/index
reference/index
explanation/index
```
