# Database: Common Settings

<!-- diataxis: reference -->

Core database settings shared across all storage backends.

Zope/Plone offers different ZODB storage backends for different environments and needs.
See {doc}`/explanation/storage-backends` for a comparison.

`db_storage`
: Which storage type to be configured.

  Allowed values: `direct`, `relstorage`, `zeo`, `pgjsonb`

  **Default:** `direct`

`db_cache_size`
: Set the ZODB cache target maximum number of non-ghost objects, i.e. the
  number of objects which the ZODB cache will try to hold in RAM per connection.
  The actual size depends on the data. For each connection in the connection pool
  of the application process one cache is created. In other words one cache is
  created for each active parallel running thread. If in doubt do not touch.
  On the other hand it is a powerful setting to tune your application.

  **Default:** `30000`

`db_cache_size_bytes`
: Set the ZODB cache target total memory usage of non-ghost objects in each
  connection object cache. This setting sets an additional limit on top of
  `db_cache_size`. The cache is kept below the value of either `db_cache_size`
  or `db_cache_size_bytes`, whatever limit was hit first. If value is `0` the
  byte size check is switched off and only `db_cache_size` is taken into account.

  Allowed values: byte-size (integer format with postfix KB, MB, GB)

  **Default:** unset, empty string, database default of `0` is active

`db_large_record_size`
: When object records are saved that are larger than this, a warning is issued,
  suggesting that blobs should be used instead.

  Allowed values: byte-size (integer format with postfix KB, MB, GB)

  **Default:** unset, empty string, database default of `16MB` is active

`db_pool_size`
: The expected maximum number of simultaneously open connections. There is no
  hard limit (as many connections as are requested will be opened, until system
  resources are exhausted). Exceeding `pool-size` connections causes a warning
  message to be logged, and exceeding twice `pool-size` connections causes a
  critical message to be logged.

  Allowed values: integer

  **Default:** unset, empty string, database default of `7` is active

`max_conflict_retries`
: The maximum number of retries on a conflict error.

  **Default:** `3`
