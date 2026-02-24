# Database: PGJsonb

<!-- diataxis: reference -->

[zodb-pgjsonb](https://pypi.org/project/zodb-pgjsonb/) is a ZODB storage
adapter optimized for cloud-native environments. It stores object state as
PostgreSQL JSONB with binary blobs in PostgreSQL bytea (or optionally tiered
to S3-compatible object storage), making it a natural fit for managed
PostgreSQL services (RDS, Cloud SQL, AlloyDB, etc.). It uses
[zodb-json-codec](https://pypi.org/project/zodb-json-codec/) for Rust-based
pickle-to-JSON transcoding.

:::{note}
Blobs are handled differently from RelStorage and ZEO. The `db_blob_mode` and
`db_blob_location` settings are **not used** with PGJsonb.
:::

## Core Settings

| Setting | Default | Allowed Values |
|---|---|---|
| `db_pgjsonb_dsn` | *(unset, **required**)* | libpq DSN or URI |
| `db_pgjsonb_name` | `pgjsonb` | string |
| `db_pgjsonb_history_preserving` | `false` | `true`, `false` |

**`db_pgjsonb_dsn`** -- PostgreSQL connection string in libpq key=value format or URI format. Examples: `dbname='zodb' user='zodb' host='localhost' port='5433'` or `postgresql://zodb:zodb@localhost:5433/zodb`. **Required** when `db_storage` is `pgjsonb`.

**`db_pgjsonb_history_preserving`** -- Enable history-preserving mode with undo support. A history-preserving schema supports ZODB-level undo, but grows more quickly and requires regular packing. If switched off (the default), the storage uses a history-free schema -- faster, but no undo support.

## Connection Pool

| Setting | Default |
|---|---|
| `db_pgjsonb_pool_size` | *(unset, default `1`)* |
| `db_pgjsonb_pool_max_size` | *(unset, default `10`)* |
| `db_pgjsonb_pool_timeout` | *(unset, default `30.0`s)* |

**`db_pgjsonb_pool_size`** -- Minimum number of connections in the instance connection pool. Set to `0` for on-demand creation.

**`db_pgjsonb_pool_max_size`** -- Maximum number of connections in the instance connection pool.

**`db_pgjsonb_pool_timeout`** -- Connection pool acquisition timeout in seconds. Raises a `StorageError` if a connection cannot be acquired within this time.

## Object Cache

| Setting | Default |
|---|---|
| `db_pgjsonb_cache_local_mb` | *(unset, default `16`)* |

**`db_pgjsonb_cache_local_mb`** -- Per-instance object cache size in megabytes. Caches `load()` results (pickle bytes) to avoid repeated PostgreSQL round-trips and JSONB transcoding. Set to `0` to disable.

## Blob Settings

| Setting | Default |
|---|---|
| `db_pgjsonb_blob_temp_dir` | *(unset)* |

**`db_pgjsonb_blob_temp_dir`** -- Directory for temporary blob files during transactions. Auto-created in system temp directory if omitted.

## S3 Tiered Blob Storage

These settings enable tiered blob storage: blobs exceeding the threshold are
stored in S3-compatible object storage instead of PostgreSQL bytea. Requires
the `zodb-pgjsonb[s3]` extra to be installed.

| Setting | Default | Allowed Values |
|---|---|---|
| `db_pgjsonb_s3_bucket_name` | *(unset)* | string |
| `db_pgjsonb_s3_prefix` | *(unset)* | string |
| `db_pgjsonb_s3_endpoint_url` | *(unset, uses AWS)* | URL |
| `db_pgjsonb_s3_region` | *(unset)* | AWS region |
| `db_pgjsonb_s3_access_key` | *(unset)* | string |
| `db_pgjsonb_s3_secret_key` | *(unset)* | string |
| `db_pgjsonb_s3_use_ssl` | `true` | `true`, `false` |
| `db_pgjsonb_blob_threshold` | *(unset, default `1MB`)* | byte-size (KB, MB, GB) |
| `db_pgjsonb_blob_cache_dir` | *(unset)* | path |
| `db_pgjsonb_blob_cache_size` | *(unset, default `1GB`)* | byte-size (KB, MB, GB) |

**`db_pgjsonb_s3_bucket_name`** -- S3 bucket name for large blob storage. If omitted, all blobs are stored in PostgreSQL bytea.

**`db_pgjsonb_s3_endpoint_url`** -- S3 endpoint URL for MinIO, Ceph, or other S3-compatible stores (e.g. `http://localhost:9000`). Uses AWS S3 if omitted.

**`db_pgjsonb_s3_access_key`** / **`db_pgjsonb_s3_secret_key`** -- AWS credentials. Uses boto3 credential chain (IAM role, `~/.aws/credentials`, environment variables) if omitted.

**`db_pgjsonb_blob_threshold`** -- Blobs larger than this are stored in S3 (if configured). Blobs smaller than this stay in PostgreSQL bytea. Set to `0` to send all blobs to S3. Only effective when `db_pgjsonb_s3_bucket_name` is set.

**`db_pgjsonb_blob_cache_dir`** -- Local cache directory for S3 blobs. Recommended for production to avoid repeated S3 downloads. Falls back to `db_pgjsonb_blob_temp_dir` if omitted.

**`db_pgjsonb_blob_cache_size`** -- Maximum size of local blob cache.
