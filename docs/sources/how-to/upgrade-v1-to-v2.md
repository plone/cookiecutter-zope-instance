# Upgrade from Version 1 to Version 2

<!-- diataxis: how-to -->

This guide covers the breaking changes between cookiecutter-zope-instance
version 1.x and 2.x, and how to update your `instance.yaml` accordingly.

## Boolean values: string to native boolean

In version 1.x, the variables `debug_mode` and `verbose_security` expected
**string** values `"True"` or `"False"`. Since version 2.x, all boolean
settings use **native YAML booleans** `true` or `false`.

**Before (v1):**

```yaml
default_context:
    debug_mode: "True"
    verbose_security: "False"
```

**After (v2):**

```yaml
default_context:
    debug_mode: true
    verbose_security: false
```

## ZCML configuration: dict to flat variables

In version 1.x, ZCML settings were grouped under a single `load_zcml`
dictionary. Since version 2.x, each setting is a separate variable prefixed
with `zcml_`.

**Before (v1):**

```yaml
default_context:
    load_zcml:
        package_includes: "my.package, other.package"
        package_metas: "my.meta"
```

**After (v2):**

```yaml
default_context:
    zcml_package_includes: "my.package, other.package"
    zcml_package_metas: "my.meta"
```

## Version 2.1: `db_blobs_mode` renamed

In version 2.1, the setting `db_blobs_mode` was renamed to `db_blob_mode`
(without the trailing "s") for consistency. If you are upgrading from an early
2.0.x release, update this variable name as well.

## Pinning to the old version

If you are not ready to migrate, you can continue using the 1.x series:

```bash
cookiecutter -c 1.0.1 -f --no-input --config-file instance.yaml \
    gh:plone/cookiecutter-zope-instance
```

Check the
[releases page](https://github.com/plone/cookiecutter-zope-instance/releases)
for the latest 1-series version number.
