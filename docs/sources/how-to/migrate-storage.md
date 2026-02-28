# Migrate Data Between Storage Backends

<!-- diataxis: how-to -->

This guide shows how to copy ZODB data from one storage backend to another
using the generic [zodb-convert](https://pypi.org/project/zodb-convert/) tool.

## Prerequisites

- The `zodb-convert` package installed in your virtual environment
- The storage-specific packages for both source and destination installed
  (e.g. `ZODB` for filestorage, `RelStorage` for relstorage, `zodb-pgjsonb`
  for pgjsonb)

## Approach 1: Generated configuration files

When your instance uses a non-filestorage backend (RelStorage, PGJsonb, or
ZEO), the cookiecutter generates `convert-import.conf` and
`convert-export.conf` files in the `etc/` directory. These are ready-made
configuration files for `zodb-convert` that convert between your configured
backend and a FileStorage.

### Step 1: Set the conversion paths

In your `instance.yaml`, provide the FileStorage paths for the "other side"
of the conversion:

```yaml
default_context:
    db_storage: pgjsonb
    db_pgjsonb_dsn: "dbname='zodb' user='zodb' host='localhost' port='5433'"

    # Conversion settings (FileStorage side)
    db_convert_import_filestorage_location: var/import/Data.fs
    db_convert_import_blobs_location: var/import/blobs
    db_convert_export_filestorage_location: var/export/Data.fs
    db_convert_export_blobs_location: var/export/blobs
```

These settings work with all non-filestorage backends.

### Step 2: Import data from FileStorage

Place your `Data.fs` and blobs at the import locations, then run:

```bash
zodb-convert etc/convert-import.conf
```

### Step 3: Export data to FileStorage

To create a portable FileStorage backup:

```bash
zodb-convert etc/convert-export.conf
```

## Approach 2: Using existing zope.conf files

If you have two Zope instances with different storage backends, `zodb-convert`
can read storage configuration directly from their `zope.conf` files. No
extra configuration files are needed.

### Step 1: Generate the destination instance

Create a second instance configured for the new storage backend:

```yaml
# instance-new.yaml
default_context:
    db_storage: pgjsonb
    db_pgjsonb_dsn: "dbname='zodb' user='zodb' host='localhost' port='5433'"
```

Run cookiecutter to generate:

```bash
cookiecutter -f --no-input --config-file instance-new.yaml \
    gh:plone/cookiecutter-zope-instance
```

### Step 2: Run the conversion

```bash
zodb-convert \
    --source-zope-conf /old-instance/etc/zope.conf \
    --dest-zope-conf /new-instance/etc/zope.conf
```

### Specifying a named database

If your `zope.conf` defines multiple `<zodb_db>` sections:

```bash
zodb-convert \
    --source-zope-conf old/etc/zope.conf --source-db main \
    --dest-zope-conf new/etc/zope.conf --dest-db main
```

The default database name is `main`.

## Useful options

- `--dry-run` -- preview what would be copied without writing data
- `--incremental` -- resume from the last transaction in the destination
  (useful for large databases or after interruptions)
- `-v` -- show INFO-level progress; `-vv` for DEBUG-level detail

## Common migration scenarios

| From | To | Notes |
|---|---|---|
| direct (filestorage) | relstorage | Classic scale-out migration |
| direct (filestorage) | pgjsonb | Move to SQL-queryable storage |
| relstorage | pgjsonb | Switch to JSONB representation |
| zeo | relstorage | Remove ZEO server dependency |
| any | direct (filestorage) | Create a portable backup |

All combinations work -- `zodb-convert` is storage-agnostic.

## Configuration reference

| Setting | Default | Description |
|---|---|---|
| `db_convert_import_filestorage_location` | *(unset)* | Path to the source FileStorage for import |
| `db_convert_import_blobs_location` | *(unset)* | Path to the source blob directory for import |
| `db_convert_export_filestorage_location` | *(unset)* | Path for the destination FileStorage on export |
| `db_convert_export_blobs_location` | *(unset)* | Path for the destination blob directory on export |

The `convert-import.conf` file is generated when both `db_convert_import_*`
settings are provided. The `convert-export.conf` file is generated when both
`db_convert_export_*` settings are provided. Neither file is generated for
the `direct` (filestorage) backend since it *is* the portable format.

## Next steps

- [zodb-convert on PyPI](https://pypi.org/project/zodb-convert/) -- Full
  documentation and source code
- {doc}`/explanation/storage-backends` -- Understanding the trade-offs
  between backends
