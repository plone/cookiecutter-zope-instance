# Back up and restore

<!-- diataxis: how-to -->

This guide shows you how to back up an instance's data and restore it.
The right method depends on your storage backend.

## Prerequisites

- New to this template? Start with {doc}`/tutorials/first-zope-instance`.

## Choose an approach

| Backend | Recommended backup |
|---|---|
| direct (filestorage) | Cold copy of `Data.fs` and the blob directory |
| relstorage | `pg_dump` (or the database engine's native tool) |
| pgjsonb | `pg_dump`, plus the S3 bucket when blobs are tiered |
| zeo | Back up the storage on the ZEO server |
| any | Portable export to a FileStorage with `zodb-convert` |

## Filestorage: cold copy

Stop the instance, then copy the data file and blob directory together so
they stay consistent:

```shell
cp var/filestorage/Data.fs /backup/Data.fs
cp -a var/blobs /backup/blobs
```

Restore by copying both back into place while the instance is stopped.

```{important}
Copy `Data.fs` and the blob directory from the same point in time.
A blob directory that is out of sync with `Data.fs` causes
`POSKeyError` on blob access.
```

## PostgreSQL-backed: pg_dump

For RelStorage and PGJsonb, back up the underlying PostgreSQL database with
its native tools:

```shell
pg_dump --format=custom --file=/backup/zodb.dump plone
```

Restore into an empty database:

```shell
pg_restore --dbname=plone /backup/zodb.dump
```

When PGJsonb tiers blobs to S3 (`db_pgjsonb_s3_bucket_name`), back up that
bucket as well; the database alone does not contain the tiered blobs.

## Portable backup with zodb-convert

To create a storage-agnostic snapshot, export the database to a FileStorage
with `zodb-convert`.
This works for every backend and produces a portable `Data.fs` you can
restore into any other backend.
See {doc}`migrate-storage` for the step-by-step procedure using the generated
`convert-export.conf` and `convert-import.conf` files.

## Next steps

- {doc}`migrate-storage` -- Move data between backends with `zodb-convert`.
- {doc}`pack-and-gc` -- Reclaim space after restoring a large database.
- {doc}`/explanation/blob-handling` -- How blobs are stored across backends.
