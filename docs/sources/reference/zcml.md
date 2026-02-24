# ZCML

<!-- diataxis: reference -->

Settings for ZCML (Zope Configuration Markup Language) package loading and overrides.

:::{deprecated} 2.0
The `load_zcml` dict setting was replaced by individual `zcml_*` variables.
:::

| Setting | Default |
|---|---|
| `zcml_package_metas` | *(unset)* |
| `zcml_package_includes` | *(unset)* |
| `zcml_package_overrides` | *(unset)* |
| `zcml_include_file_location` | *(unset)* |
| `zcml_overrides_file_location` | *(unset)* |
| `zcml_resources_directory_location` | *(unset)* |
| `zcml_locales_directory_location` | *(unset)* |

**`zcml_package_metas`** -- A string with comma separated values of `meta.zcml` files from packages to include. Examples: `"my.fancypackage"` or `"myns.mypackage, collective.example"`.

**`zcml_package_includes`** -- A string with comma separated `configure.zcml` files from packages to include. Examples: `"my.fancypackage"` or `"myns.mypackage, collective.example"`.

**`zcml_package_overrides`** -- A string with comma separated `overrides.zcml` files from packages to include. Examples: `"my.fancypackage"` or `"myns.mypackage, collective.example"`.

**`zcml_include_file_location`** -- A (relative to `TARGET/etc`) path to a ZCML file to include.

**`zcml_overrides_file_location`** -- A (relative to `TARGET/etc`) path to an overrides ZCML file to include.

**`zcml_resources_directory_location`** -- A (relative to `TARGET/etc`) path to a Plone resource directory to include. Please refer to [plone.resource](https://pypi.org/project/plone.resource) for more details and setup instructions.

**`zcml_locales_directory_location`** -- Specify a (relative to `TARGET/etc`) locales directory. This registers a locales directory with extra or different translations. Given you want to override a few translations from the `plone` domain in the English language, add a `en/LC_MESSAGES/plone.po` file in this directory, with standard headers at the top, followed by something like this:

```po
#. Default: "You are here:"
msgid "you_are_here"
msgstr "You are very welcome here:"
```

Translations for other message ids are not affected and will continue to work.
