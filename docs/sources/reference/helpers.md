# Helpers

<!-- diataxis: reference -->

Helper scripts for copy-paste usage in projects. Located in the `helpers/`
directory of the cookiecutter-zope-instance repository.

## `transform_from_environment.py`

Creates configuration from prefixed environment variables. This is useful for
containerized deployments.

**Precondition:** Python 3 with [PyYAML](https://pypi.org/project/PyYAML/)
installed.

The script takes a YAML configuration file as input and outputs a YAML
configuration file. Any environment variable with a given prefix (`INSTANCE_`
by default) is transformed into a configuration variable. The prefix is
stripped and the rest of the environment variable name either adds or replaces
the configuration variable name.

### Basic usage

Given a configuration file `instance.yaml`:

```yaml
default_context:
    wsgi_fast_listen: 0.0.0.0:8080
    initial_user_name: admin
    initial_user_password: admin
    debug_mode: true
    verbose_security: true
    zcml_package_includes: my.fancy.package
    db_storage: direct
```

Set environment variables for production:

```bash
export INSTANCE_wsgi_fast_listen=
export INSTANCE_wsgi_listen=127.0.0.1:8080
export INSTANCE_initial_user_password=
export INSTANCE_debug_mode=false
export INSTANCE_verbose_security=false
export INSTANCE_db_storage=relstorage
export INSTANCE_db_blob_mode=cache
export INSTANCE_db_relstorage_keep_history=false
export INSTANCE_db_relstorage=postgresql
export INSTANCE_db_relstorage_postgresql_dsn="host='db' dbname='plone' user='plone' password='verysecret'"
export INSTANCE_db_cache_size=50000
export INSTANCE_db_cache_size_bytes=1500MB
```

After calling the script in the directory of the configuration file, all
prefixed environment variables are transformed into a new configuration file
`instance-from-environment.yaml`:

```yaml
default_context:
    db_blob_mode: cache
    db_cache_size: '50000'
    db_cache_size_bytes: 1500MB
    db_relstorage: postgresql
    db_relstorage_keep_history: false
    db_relstorage_postgresql_dsn: host='db' dbname='plone' user='plone' password='verysecret'
    db_storage: relstorage
    debug_mode: false
    initial_user_name: admin
    initial_user_password: ''
    verbose_security: false
    wsgi_fast_listen: ''
    wsgi_listen: 127.0.0.1:8080
    zcml_package_includes: my.fancy.package
```

### Dict convention with `_DICT_`

To set dictionary/mapping values, the helper script supports `_DICT_` as a
separator. The environment variables:

```bash
export INSTANCE_a_DICT_b="value b"
export INSTANCE_a_DICT_c="value c"
```

will be transformed into:

```yaml
default_context:
    a:
        b: value b
        c: value c
```

This works recursively and updates existing values in the configuration file.
It is useful to modify the `environment` settings:

```bash
export INSTANCE_environment_DICT_PTS_LANGUAGES="de en"
export INSTANCE_environment_DICT_zope_i18n_allowed_languages="de en"
```

See {doc}`/how-to/use-environment-variables` for a step-by-step guide.
