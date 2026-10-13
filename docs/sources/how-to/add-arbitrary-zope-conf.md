# Add arbitrary zope.conf settings

<!-- diataxis: how-to -->

Sometimes `zope.conf` needs configuration this template has no option for, such as an
additional ZODB mount. Instead of patching the generated file, keep those settings in a
file you own and let the generated `zope.conf` pull it in via
[ZConfig's](https://zconfig.readthedocs.io/) `%include` directive.

## Example: a temporary storage for sessions

Create a file next to your instance, e.g. `instance/etc/zope-conf-additional.conf`:

```
<zodb_db temporary>
    <temporarystorage>
    name Temporary database (for sessions)
    </temporarystorage>
    mount-point /temp_folder
    container-class Products.TemporaryFolder.TemporaryContainer
</zodb_db>
```

Then configure:

```yaml
default_context:
  zope_conf_include_file_location: "instance/etc/zope-conf-additional.conf"
```

The generated `zope.conf` ends with:

```
%include /path/to/output-dir/instance/etc/zope-conf-additional.conf
```

Your file is never touched by the generator, so it survives re-generation.

## Notes

- A relative path is anchored at the cookiecutter output directory (the parent of the
  instance directory); an absolute path is used as-is.
- The included file has to exist when Zope starts; ZConfig fails otherwise. It does not
  need to exist when the configuration is generated.
- The include is rendered at the end of `zope.conf`. It can contain sections
  (`<zodb_db>`, `<product-config>`, ...) as well as top-level directives, and may itself
  use further `%include` lines.
- The example above additionally requires the `tempstorage` and
  `Products.TemporaryFolder` packages. Session support via temporary storage is fine to
  use again; the reliability issue that once discouraged it was fixed in
  [tempstorage](https://github.com/zopefoundation/tempstorage/pull/16).
