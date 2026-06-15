# Back up and restore

<!-- diataxis: how-to -->

This guide shows you how to back up an instance's data and restore it.
The right method depends on your storage backend.

## Prerequisites

- New to this template? Start with {doc}`/tutorials/first-zope-instance`.

## Choose an approach

A complete backup has two parts: the storage (the database or `Data.fs`) and
any blobs kept on the filesystem.
Whether you must back up a blob directory depends on `db_blob_mode`: in
`shared` mode the directory holds the authoritative blobs, while in `cache`
mode it is only a local cache and the authoritative blobs live in the
database or on the ZEO server.

| Backend | Storage backup | Filesystem blobs to back up |
|---|---|---|
| direct (filestorage) | Cold copy of `Data.fs` | The blob directory (always) |
| relstorage | `pg_dump` | The shared blob directory if `db_blob_mode: shared`; none in `cache` mode (blobs are in the database) |
| pgjsonb | `pg_dump` | None on the filesystem; the S3 bucket if blobs are tiered |
| zeo | Back up the storage on the ZEO server | The shared blob directory if `db_blob_mode: shared` |
| any | Portable `zodb-convert` export to a FileStorage (includes blobs) | — |

```{important}
Back up the storage and its blob directory from the same point in time.
A blob directory that is out of sync with the storage causes `POSKeyError`
on blob access.
Because blob files are write-once, copying the blob directory last makes it a
safe superset of what the storage references.
```

## Filestorage: cold copy

Stop the instance, then copy the data file and blob directory together so
they stay consistent:

```shell
cp var/filestorage/Data.fs /backup/Data.fs
cp -a var/blobs /backup/blobs
```

Restore by copying both back into place while the instance is stopped.

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

With RelStorage in the recommended `cache` mode, blobs are stored in the
database, so `pg_dump` captures them.
When PGJsonb tiers blobs to S3 (`db_pgjsonb_s3_bucket_name`), back up that
bucket as well; the database alone does not contain the tiered blobs.

## ZEO

A ZEO client holds no authoritative data of its own, so there is nothing to
back up on the client.
Back up on the ZEO server host instead: the server runs its own storage --
usually a FileStorage or RelStorage -- so use the matching method above
(cold copy of `Data.fs`, or `pg_dump`) against that storage.

If the deployment uses a shared blob directory, also back it up as described
below.
ZEO server administration is otherwise outside the scope of this template;
consult the ZODB/ZEO documentation.

## Shared blob directories

When blobs are stored on the filesystem in `shared` mode rather than in the
database, the blob directory (`db_blob_location`) is authoritative and needs
its own backup.
This applies to filestorage, to RelStorage or ZEO configured with
`db_blob_mode: shared`, and to any setup whose blob directory is a network
mount such as NFS.

Back up the directory alongside the storage:

```shell
cp -a /srv/zodb/blobs /backup/blobs
```

For ZEO, back up the shared blob directory on whichever host exports it, in
addition to backing up the storage on the ZEO server.
A `cache`-mode blob directory does not need backing up: it is rebuilt from the
authoritative storage.

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
