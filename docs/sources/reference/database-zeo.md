# Database: ZEO

<!-- diataxis: reference -->

ZEO is a mature client-server storage created for ZODB for sharing a single
storage among many clients. All options can be found in the
[Zope Configuration Reference](https://zope.readthedocs.io/en/latest/operation.html#zope-configuration-reference)
under `<zeoclient>`.

## Main Settings

`db_zeo_server`
: Set the server address of the ZEO server. You can set more than one address
  (white space delimited). Alternative addresses will be used if the primary
  address is down.

  **Default:** `localhost:8100`

`db_zeo_name`
: Set the storage name of the ZEO storage.

  **Default:** `1`

## Caching

`db_cache_size` and `db_cache_size_bytes` from {doc}`database-common` are
taken into account. Additional persistent caching is possible.

`db_zeo_client`
: Enables persistent cache files. Set the persistent cache name that is used
  to construct the cache filenames. This enables the ZEO cache to persist
  across application restarts.

  Persistent cache files are disabled by default. If disabled, the client
  creates a temporary cache that will only be used by the current object.

  The string passed here is used to construct the cache filenames.

  Allowed values: string

  **Default:** unset, empty string

`db_zeo_var`
: The directory where persistent cache files are stored. By default cache
  files, if they are persistent, are stored in the current directory.

  **Default:** unset, empty string, the system temporary folder is used

`db_zeo_cache_size`
: Set the size of the file based ZEO client cache. The ZEO cache is a disk
  based cache shared between application threads. It is stored either in
  temporary files or, in case you activate persistent cache files with the
  `db_zeo_client` option, in the folder designated by `db_zeo_var`.

  **Default:** `128MB`

## Authentication

ZEO supports authentication. You need to activate ZEO authentication on the
server side as well for this to work. Without this anyone that can connect to
the database server's socket can read and write arbitrary data.

`db_zeo_username`
: Enable ZEO authentication and use the given username when accessing the ZEO
  server. It is obligatory to also specify a `db_zeo_password`.

  **Default:** unset, empty string, no authentication

`db_zeo_password`
: Password to use when connecting to a ZEO server with authentication enabled.

  **Default:** unset, empty string

`db_zeo_realm`
: Authentication realm to use when authenticating with a ZEO server.

  **Default:** `ZEO`

## Advanced Options

`db_zeo_read_only_fallback`
: A flag indicating whether a read-only remote storage should be acceptable as
  a fallback when no writable storages are available.

  Allowed values: `true`, `false`

  **Default:** `false`

`db_zeo_read_only`
: Set ZEO client as read only.

  Allowed values: `true`, `false`

  **Default:** `false`

`db_zeo_drop_cache_rather_verify`
: Indicates that the cache should be dropped rather than verified when the
  verification optimization is not available (e.g. when the ZEO server
  restarted).

  Allowed values: `true`, `false`

  **Default:** `false`
