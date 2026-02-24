# Configure ZEO Client

<!-- diataxis: how-to -->

This guide walks you through setting up a ZEO (Zope Enterprise Objects)
client. ZEO is a mature client-server storage for ZODB that allows multiple
Zope application processes to share a single database.

## Prerequisites

- A running ZEO server (see ZODB/ZEO documentation for server setup)
- The `ZEO` Python package installed

## Step 1: Set the storage type

In your `instance.yaml`, set the storage backend to `zeo`:

```yaml
default_context:
    db_storage: zeo
```

## Step 2: Configure the server address

Tell the client where to find the ZEO server:

```yaml
default_context:
    db_storage: zeo
    db_zeo_server: "localhost:8100"
```

You can specify multiple server addresses (space-separated) for failover:

```yaml
default_context:
    db_zeo_server: "primary.example.com:8100 secondary.example.com:8100"
```

## Step 3: Configure blob storage

For ZEO, shared blob storage is recommended. All ZEO clients and the ZEO
server share a common blob directory (which may be on a network filesystem
such as NFS):

```yaml
default_context:
    db_storage: zeo
    db_zeo_server: "localhost:8100"
    db_blob_mode: shared
    db_blob_location: /srv/zodb/blobs
```

Alternatively, you can use cache mode where blobs are fetched from the ZEO
server on demand:

```yaml
default_context:
    db_blob_mode: cache
    db_blob_location: /var/cache/zodb/blobs
    db_blob_cache_size: 10737418240  # 10 GB
```

## Optional: Enable persistent client cache

To persist the cache across restarts (reducing startup time and ZEO server
load), set a client name:

```yaml
default_context:
    db_storage: zeo
    db_zeo_server: "localhost:8100"
    db_zeo_client: "client1"
    db_zeo_var: /var/cache/zeo
    db_zeo_cache_size: 256MB
```

Each client in a multi-instance deployment should have a unique
`db_zeo_client` value so that cache files do not collide.

## Complete example

```yaml
default_context:
    initial_user_name: admin
    initial_user_password: admin

    zcml_package_includes: my.awesome.addon

    # ZEO storage
    db_storage: zeo
    db_zeo_server: "zeo.example.com:8100"
    db_zeo_name: "1"

    # Shared blob directory (NFS mount)
    db_blob_mode: shared
    db_blob_location: /srv/zodb/blobs

    # Persistent client cache
    db_zeo_client: "web1"
    db_zeo_var: /var/cache/zeo
    db_zeo_cache_size: 256MB

    # ZODB object cache
    db_cache_size: 30000
```

## Next steps

- {doc}`/reference/database-zeo` -- Full reference for all ZEO options
  including authentication, read-only mode, and advanced cache settings.
- {doc}`/explanation/storage-backends` -- Comparison of all storage backends.
