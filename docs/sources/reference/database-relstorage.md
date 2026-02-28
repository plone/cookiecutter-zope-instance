# Database: RelStorage

<!-- diataxis: reference -->

[RelStorage](https://pypi.org/project/RelStorage/) is a storage implementation
for ZODB that stores pickles in a relational database (RDBMS).

:::{note}
Please see {doc}`database-common` and {doc}`database-blobs` as well --
you will need to set `db_blob_mode` to `cache` for RelStorage.
:::

## General Settings

| Setting | Default | Allowed Values |
|---|---|---|
| `db_relstorage` | `postgresql` | `postgresql`, `mysql`, `oracle`, `sqlite3` |
| `db_relstorage_keep_history` | `true` | `true`, `false` |
| `db_relstorage_read_only` | `false` | `true`, `false` |
| `db_relstorage_create_schema` | `true` | `true`, `false` |
| `db_relstorage_name` | *(unset)* | string |
| `db_relstorage_commit_lock_timeout` | *(unset, default `30`s)* | integer (seconds) |
| `db_relstorage_pack_gc` | *(unset, default `true`)* | `true`, `false` |

**`db_relstorage_name`** -- The storage name, used for logging and storage identification. Useful when running multiple RelStorage instances in the same process.

**`db_relstorage_keep_history`** -- If switched on, the adapter will create and use a history-preserving database schema (like FileStorage or ZEO). A history-preserving schema supports ZODB-level undo, but also grows more quickly and requires extensive packing on a regular basis. If switched off, the adapter will create and use a history-free database schema. Undo will not be supported, but the database will not grow as quickly.

**`db_relstorage_create_schema`** -- Normally, RelStorage will create or update the database schema on start-up. Switch it off if you need to connect to a RelStorage database without automatic creation or updates.

**`db_relstorage_commit_lock_timeout`** -- During commit, RelStorage acquires a database-wide lock. This option specifies how long to wait for the lock before failing the attempt to commit. Consult and understand the RelStorage documentation before using this setting.

**`db_relstorage_pack_gc`** -- If switched off, garbage collection is not performed during packing. This can make packing significantly faster and avoids issues when objects are referenced only from other databases.

## Blob Caching

RelStorage provides advanced blob caching options. For details read
[RelStorage: Blobs](https://relstorage.readthedocs.io/en/latest/relstorage-options.html#blobs).

| Setting | Default | Allowed Values |
|---|---|---|
| `db_relstorage_blob_cache_size_check_external` | `false` | `true`, `false` |
| `db_relstorage_blob_chunk_size` | *(unset, default `1048576`)* | byte-size |

## RAM and Persistent Caching

For details about caching read
[RelStorage: Database Caching](https://relstorage.readthedocs.io/en/latest/relstorage-options.html#database-caching).

| Setting | Default |
|---|---|
| `db_relstorage_cache_local_mb` | *(unset, default `10`)* |
| `db_relstorage_cache_local_object_max` | *(unset, default `16384` bytes)* |
| `db_relstorage_cache_local_compression` | *(unset, default `none`)* |
| `db_relstorage_cache_local_dir` | *(unset)* |
| `db_relstorage_cache_prefix` | *(unset, default is DB name)* |

**`db_relstorage_cache_local_mb`** -- Configures the approximate maximum amount of memory the cache should consume, in megabytes. Set to `0` to *disable* the in-memory cache (this is not recommended).

**`db_relstorage_cache_local_object_max`** -- Configures the maximum size of an object's pickle (in bytes) that can qualify for the *local* cache. The size is measured after compression. Larger objects can still qualify for the remote cache.

**`db_relstorage_cache_local_compression`** -- Configures compression within the *local* cache. This option names a Python module that provides two functions, `compress()` and `decompress()`. Supported values include `zlib`, `bz2`, and `none` (no compression). If you use the compressing storage wrapper `zc.zlibstorage`, this option automatically does nothing. With other compressing storage wrappers this should be set to `none`.

**`db_relstorage_cache_local_dir`** -- The path to a directory where the local cache will be saved when the database is closed. On startup, RelStorage will look in this directory for cache files to load into memory. The cache files must be located on a local (not network) filesystem. Consult and understand the *Database Caching* manual before using this setting.

**`db_relstorage_cache_prefix`** -- The prefix used as part of persistent cache file names. All clients using a database should use the same cache-prefix.

## Replication

If your database runs replicated, RelStorage supports handling of
replications. For details read
[RelStorage: Replication](https://relstorage.readthedocs.io/en/latest/relstorage-options.html#replication).

| Setting | Default |
|---|---|
| `db_relstorage_replica_conf` | *(unset)* |
| `db_relstorage_ro_replica_conf` | *(unset)* |
| `db_relstorage_replica_timeout` | *(unset)* |
| `db_relstorage_replica_revert_when_stale` | *(unset)* |

## Command Line Utilities

RelStorage provides helper scripts for packing (`zodbpack`) and
import/export from filestorage (`zodbconvert`).

:::{deprecated} 2.5
The RelStorage-specific `zodbconvert` import/export configuration files
(`relstorage-import.conf`, `relstorage-export.conf`) and their corresponding
`db_relstorage_import_*` / `db_relstorage_export_*` settings are deprecated
in favor of the generic
[zodb-convert](https://pypi.org/project/zodb-convert/) tool, which works
with any ZODB storage backend. Use the new `db_convert_*` settings and the
generated `convert-import.conf` / `convert-export.conf` files instead.
See {doc}`/how-to/migrate-storage` for details.

The existing settings and generated files continue to work but may be
removed in a future major version.
:::

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

| Setting | Default |
|---|---|
| `db_relstorage_import_filestorage_location` | *(unset)* |
| `db_relstorage_import_blobs_location` | *(unset)* |
| `db_relstorage_export_filestorage_location` | *(unset)* |
| `db_relstorage_export_blobs_location` | *(unset)* |

## PostgreSQL

For details read [RelStorage: PostgreSQL adapter options](https://relstorage.readthedocs.io/en/latest/postgresql/options.html).

| Setting | Default | Allowed Values |
|---|---|---|
| `db_relstorage_postgresql_driver` | `psycopg2` | `psycopg2`, `psycopg2 gevent`, `psycopg2cffi`, `pg8000` |
| `db_relstorage_postgresql_dsn` | *(unset)* | libpq DSN string |

**`db_relstorage_postgresql_dsn`** -- Specifies the data source name for connecting to PostgreSQL. A PostgreSQL DSN is a list of parameters separated with whitespace. A typical DSN looks like: `dbname='plone' user='username' host='localhost' password='secret'`

## MySQL

For details read [RelStorage: MySQL adapter options](https://relstorage.readthedocs.io/en/latest/mysql/options.html).

| Setting | Default | Allowed Values |
|---|---|---|
| `db_relstorage_mysql_driver` | `MySQLdb` | `MySQLdb`, `gevent MySQLdb`, `PyMySQL`, `C MySQL Connector/Python` |
| `db_relstorage_mysql_parameters` | *(empty dict)* | dictionary |

**`db_relstorage_mysql_parameters`** -- A dictionary with all MySQL parameters. This depends on the driver. Example:

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

## Oracle

For details read [RelStorage: Oracle adapter options](https://relstorage.readthedocs.io/en/latest/oracle/options.html).

| Setting | Default |
|---|---|
| `db_relstorage_oracle_driver` | `cx_Oracle` |
| `db_relstorage_oracle_user` | *(unset)* |
| `db_relstorage_oracle_password` | *(unset)* |
| `db_relstorage_oracle_dsn` | *(unset)* |
| `db_relstorage_commit_lock_id` | *(unset)* |

**`db_relstorage_oracle_driver`** -- The Oracle database driver. Currently only `cx_Oracle` is supported by RelStorage.

**`db_relstorage_oracle_dsn`** -- The Oracle data source name. The Oracle client library will normally expect to find the DSN in `/etc/oratab`.

**`db_relstorage_commit_lock_id`** -- During commit, RelStorage acquires a database-wide lock. This option specifies the lock ID. This option currently applies only to the Oracle adapter.

## SQLite

For details read [RelStorage: SQLite adapter options](https://relstorage.readthedocs.io/en/latest/sqlite3/options.html).

| Setting | Default | Allowed Values |
|---|---|---|
| `db_relstorage_sqlite3_driver` | `sqlite3` | `sqlite3`, `gevent sqlite3` |
| `db_relstorage_sqlite3_data_dir` | `{{ cookiecutter.location_clienthome }}/sqlite3/` | path |
| `db_relstorage_sqlite3_gevent_yield_interval` | *(unset, default `100`)* | integer |
| `db_relstorage_sqlite3_pragma` | *(empty dict)* | dictionary |

**`db_relstorage_sqlite3_data_dir`** -- The path to a directory to hold the data. Choosing a dedicated directory is strongly recommended. A network filesystem is generally not recommended.

**`db_relstorage_sqlite3_gevent_yield_interval`** -- Only used if the driver is `gevent sqlite3`.

**`db_relstorage_sqlite3_pragma`** -- For advanced tuning, nearly the entire set of SQLite PRAGMAs are available.
