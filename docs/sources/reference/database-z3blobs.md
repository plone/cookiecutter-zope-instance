# Database: S3 Blob Wrapper (z3blobs)

<!-- diataxis: reference -->

[zodb-s3blobs](https://pypi.org/project/zodb-s3blobs/) is a storage **wrapper**
that intercepts blob operations and redirects them to S3-compatible object
storage. It wraps any ZODB storage backend (`direct`, `relstorage`, or `zeo`)
and replaces its blob handling with S3-backed blob storage plus a local LRU
cache.

:::{note}
z3blobs is a wrapper, not a standalone storage backend. You still choose a
backend via `db_storage`. The wrapper is enabled by setting
`db_z3blobs_enabled: true`.
:::

:::{important}
z3blobs **cannot** be used with `pgjsonb` storage. PGJsonb handles blobs
natively via PostgreSQL bytea and optional S3 tiering through its own
`db_pgjsonb_s3_*` settings.
:::

## Core Settings

| Setting | Default | Allowed Values |
|---|---|---|
| `db_z3blobs_enabled` | `false` | `true`, `false` |
| `db_z3blobs_bucket_name` | *(unset, **required** when enabled)* | string |
| `db_z3blobs_cache_dir` | *(unset, **required** when enabled)* | path |
| `db_z3blobs_cache_size` | *(unset)* | byte-size (KB, MB, GB) |

**`db_z3blobs_enabled`** -- Enable the S3 blob wrapper. When `true`, the selected `db_storage` backend is nested inside `<s3blobstorage>` and the inner storage's blob directives (`blob-dir`, `shared-blob-dir`, etc.) are suppressed.

**`db_z3blobs_bucket_name`** -- S3 bucket name for blob storage. **Required** when z3blobs is enabled.

**`db_z3blobs_cache_dir`** -- Local filesystem directory for the LRU blob cache. Blobs are cached here after download from S3 to avoid repeated network requests. **Required** when z3blobs is enabled.

**`db_z3blobs_cache_size`** -- Maximum size of the local blob cache. When exceeded, least recently used blobs are evicted.

## S3 Connection Settings

| Setting | Default | Allowed Values |
|---|---|---|
| `db_z3blobs_s3_prefix` | *(unset)* | string |
| `db_z3blobs_s3_endpoint_url` | *(unset, uses AWS)* | URL |
| `db_z3blobs_s3_region` | *(unset)* | AWS region |
| `db_z3blobs_s3_access_key` | *(unset)* | string |
| `db_z3blobs_s3_secret_key` | *(unset)* | string |
| `db_z3blobs_s3_use_ssl` | `true` | `true`, `false` |
| `db_z3blobs_s3_addressing_style` | *(unset)* | `path`, `virtual` |
| `db_z3blobs_s3_sse_customer_key` | *(unset)* | base64-encoded key |

**`db_z3blobs_s3_prefix`** -- Key prefix within the bucket. Useful for sharing a bucket across multiple deployments.

**`db_z3blobs_s3_endpoint_url`** -- S3 endpoint URL for MinIO, Ceph, or other S3-compatible stores (e.g. `http://localhost:9000`). Uses AWS S3 if omitted.

**`db_z3blobs_s3_access_key`** / **`db_z3blobs_s3_secret_key`** -- AWS credentials. Uses boto3 credential chain (IAM role, `~/.aws/credentials`, environment variables) if omitted.

**`db_z3blobs_s3_addressing_style`** -- S3 URL addressing style. Use `path` for MinIO and other S3-compatible stores that don't support virtual-hosted-style addressing.

**`db_z3blobs_s3_sse_customer_key`** -- Customer-provided encryption key for S3 Server-Side Encryption (SSE-C). Must be a base64-encoded 256-bit key. **Requires `s3_use_ssl: true`** (enforced by pre-generation validation).
