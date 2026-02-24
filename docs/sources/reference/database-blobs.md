# Database: Blob Settings

<!-- diataxis: reference -->

Blob settings valid for `direct`, `relstorage`, and `zeo` storage backends.

:::{note}
These settings are **not used** with PGJsonb, which manages blobs through its
own settings. See {doc}`database-pgjsonb`.
:::

See {doc}`/explanation/blob-handling` for background on how blobs work across backends.

| Setting | Default | Allowed Values |
|---|---|---|
| `db_blob_mode` | `shared` | `shared`, `cache` |
| `db_blob_location` | `{{ cookiecutter.location_clienthome }}/blobs` | path |
| `db_blob_cache_size` | `6312427520` (~5 GB) | integer (bytes) |
| `db_blob_cache_size_check` | `10` | integer (percent) |

:::{attention}
Do not forget to set `db_blob_mode` to `cache` if you use RelStorage!
:::

**`db_blob_mode`** -- Set if blobs are stored *shared* within all clients or are they stored on the storage backend and the client only operates as temporary *cache*. For *direct* storage only *shared* applies (operates like shared with one single client).

**`db_blob_location`** -- The name of the directory where the ZODB blob data or cache (depends on `db_blob_mode`) will be stored.

**`db_blob_cache_size`** -- Set the maximum size of the blob cache, in bytes. With many blobs and enough disk space on the client hardware this should be increased. If not set, then the cache size isn't checked and the blob directory will grow without bound. Only valid for `db_blob_mode` `cache`.

**`db_blob_cache_size_check`** -- Set the ZEO check size as percent of `db_blob_cache_size` (for example, `10` for 10%). The ZEO cache size will be checked when this many bytes have been loaded into the cache. Only valid for `db_blob_mode` `cache`.
