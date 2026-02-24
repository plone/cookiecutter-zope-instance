# Database: RelStorage

<!-- diataxis: reference -->

[RelStorage](https://pypi.org/project/RelStorage/) is a storage implementation
for ZODB that stores pickles in a relational database (RDBMS).

:::{note}
Please see {doc}`database-common` and {doc}`database-blobs` as well --
you will need to set `db_blob_mode` to `cache` for RelStorage.
:::

## General Settings

`db_relstorage`
: Set the database server to be used.

  Allowed values: `postgresql`, `mysql`, `oracle`, `sqlite3`

  **Default:** `postgresql`

`db_relstorage_keep_history`
: If this option is switched on, the adapter will create and use a
  history-preserving database schema (like FileStorage or ZEO). A
  history-preserving schema supports ZODB-level undo, but also grows more
  quickly and requires extensive packing on a regular basis.

  If this option is switched off, the adapter will create and use a
  history-free database schema. Undo will not be supported, but the database
  will not grow as quickly.

  Allowed values: `true`, `false`

  **Default:** `true`

`db_relstorage_read_only`
: If switched on, only reads may be executed against the storage.

  Allowed values: `true`, `false`

  **Default:** `false`

`db_relstorage_create_schema`
: Normally, RelStorage will create or update the database schema on start-up.
  Switch it off if you need to connect to a RelStorage database without
  automatic creation or updates.

  Allowed values: `true`, `false`

  **Default:** `true`

`db_relstorage_commit_lock_timeout`
: During commit, RelStorage acquires a database-wide lock. This option
  specifies how long to wait for the lock before failing the attempt to commit.
  Consult and understand the RelStorage documentation before using this setting.

  **Default:** unset, empty string, RelStorage default of `30` seconds is active

## Blob Caching

RelStorage provides advanced blob caching options. For details read
[RelStorage: Blobs](https://relstorage.readthedocs.io/en/latest/relstorage-options.html#blobs).

`db_relstorage_blob_cache_size_check_external`
: For details read original RelStorage documentation.

  Allowed values: `true`, `false`

  **Default:** `false`

`db_relstorage_blob_chunk_size`
: For details read original RelStorage documentation.

  **Default:** unset, empty string, RelStorage default of `1048576` (1 MB) is
  active. This option allows suffixes such as "mb" or "gb".

## RAM and Persistent Caching

For details about caching read
[RelStorage: Database Caching](https://relstorage.readthedocs.io/en/latest/relstorage-options.html#database-caching).

`db_relstorage_cache_local_mb`
: Configures the approximate maximum amount of memory the cache should
  consume, in megabytes. Set to `0` to *disable* the in-memory cache (this
  is not recommended).

  **Default:** unset, empty string, RelStorage default of `10` is active

`db_relstorage_cache_local_object_max`
: Configures the maximum size of an object's pickle (in bytes) that can
  qualify for the *local* cache. The size is measured after compression.
  Larger objects can still qualify for the remote cache.

  **Default:** unset, empty string, RelStorage default of `16384` bytes is
  active

`db_relstorage_cache_local_compression`
: Configures compression within the *local* cache. This option names a Python
  module that provides two functions, `compress()` and `decompress()`.
  Supported values include `zlib`, `bz2`, and `none` (no compression). If you
  use the compressing storage wrapper `zc.zlibstorage`, this option
  automatically does nothing. With other compressing storage wrappers this
  should be set to `none`.

  **Default:** unset, empty string, RelStorage default of `none` is active

`db_relstorage_cache_local_dir`
: The path to a directory where the local cache will be saved when the
  database is closed. On startup, RelStorage will look in this directory for
  cache files to load into memory. The cache files must be located on a local
  (not network) filesystem. Consult and understand the *Database Caching*
  manual before using this setting.

  **Default:** unset, empty string

`db_relstorage_cache_prefix`
: The prefix used as part of persistent cache file names. All clients using a
  database should use the same cache-prefix.

  **Default:** unset, empty string, RelStorage default of the database name is
  active

## Replication

If your database runs replicated, RelStorage supports handling of
replications. For details read
[RelStorage: Replication](https://relstorage.readthedocs.io/en/latest/relstorage-options.html#replication).

`db_relstorage_replica_conf`
: For details read original RelStorage documentation.

  **Default:** unset, empty string

`db_relstorage_ro_replica_conf`
: For details read original RelStorage documentation.

  **Default:** unset, empty string

`db_relstorage_replica_timeout`
: For details read original RelStorage documentation.

  **Default:** unset, empty string

`db_relstorage_replica_revert_when_stale`
: For details read original RelStorage documentation.

  **Default:** unset, empty string

## Command Line Utilities

RelStorage provides helper scripts for packing (`zodbpack`) and
import/export from filestorage (`zodbconvert`).

The file `relstorage-pack.conf` for the command line utility `zodbpack` is
always generated for all RelStorage configurations. For usage information
read [Packing Or Reference Checking A ZODB Storage: zodbpack](https://relstorage.readthedocs.io/en/latest/zodbpack.html).

The files:

- `relstorage-export.conf` is generated if the two `db_relstorage_export_*`
  settings are given.
- `relstorage-import.conf` is generated if the two `db_relstorage_import_*`
  settings are given.

Both are for the command line utility `zodbconvert`. For usage information
read [Copying Data Between ZODB Storages: zodbconvert](https://relstorage.readthedocs.io/en/latest/zodbconvert.html).

`db_relstorage_import_filestorage_location`
: The filename of the filestorage to import from.

  **Default:** unset, empty string

`db_relstorage_import_blobs_location`
: The directory of the blob storage to import from.

  **Default:** unset, empty string

`db_relstorage_export_filestorage_location`
: The filename of the filestorage to export to.

  **Default:** unset, empty string

`db_relstorage_export_blobs_location`
: The directory of the blob storage to export to.

  **Default:** unset, empty string

## PostgreSQL

For details read [RelStorage: PostgreSQL adapter options](https://relstorage.readthedocs.io/en/latest/postgresql/options.html).

`db_relstorage_postgresql_driver`
: Driver to use.

  Allowed values: `psycopg2`, `psycopg2 gevent`, `psycopg2cffi`, `pg8000`

  **Default:** `psycopg2`

`db_relstorage_postgresql_dsn`
: Specifies the data source name for connecting to PostgreSQL. A PostgreSQL
  DSN is a list of parameters separated with whitespace. A typical DSN looks
  like: `dbname='plone' user='username' host='localhost' password='secret'`

  **Default:** unset, empty string

## MySQL

For details read [RelStorage: MySQL adapter options](https://relstorage.readthedocs.io/en/latest/mysql/options.html).

`db_relstorage_mysql_driver`
: Driver to use.

  Allowed values: `MySQLdb`, `gevent MySQLdb`, `PyMySQL`,
  `C MySQL Connector/Python`

  **Default:** `MySQLdb`

`db_relstorage_mysql_parameters`
: A dictionary with all MySQL parameters. This depends on the driver.

  Example:

  ```json
  {
      "db_relstorage_mysql_parameters": {
          "host": "localhost",
          "user": "plone",
          "passwd": "secret",
          "db": "plone"
      }
  }
  ```

  **Default:** empty dictionary

## Oracle

For details read [RelStorage: Oracle adapter options](https://relstorage.readthedocs.io/en/latest/oracle/options.html).

`db_relstorage_oracle_user`
: The Oracle account name.

  **Default:** unset, empty string

`db_relstorage_oracle_password`
: The Oracle account password.

  **Default:** unset, empty string

`db_relstorage_oracle_dsn`
: The Oracle data source name. The Oracle client library will normally expect
  to find the DSN in `/etc/oratab`.

  **Default:** unset, empty string

`db_relstorage_commit_lock_id`
: During commit, RelStorage acquires a database-wide lock. This option
  specifies the lock ID. This option currently applies only to the Oracle
  adapter.

  **Default:** unset, empty string

## SQLite

For details read [RelStorage: SQLite adapter options](https://relstorage.readthedocs.io/en/latest/sqlite3/options.html).

`db_relstorage_sqlite3_driver`
: Allowed values: `sqlite3`, `gevent sqlite3`

  **Default:** `sqlite3`

`db_relstorage_sqlite3_data_dir`
: The path to a directory to hold the data. Choosing a dedicated directory is
  strongly recommended. A network filesystem is generally not recommended.

  **Default:** `{{ cookiecutter.location_clienthome }}/sqlite3/`

`db_relstorage_sqlite3_gevent_yield_interval`
: Only used if the driver is `gevent sqlite3`.

  **Default:** unset, empty string, RelStorage has an internal default of `100`

`db_relstorage_sqlite3_pragma`
: For advanced tuning, nearly the entire set of SQLite PRAGMAs are available.

  **Default:** unset, empty dictionary
