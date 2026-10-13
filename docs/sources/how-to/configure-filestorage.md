# Configure direct filestorage

<!-- diataxis: how-to -->

This guide shows you how to configure the `direct` (FileStorage) backend, in
which a single process opens a local `Data.fs` file directly without a
database server.
This is the default backend and the simplest option for development and
single-process deployments.

## Prerequisites

- New to this template? Start with {doc}`/tutorials/first-zope-instance`.

## Step 1: set the storage type

In your `instance.yaml`, set the storage backend to `direct`:

```yaml
default_context:
    db_storage: direct
```

`direct` is the default, so this line is optional.
Set it explicitly to make the choice clear.

## Step 2: set the data file location

Point `db_filestorage_location` at the path for the `Data.fs` file.
Lock and index files (`Data.fs.*`) are created alongside it.

```yaml
default_context:
    db_storage: direct
    db_filestorage_location: var/filestorage/Data.fs
```

When unset, the file defaults to a `filestorage/Data.fs` path inside the
instance's client home.

## Step 3: tune packing and safety (optional)

Control how packing and database creation behave:

```yaml
default_context:
    db_storage: direct
    db_filestorage_location: var/filestorage/Data.fs

    # Keep a .old copy of the database before packing
    db_filestorage_pack_keep_old: true

    # Skip garbage collection during packing for speed
    db_filestorage_pack_gc: true

    # Fail to start if the file is missing instead of creating it
    db_filestorage_create: false
```

To serve a read-only replica, open the storage in read-only mode:

```yaml
default_context:
    db_storage: direct
    db_filestorage_read_only: true
```

## Complete example

```yaml
default_context:
    # Serving
    wsgi_listen: localhost:8080

    initial_user_name: admin
    initial_user_password: admin

    zcml_package_includes: my.awesome.addon

    # Storage
    db_storage: direct
    db_filestorage_location: var/filestorage/Data.fs
```

For the full set of annotated sample configurations, including the other
backends, see {doc}`/reference/sample-configurations`.

## Next steps

- {doc}`/reference/database-direct` -- Full reference for all filestorage
  options including quota, packer, and read-only settings.
- {doc}`migrate-storage` -- Migrate data between filestorage and other
  backends using `zodb-convert`.
- {doc}`/explanation/storage-backends` -- Comparison of all storage backends.
