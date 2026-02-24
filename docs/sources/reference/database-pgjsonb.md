# Database: PGJsonb

<!-- diataxis: reference -->

[zodb-pgjsonb](https://pypi.org/project/zodb-pgjsonb/) is a ZODB storage
adapter that stores object state as PostgreSQL JSONB with binary blobs in
PostgreSQL bytea (or optionally tiered to S3-compatible object storage). It
uses [zodb-json-codec](https://pypi.org/project/zodb-json-codec/) for
Rust-based pickle-to-JSON transcoding.

:::{note}
Blobs are handled differently from RelStorage and ZEO. The `db_blob_mode` and
`db_blob_location` settings are **not used** with PGJsonb.
:::

## Core Settings

`db_pgjsonb_dsn`
: PostgreSQL connection string in libpq key=value format or URI format.

  Examples:

  - `dbname='zodb' user='zodb' host='localhost' port='5433'`
  - `postgresql://zodb:zodb@localhost:5433/zodb`

  **Default:** unset, empty string. **Required** when `db_storage` is `pgjsonb`.

`db_pgjsonb_name`
: Storage name used in sort keys and logging.

  **Default:** `pgjsonb`

`db_pgjsonb_history_preserving`
: Enable history-preserving mode with undo support. A history-preserving
  schema supports ZODB-level undo, but grows more quickly and requires regular
  packing. If switched off (the default), the storage uses a history-free
  schema -- faster, but no undo support.

  Allowed values: `true`, `false`

  **Default:** `false`

## Connection Pool

`db_pgjsonb_pool_size`
: Minimum number of connections in the instance connection pool. Set to `0`
  for on-demand creation.

  **Default:** unset, empty string, storage default of `1` is active

`db_pgjsonb_pool_max_size`
: Maximum number of connections in the instance connection pool.

  **Default:** unset, empty string, storage default of `10` is active

`db_pgjsonb_pool_timeout`
: Connection pool acquisition timeout in seconds. Raises a `StorageError` if
  a connection cannot be acquired within this time.

  **Default:** unset, empty string, storage default of `30.0` is active

## Object Cache

`db_pgjsonb_cache_local_mb`
: Per-instance object cache size in megabytes. Caches `load()` results (pickle
  bytes) to avoid repeated PostgreSQL round-trips and JSONB transcoding. Set
  to `0` to disable.

  **Default:** unset, empty string, storage default of `16` is active

## Blob Settings

`db_pgjsonb_blob_temp_dir`
: Directory for temporary blob files during transactions. Auto-created in
  system temp directory if omitted.

  **Default:** unset, empty string

## S3 Tiered Blob Storage

These settings enable tiered blob storage: blobs exceeding the threshold are
stored in S3-compatible object storage instead of PostgreSQL bytea. Requires
the `zodb-pgjsonb[s3]` extra to be installed.

`db_pgjsonb_s3_bucket_name`
: S3 bucket name for large blob storage. If omitted, all blobs are stored in
  PostgreSQL bytea.

  **Default:** unset, empty string

`db_pgjsonb_s3_prefix`
: S3 key prefix for namespace isolation (e.g. `myapp/blobs/`).

  **Default:** unset, empty string

`db_pgjsonb_s3_endpoint_url`
: S3 endpoint URL for MinIO, Ceph, or other S3-compatible stores (e.g.
  `http://localhost:9000`).

  **Default:** unset, empty string. Uses AWS S3 if omitted.

`db_pgjsonb_s3_region`
: AWS region name (e.g. `us-east-1`). Uses boto3 default if omitted.

  **Default:** unset, empty string

`db_pgjsonb_s3_access_key`
: AWS access key ID. Uses boto3 credential chain (IAM role,
  `~/.aws/credentials`, environment variables) if omitted.

  **Default:** unset, empty string

`db_pgjsonb_s3_secret_key`
: AWS secret access key. Uses boto3 credential chain if omitted.

  **Default:** unset, empty string

`db_pgjsonb_s3_use_ssl`
: Enable SSL/TLS for S3 connections.

  Allowed values: `true`, `false`

  **Default:** `true`

`db_pgjsonb_blob_threshold`
: Blobs larger than this are stored in S3 (if configured). Blobs smaller than
  this stay in PostgreSQL bytea. Set to `0` to send all blobs to S3. Only
  effective when `db_pgjsonb_s3_bucket_name` is set.

  Allowed values: byte-size (integer format with postfix KB, MB, GB)

  **Default:** unset, empty string, storage default of `1MB` is active

`db_pgjsonb_blob_cache_dir`
: Local cache directory for S3 blobs. Recommended for production to avoid
  repeated S3 downloads. Falls back to `db_pgjsonb_blob_temp_dir` if omitted.

  **Default:** unset, empty string

`db_pgjsonb_blob_cache_size`
: Maximum size of local blob cache.

  Allowed values: byte-size (integer format with postfix KB, MB, GB)

  **Default:** unset, empty string, storage default of `1GB` is active
