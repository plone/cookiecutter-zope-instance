# Sample configurations

<!-- diataxis: reference -->

This page collects complete, copy-paste `instance.yaml` configurations, one
per storage backend, in development and production variants.
Each configuration is self-contained and generates a working instance as-is.

For step-by-step guidance, see the {doc}`/how-to/index` guides.
For the trade-offs between backends, see {doc}`/explanation/storage-backends`.
For the meaning of every individual setting, see the reference pages linked
from each section below.

:::{important}
The passwords shown here are placeholders for local use.
Never commit real credentials.
In production, set `initial_user_password` and database passwords from the
environment instead.
See {doc}`/how-to/use-environment-variables`.
:::

(sample-filestorage-dev)=

## Filestorage (development)

The minimal configuration.
A single process opens a local `Data.fs` file directly, with no database
server.
This is the base that the other configurations extend.

```yaml
default_context:
    # Serving
    wsgi_listen: localhost:8080

    # Initial admin user
    initial_user_name: admin
    initial_user_password: admin

    # Add-ons
    zcml_package_includes: my.awesome.addon

    # Storage
    db_storage: direct
```

See {doc}`database-direct` and {doc}`basic-config`.

(sample-relstorage-prod)=

## RelStorage with PostgreSQL (production)

The recommended backend for production deployments that scale horizontally.
Pickles are stored in PostgreSQL, and each client keeps a local blob cache.

```yaml
default_context:
    # Serving (bind to localhost when behind a reverse proxy)
    wsgi_listen: 127.0.0.1:8080

    # Initial admin user (override the password from the environment)
    initial_user_name: admin
    initial_user_password: admin

    # Add-ons
    zcml_package_includes: my.awesome.addon

    # Storage
    db_storage: relstorage
    db_blob_mode: cache
    db_relstorage: postgresql
    db_relstorage_postgresql_dsn: "host='db' dbname='plone' user='plone' password='secret'"
    db_relstorage_keep_history: false

    # Caches
    db_cache_size: 50000
    db_cache_size_bytes: 1500MB
    db_blob_cache_size: 10737418240  # 10 GB
```

See {doc}`database-relstorage`, {doc}`database-blobs`, and {doc}`database-common`.

(sample-zeo-prod)=

## ZEO client (production)

A client that connects to a shared ZEO server.
Blobs are shared through a common directory (for example, an NFS mount).
Each client in a multi-instance deployment needs a unique `db_zeo_client`.

```yaml
default_context:
    # Serving (bind to localhost when behind a reverse proxy)
    wsgi_listen: 127.0.0.1:8080

    # Initial admin user (override the password from the environment)
    initial_user_name: admin
    initial_user_password: admin

    # Add-ons
    zcml_package_includes: my.awesome.addon

    # Storage
    db_storage: zeo
    db_zeo_server: "zeo.example.com:8100"

    # Shared blob directory (for example, an NFS mount)
    db_blob_mode: shared
    db_blob_location: /srv/zodb/blobs

    # Persistent client cache (unique name per client)
    db_zeo_client: web1
    db_zeo_var: /var/cache/zeo
    db_zeo_cache_size: 256MB

    # Object cache
    db_cache_size: 30000
```

See {doc}`database-zeo`, {doc}`database-blobs`, and {doc}`database-common`.

(sample-pgjsonb-prod)=

## PGJsonb (production)

A cloud-native backend that stores object state as PostgreSQL JSONB.
Blobs live in PostgreSQL `bytea` by default; the generic `db_blob_*` settings
do not apply.

```yaml
default_context:
    # Serving (bind to localhost when behind a reverse proxy)
    wsgi_listen: 127.0.0.1:8080

    # Initial admin user (override the password from the environment)
    initial_user_name: admin
    initial_user_password: admin

    # Add-ons
    zcml_package_includes: my.awesome.addon

    # Storage
    db_storage: pgjsonb
    db_pgjsonb_dsn: "dbname='zodb' user='zodb' host='db' port='5432'"
    db_pgjsonb_history_preserving: false

    # Object cache
    db_cache_size: 50000
    db_pgjsonb_cache_local_mb: 64
```

See {doc}`database-pgjsonb` and {doc}`database-common`.

(sample-pgjsonb-s3-prod)=

## PGJsonb with S3 blob tiering (production)

The same backend, with blobs larger than the threshold tiered to
S3-compatible object storage instead of PostgreSQL `bytea`.
Requires the `zodb-pgjsonb[s3]` extra.
This is PGJsonb's own S3 tiering and does not use the z3blobs wrapper.

```yaml
default_context:
    # Serving (bind to localhost when behind a reverse proxy)
    wsgi_listen: 127.0.0.1:8080

    # Initial admin user (override the password from the environment)
    initial_user_name: admin
    initial_user_password: admin

    # Add-ons
    zcml_package_includes: my.awesome.addon

    # Storage
    db_storage: pgjsonb
    db_pgjsonb_dsn: "dbname='zodb' user='zodb' host='db' port='5432'"
    db_pgjsonb_history_preserving: false

    # S3 tiered blob storage (credentials via the boto3 chain when omitted)
    db_pgjsonb_s3_bucket_name: zodb-blobs
    db_pgjsonb_s3_region: eu-west-1
    db_pgjsonb_blob_threshold: 100KB
    db_pgjsonb_blob_cache_dir: /var/cache/zodb-blobs
    db_pgjsonb_blob_cache_size: 2GB

    # Object cache
    db_cache_size: 50000
    db_pgjsonb_cache_local_mb: 64
```

Set `db_pgjsonb_s3_endpoint_url` for MinIO or other S3-compatible stores.
See {doc}`database-pgjsonb` and {doc}`/explanation/blob-handling`.

## S3 blob storage (z3blobs wrapper)

The z3blobs wrapper redirects blob handling to S3-compatible object storage.
It wraps a `direct`, `relstorage`, or `zeo` backend (not `pgjsonb`).
Add the following keys to any of the configurations above except PGJsonb.

```yaml
default_context:
    # ... a direct, relstorage, or zeo configuration from above ...

    # S3 blob wrapper
    db_z3blobs_enabled: true
    db_z3blobs_bucket_name: prod-blobs
    db_z3blobs_cache_dir: /var/cache/s3blobs
    db_z3blobs_cache_size: 10GB
    db_z3blobs_s3_region: eu-west-1
```

See {doc}`database-z3blobs` and {doc}`/explanation/blob-handling`.
