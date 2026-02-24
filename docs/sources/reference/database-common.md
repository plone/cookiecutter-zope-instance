# Database: Common Settings

<!-- diataxis: reference -->

Core database settings shared across all storage backends.
See {doc}`/explanation/storage-backends` for a comparison.

| Setting | Default | Allowed Values |
|---|---|---|
| `db_storage` | `direct` | `direct`, `relstorage`, `zeo`, `pgjsonb` |
| `db_cache_size` | `30000` | integer |
| `db_cache_size_bytes` | *(unset)* | byte-size (KB, MB, GB) |
| `db_large_record_size` | *(unset, default `16MB`)* | byte-size (KB, MB, GB) |
| `db_pool_size` | *(unset, default `7`)* | integer |
| `max_conflict_retries` | `3` | integer |

**`db_cache_size`** -- ZODB cache target maximum number of non-ghost objects per connection. One cache is created for each active parallel running thread. A powerful tuning knob -- if in doubt, do not touch.

**`db_cache_size_bytes`** -- Additional memory limit on top of `db_cache_size`. The cache is kept below whichever limit is hit first. Set to `0` to disable the byte-size check.

**`db_large_record_size`** -- When object records exceed this size a warning is issued suggesting blobs should be used instead.

**`db_pool_size`** -- Expected maximum number of simultaneously open connections. No hard limit; exceeding it logs a warning, exceeding 2x logs a critical message.
