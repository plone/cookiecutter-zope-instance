# Use Environment Variables for Configuration

<!-- diataxis: how-to -->

This guide shows how to use the `transform_from_environment.py` helper script
to override `instance.yaml` settings with environment variables. This pattern
is essential for containerized (Docker/Kubernetes) deployments.

## Step 1: Copy the helper script

The `transform_from_environment.py` script is located in the `helpers/`
directory of the cookiecutter-zope-instance repository. Copy it into your
project:

```bash
cp cookiecutter-zope-instance/helpers/transform_from_environment.py .
```

The script requires Python 3 with
[PyYAML](https://pypi.org/project/PyYAML/) installed.

## Step 2: Prepare a base development configuration

Create your base `instance.yaml` for local development:

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

## Step 3: Set environment variables for production

Every environment variable with the `INSTANCE_` prefix (configurable) is
picked up by the transform script. The prefix is stripped and the remaining
name becomes the configuration key:

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

Setting a variable to an empty string effectively clears that value.

## Step 4: Run the transform script

```bash
python3 transform_from_environment.py
```

This produces `instance-from-environment.yaml` that merges the base file with
all `INSTANCE_*` overrides.

## Step 5: Use the generated file with cookiecutter

```bash
cookiecutter -f --no-input --config-file instance-from-environment.yaml \
    gh:plone/cookiecutter-zope-instance
```

## Dict convention with `_DICT_` separator

To set dictionary/mapping values (such as the `environment` setting), use
`_DICT_` as a separator:

```bash
export INSTANCE_environment_DICT_PTS_LANGUAGES="de en"
export INSTANCE_environment_DICT_zope_i18n_allowed_languages="de en"
```

## Docker integration pattern

A typical Dockerfile pattern:

```dockerfile
FROM python:3.12-slim

COPY instance.yaml /app/instance.yaml
COPY transform_from_environment.py /app/transform_from_environment.py

WORKDIR /app

CMD python3 transform_from_environment.py && \
    cookiecutter -f --no-input \
        --config-file instance-from-environment.yaml \
        gh:plone/cookiecutter-zope-instance && \
    runwsgi instance/etc/zope.ini
```

In your `docker-compose.yml` or Kubernetes manifests, set `INSTANCE_*`
environment variables to configure each deployment.

## Next steps

- {doc}`/reference/helpers` -- Reference documentation for helper scripts.
