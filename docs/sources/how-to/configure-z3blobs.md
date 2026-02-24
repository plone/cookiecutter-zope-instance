# Configure S3 Blob Storage (z3blobs)

<!-- diataxis: how-to -->

This guide walks you through enabling S3-backed blob storage using
`zodb-s3blobs` as a wrapper around your existing ZODB storage backend.

## Prerequisites

- The `zodb-s3blobs` Python package installed
- An S3-compatible storage service (AWS S3, MinIO, Ceph, etc.)
- A bucket created for your blob data

## Step 1: Enable the wrapper

In your `instance.yaml`, enable the z3blobs wrapper alongside your existing
storage backend:

```yaml
default_context:
    db_storage: direct    # or relstorage, zeo
    db_z3blobs_enabled: true
```

## Step 2: Configure the S3 bucket

Provide the bucket name and a local cache directory:

```yaml
default_context:
    db_storage: direct
    db_z3blobs_enabled: true
    db_z3blobs_bucket_name: my-zodb-blobs
    db_z3blobs_cache_dir: var/s3cache
```

## Step 3: Configure S3 connection (if not AWS)

For MinIO or other S3-compatible stores, set the endpoint URL and credentials:

```yaml
default_context:
    db_storage: direct
    db_z3blobs_enabled: true
    db_z3blobs_bucket_name: my-zodb-blobs
    db_z3blobs_cache_dir: var/s3cache
    db_z3blobs_s3_endpoint_url: "http://minio:9000"
    db_z3blobs_s3_access_key: minioadmin
    db_z3blobs_s3_secret_key: minioadmin
    db_z3blobs_s3_use_ssl: false
    db_z3blobs_s3_addressing_style: path
```

## Example: z3blobs with RelStorage

```yaml
default_context:
    initial_user_name: admin
    initial_user_password: admin
    zcml_package_includes: my.addon

    # RelStorage backend
    db_storage: relstorage
    db_relstorage_postgresql_dsn: "dbname='zodb' host='db' port='5432'"

    # S3 blob wrapper
    db_z3blobs_enabled: true
    db_z3blobs_bucket_name: prod-blobs
    db_z3blobs_s3_region: eu-west-1
    db_z3blobs_cache_dir: /var/cache/s3blobs
    db_z3blobs_cache_size: 10GB
```

## Example: z3blobs with ZEO

```yaml
default_context:
    db_storage: zeo
    db_zeo_server: "zeo-server:8100"

    db_z3blobs_enabled: true
    db_z3blobs_bucket_name: prod-blobs
    db_z3blobs_cache_dir: /var/cache/s3blobs
```

## What happens to blob settings?

When z3blobs is enabled, the inner storage's blob directives (`blob-dir`,
`shared-blob-dir`, `blob-cache-size`, etc.) are **automatically suppressed**.
All blob operations are handled by the z3blobs wrapper instead.

## Important: not compatible with PGJsonb

z3blobs **cannot** be combined with `pgjsonb` storage. PGJsonb handles blobs
natively through its own `db_pgjsonb_s3_*` settings. If you need S3 blob
storage with PGJsonb, use the built-in S3 tiering instead. See
{doc}`configure-pgjsonb`.

## Next steps

- {doc}`/reference/database-z3blobs` -- Full reference for all z3blobs settings.
- {doc}`/explanation/blob-handling` -- How blobs work across different backends.
- {doc}`/explanation/storage-backends` -- Comparison of all storage backends.
