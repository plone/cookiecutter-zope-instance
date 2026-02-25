# Database: Direct Filestorage

<!-- diataxis: reference -->

If you have only one application process, it can open a direct filestorage
database file directly without running a database server process. For details
read the [Zope configuration reference](https://zope.readthedocs.io/en/latest/operation.html#zope-configuration-reference).

| Setting | Default | Allowed Values |
|---|---|---|
| `db_filestorage_location` | `{{ cookiecutter.location_clienthome }}/filestorage/Data.fs` | path |
| `db_filestorage_pack_keep_old` | `true` | `true`, `false` |
| `db_filestorage_quota` | *(unset)* | byte-size (KB, MB, GB) |
| `db_filestorage_packer` | *(unset)* | dotted-name |
| `db_filestorage_pack_gc` | `true` | `true`, `false` |
| `db_filestorage_create` | *(unset, default `true`)* | `true`, `false` |
| `db_filestorage_read_only` | *(unset, default `false`)* | `true`, `false` |

**`db_filestorage_location`** -- The filename where the ZODB data file will be stored. Note: side by side with the given file other `Data.fs.*` files (like locks and indexes) are created.

**`db_filestorage_pack_keep_old`** -- If switched on, a copy of the database before packing is kept in a `.old` file.

**`db_filestorage_quota`** -- Maximum allowed size of the storage file. Operations which would cause the size of the storage to exceed the quota will result in a `ZODB.FileStorage.FileStorageQuotaError` being raised.

**`db_filestorage_packer`** -- The dotted name (dotted module name and object name) of a packer object. This is used to provide an alternative pack implementation.

**`db_filestorage_pack_gc`** -- If switched off, then no garbage collection will be performed when packing. This can make packing go much faster and can avoid problems when objects are referenced only from other databases.

**`db_filestorage_create`** -- Whether to create the database file if it does not exist. Default is `true`. Set to `false` to prevent accidental creation of empty databases -- Zope will fail to start if the file is missing.

**`db_filestorage_read_only`** -- Open the storage in read-only mode. No modifications can be made. Useful for analysis, debugging, or serving read-only replicas.
