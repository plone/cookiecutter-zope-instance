# Configure RelStorage with PostgreSQL

<!-- diataxis: how-to -->

This guide walks you through setting up RelStorage with PostgreSQL as your
ZODB storage backend. RelStorage stores pickles in a relational database and
is the recommended backend for production Plone deployments that need
horizontal scaling.

## Prerequisites

- A running PostgreSQL server
- The `RelStorage` and `psycopg2` Python packages installed
- A PostgreSQL database created for your Zope instance

## Step 1: Set the storage type

In your `instance.yaml`, set the storage backend to `relstorage`:

```yaml
default_context:
    db_storage: relstorage
```

## Step 2: Set the blob mode

RelStorage stores blobs in the database. Your Zope client needs a local cache
directory for blob data. Set the blob mode to `cache`:

```yaml
default_context:
    db_storage: relstorage
    db_blob_mode: cache
```

```{important}
You **must** set `db_blob_mode` to `cache` when using RelStorage.
The default value `shared` is only appropriate for direct filestorage.
```

## Step 3: Choose the database backend

Set the relational database type. PostgreSQL is the recommended choice:

```yaml
default_context:
    db_storage: relstorage
    db_blob_mode: cache
    db_relstorage: postgresql
```

Other supported values are `mysql`, `oracle`, and `sqlite3`.

## Step 4: Configure the connection string

Provide the PostgreSQL DSN (Data Source Name) so RelStorage can connect to
your database:

```yaml
default_context:
    db_storage: relstorage
    db_blob_mode: cache
    db_relstorage: postgresql
    db_relstorage_postgresql_dsn: "host='localhost' dbname='plone' user='plone' password='secret'"
```

## Complete example

Here is a production-ready `instance.yaml` with commonly tuned settings:

```yaml
default_context:
    initial_user_name: admin
    initial_user_password: admin

    zcml_package_includes: my.awesome.addon

    # Storage
    db_storage: relstorage
    db_blob_mode: cache
    db_relstorage: postgresql
    db_relstorage_postgresql_dsn: "host='db' dbname='plone' user='plone' password='secret'"

    # Performance tuning
    db_cache_size: 50000
    db_cache_size_bytes: 1500MB
    db_relstorage_keep_history: false

    # Blob cache
    db_blob_cache_size: 10737418240  # 10 GB
```

## Generated helper files

When you use RelStorage, the cookiecutter also generates configuration files
for RelStorage command-line utilities:

- **`relstorage-pack.conf`** -- Always generated. Used with the `zodbpack`
  command for database packing and garbage collection.
- **`relstorage-export.conf`** -- Generated when `db_relstorage_export_*`
  settings are provided. Used with `zodbconvert` to export data to a
  filestorage.
- **`relstorage-import.conf`** -- Generated when `db_relstorage_import_*`
  settings are provided. Used with `zodbconvert` to import data from a
  filestorage.

:::{tip}
For migrating data between storage backends, the generic
[zodb-convert](https://pypi.org/project/zodb-convert/) tool is now the
recommended approach. It works with all storage backends and can read storage
configuration directly from `zope.conf` files.
See {doc}`migrate-storage` for a step-by-step guide.
:::

## Next steps

- {doc}`migrate-storage` -- Migrate data between any storage backends using
  `zodb-convert`.
- {doc}`/reference/database-relstorage` -- Full reference for all RelStorage
  options including caching, replication, MySQL, Oracle, and SQLite settings.
- {doc}`/explanation/storage-backends` -- Comparison of all storage backends.
