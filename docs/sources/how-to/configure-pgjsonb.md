# Configure PGJsonb Storage

<!-- diataxis: how-to -->

This guide walks you through setting up PGJsonb as your ZODB storage backend.
PGJsonb stores object state as PostgreSQL JSONB, making it queryable with
standard SQL operators.

## Prerequisites

- A running PostgreSQL 14+ server
- The `zodb-pgjsonb` and `zodb-json-codec` Python packages installed
- A PostgreSQL database created for your Zope instance

## Step 1: Set the storage type

In your `instance.yaml`, set the storage backend to `pgjsonb`:

```yaml
default_context:
    db_storage: pgjsonb
```

## Step 2: Configure the connection string

Provide the PostgreSQL DSN so the storage can connect to your database:

```yaml
default_context:
    db_storage: pgjsonb
    db_pgjsonb_dsn: "dbname='zodb' user='zodb' host='localhost' port='5433'"
```

URI format is also supported:

```yaml
default_context:
    db_pgjsonb_dsn: "postgresql://zodb:zodb@localhost:5433/zodb"
```

## Step 3: Choose history mode

By default, PGJsonb uses a history-free schema (no undo, better performance).
To enable ZODB-level undo support:

```yaml
default_context:
    db_storage: pgjsonb
    db_pgjsonb_dsn: "dbname='zodb' user='zodb' host='localhost' port='5433'"
    db_pgjsonb_history_preserving: true
```

## Complete example

```yaml
default_context:
    initial_user_name: admin
    initial_user_password: admin

    zcml_package_includes: my.awesome.addon

    # PGJsonb storage
    db_storage: pgjsonb
    db_pgjsonb_dsn: "dbname='zodb' user='zodb' host='db' port='5432'"
    db_pgjsonb_history_preserving: false

    # ZODB object cache
    db_cache_size: 50000
```

## Optional: S3 tiered blob storage

For deployments with many large blobs, you can tier blobs to S3-compatible
object storage:

```yaml
default_context:
    db_storage: pgjsonb
    db_pgjsonb_dsn: "dbname='zodb' user='zodb' host='db' port='5432'"
    db_pgjsonb_s3_bucket_name: my-zodb-blobs
    db_pgjsonb_s3_endpoint_url: "http://minio:9000"
    db_pgjsonb_s3_region: us-east-1
    db_pgjsonb_s3_access_key: minio-access-key
    db_pgjsonb_s3_secret_key: minio-secret-key
    db_pgjsonb_blob_threshold: 1MB
    db_pgjsonb_blob_cache_dir: /var/cache/zodb-blobs
    db_pgjsonb_blob_cache_size: 2GB
```

Blobs smaller than `db_pgjsonb_blob_threshold` remain in PostgreSQL `bytea`.
Set the threshold to `0` to send all blobs to S3.

## Important: blob settings not used with PGJsonb

The generic blob settings `db_blob_mode` and `db_blob_location` are **not
used** with PGJsonb. PGJsonb manages blob storage through its own settings
(`db_pgjsonb_blob_*` and `db_pgjsonb_s3_*`).

## Next steps

- {doc}`/reference/database-pgjsonb` -- Full reference for all PGJsonb
  options including connection pool, cache, and S3 settings.
- {doc}`/explanation/storage-backends` -- Comparison of all storage backends.
- {doc}`/explanation/blob-handling` -- How blobs work across different
  backends.
