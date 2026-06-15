# Pack and garbage-collect the database

<!-- diataxis: how-to -->

This guide shows you how to pack the ZODB to reclaim disk space and remove
unreferenced objects (garbage collection).
The procedure depends on your storage backend.

## Prerequisites

- New to this template? Start with {doc}`/tutorials/first-zope-instance`.
- A generated instance with data to pack.

## RelStorage

For RelStorage, the cookiecutter always generates `etc/relstorage-pack.conf`
for the `zodbpack` command-line utility.
Run it from your instance directory:

```shell
zodbpack etc/relstorage-pack.conf
```

`zodbpack` packs the database and performs garbage collection.
For all options, read
[Packing or reference checking a ZODB storage](https://relstorage.readthedocs.io/en/latest/zodbpack.html).

Schedule regular packing with cron, for example weekly:

```text
0 3 * * 0  cd /srv/instance && zodbpack etc/relstorage-pack.conf
```

## Filestorage

For the `direct` backend, pack from the Zope Management Interface:
open {menuselection}`Control_Panel --> Database Management --> main`, set the
number of days of history to keep, and select {guilabel}`Pack`.

Two settings control packing behavior:

```yaml
default_context:
    db_storage: direct

    # Keep a .old copy of the database before packing
    db_filestorage_pack_keep_old: true

    # Skip garbage collection during packing for speed
    db_filestorage_pack_gc: true
```

See {doc}`/reference/database-direct` for details.

## PGJsonb

A history-free PGJsonb database (the default) does not accumulate undo
history, so routine packing is rarely needed.

A history-preserving database (`db_pgjsonb_history_preserving: true`) grows
over time and requires regular packing through the storage's own tooling.
See {doc}`/reference/database-pgjsonb`.

## ZEO

Packing a ZEO database is a server-side operation: pack the storage on the
ZEO server, not from the client.
ZEO server administration is outside the scope of this template; consult the
ZODB/ZEO documentation.

## Next steps

- {doc}`/reference/database-relstorage` -- RelStorage command-line utilities.
- {doc}`backup-and-restore` -- Back up before packing large databases.
- {doc}`/explanation/storage-backends` -- Comparison of all storage backends.
