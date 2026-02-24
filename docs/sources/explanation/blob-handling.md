# How Blob Storage Works

<!-- diataxis: explanation -->

Blobs (Binary Large Objects) in ZODB represent large binary data such as
files, images, and documents. Because blobs can be very large, they are
handled differently from regular ZODB objects. Each storage backend has its
own approach to blob management.

## What are ZODB blobs?

ZODB blobs are persistent objects that store binary data in the filesystem
rather than in the main object database. When your Plone site stores an
uploaded file or image, the binary content is managed as a blob. The ZODB
object graph holds a reference to the blob, but the actual bytes live
outside the main pickle storage.

## Direct filestorage

With direct filestorage, blobs are stored in a dedicated directory on the
local filesystem. There is only one application process, so there is no
sharing concern.

- **Mode:** Always behaves as `shared` (single process)
- **Location:** Configured via `db_blob_location`
  (default: `instance/var/blobs`)
- **No cache layer** -- the application reads and writes blob files directly

## RelStorage: shared vs. cache

### Cache mode (`db_blob_mode: cache`)

Blobs are stored **inside the relational database** as binary data. Each
Zope application process maintains a local cache directory where blob files
are downloaded on demand.

- Recommended for most RelStorage deployments
- No shared filesystem required
- The local cache grows up to `db_blob_cache_size` and is automatically pruned
- Each application process has its own independent cache

### Shared mode (`db_blob_mode: shared`)

Blobs are stored in a **shared filesystem directory** accessible to all
application processes (typically via NFS).

- Requires a network filesystem mount shared by all Zope processes
- No blob data in the relational database
- All processes read/write the same blob directory

```{important}
When using RelStorage, you **must** explicitly set `db_blob_mode: cache`
(or `shared`). The default value `shared` assumes direct filestorage
semantics and will not work correctly with RelStorage unless you have
actually set up a shared filesystem.
```

## ZEO: shared vs. cache

ZEO supports the same two blob modes, but the recommended default is
different:

### Shared mode (`db_blob_mode: shared`) -- recommended for ZEO

All ZEO clients and the ZEO server share a common blob directory. This is
the traditional and most common ZEO blob setup.

### Cache mode (`db_blob_mode: cache`)

Blobs are stored on the ZEO server and cached locally by each client. Useful
when a shared filesystem is not available.

## PGJsonb: a different model

PGJsonb handles blobs differently from the other backends. The generic
`db_blob_mode` and `db_blob_location` settings are **not used**.

### Default: PostgreSQL bytea

By default, blob data is stored directly in PostgreSQL `bytea` columns
alongside the JSONB object state. This keeps everything in a single database
with no filesystem dependencies.

### Optional: S3 tiered storage

For deployments with large or numerous blobs, PGJsonb supports tiering
blobs to S3-compatible object storage:

- Blobs smaller than `db_pgjsonb_blob_threshold` (default: 1 MB) stay in
  PostgreSQL `bytea`
- Blobs exceeding the threshold are uploaded to S3
- A local cache directory avoids repeated S3 downloads

## S3 Blob Wrapper (z3blobs)

The `zodb-s3blobs` wrapper can be applied to `direct`, `relstorage`, or `zeo`
to redirect all blob operations to S3-compatible object storage. When enabled:

- The inner storage's blob settings (`blob-dir`, `shared-blob-dir`, etc.) are
  suppressed automatically
- All blob reads and writes go through the z3blobs wrapper
- A local LRU cache (`db_z3blobs_cache_dir`) avoids repeated S3 downloads
- No shared filesystem is needed for blobs

This is useful in containerized environments or when local/shared filesystem
blob storage is impractical.

:::{note}
z3blobs is **not compatible with PGJsonb**. PGJsonb has its own S3 blob tiering
via `db_pgjsonb_s3_*` settings.
:::

## Summary

| Backend | Default Blob Location | Modes | Shared FS Needed? |
|---|---|---|---|
| **direct** | Local filesystem | shared (implicit) | No |
| **relstorage** | RDBMS or shared FS | cache, shared | Only in shared mode |
| **zeo** | ZEO server or shared FS | shared, cache | Only in shared mode |
| **pgjsonb** | PostgreSQL bytea (+ optional S3) | N/A | No |
| **z3blobs wrapper** | S3 (+ local LRU cache) | N/A | No |
