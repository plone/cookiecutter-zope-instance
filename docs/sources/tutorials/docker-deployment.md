# Docker Deployment

<!-- diataxis: tutorial -->

## What you will build

In this tutorial you will take a development configuration and transform it
into a production-ready Zope configuration using **environment variables**.
This is the standard pattern for containerized (Docker / Kubernetes)
deployments where secrets and runtime settings must not be baked into images.

## Prerequisites

- A working `instance.yaml` from the {doc}`first-zope-instance` tutorial.
- The `transform_from_environment.py` helper script (found in the `helpers/`
  directory of the cookiecutter template).
- Python 3.10+

## Step 1: Start with a development config

Use the same `instance.yaml` you created earlier:

```yaml
default_context:
    initial_user_name: 'admin'
    initial_user_password: 'admin'
    zcml_package_includes: my.awesome.addon
    db_storage: direct
```

This is your *base* configuration. Environment variables will override
individual values at build time.

## Step 2: Set production environment variables

The transform script recognizes variables prefixed with `INSTANCE_`. Each
variable name maps to a key in `default_context` -- the prefix is stripped
and the remainder becomes the key.

Export the following variables in your shell:

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
```

Notable choices:

- **Empty values** (`INSTANCE_wsgi_fast_listen=`,
  `INSTANCE_initial_user_password=`) clear the key -- the fast-listen port is
  disabled and no initial user is written.
- **`db_storage=relstorage`** switches from local FileStorage to RelStorage.
- **`db_relstorage_postgresql_dsn`** points at a `db` host -- the typical
  name for a database service in Docker Compose.

## Step 3: Run the transform

```bash
python transform_from_environment.py
```

The script reads `instance.yaml`, merges the `INSTANCE_*` variables on top,
and writes `instance-from-environment.yaml`.

## Step 4: Examine the output

The effective context will look like:

```yaml
default_context:
    initial_user_name: 'admin'
    initial_user_password: ''
    zcml_package_includes: my.awesome.addon
    db_storage: relstorage
    db_blob_mode: cache
    db_relstorage_keep_history: false
    db_relstorage: postgresql
    db_relstorage_postgresql_dsn: "host='db' dbname='plone' user='plone' password='verysecret'"
    wsgi_fast_listen: ''
    wsgi_listen: '127.0.0.1:8080'
    debug_mode: false
    verbose_security: false
```

Feed this into cookiecutter to generate the production instance directory:

```bash
cookiecutter -f --no-input \
    --config-file instance-from-environment.yaml \
    gh:plone/cookiecutter-zope-instance
```

## Step 5: Use in a Dockerfile

A typical Dockerfile pattern:

```dockerfile
FROM python:3.12-slim AS build

COPY instance.yaml /app/instance.yaml
COPY transform_from_environment.py /app/

WORKDIR /app

RUN pip install cookiecutter

ARG INSTANCE_db_storage=relstorage
ARG INSTANCE_db_relstorage=postgresql

RUN python transform_from_environment.py \
 && cookiecutter -f --no-input --config-file instance-from-environment.yaml \
        gh:plone/cookiecutter-zope-instance
```

For **runtime** overrides (secrets, DSN strings) prefer passing environment
variables via `docker run -e` or a Compose `environment:` block and running
the transform + cookiecutter as the container entrypoint.

## Advanced: Dict values with `_DICT_`

Some template variables are dictionaries. The transform script supports a
special `_DICT_` infix to set individual keys inside a dict:

```bash
export INSTANCE_environment_DICT_zope_i18n_compile_mo_files=true
export INSTANCE_environment_DICT_TZ=Europe/Berlin
```

This results in:

```yaml
environment:
    zope_i18n_compile_mo_files: 'true'
    TZ: 'Europe/Berlin'
```

## What you learned

- The `transform_from_environment.py` script bridges environment variables
  and the cookiecutter YAML configuration.
- Every `INSTANCE_<key>` variable maps to a `default_context` entry.
- Empty values clear a key -- useful for disabling features in production.
- The `_DICT_` infix lets you set individual entries inside dict-typed
  variables.
- Combining the transform with cookiecutter in a Dockerfile gives you
  reproducible, secret-safe Zope instance generation.
