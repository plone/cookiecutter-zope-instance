# Understanding Storage Backends

<!-- diataxis: explanation -->

Zope and Plone use ZODB (the Zope Object Database) to persist Python objects.
ZODB is storage-agnostic -- the actual persistence layer is pluggable. This
page explains the four storage backends supported by
`cookiecutter-zope-instance`, when to use each, and the trade-offs involved.

## The four backends at a glance

| Backend | Best For | Horizontal Scaling | Undo Support | External Dependencies |
|---|---|---|---|---|
| **direct** (filestorage) | Development, single-process | No (single process only) | Yes (built-in) | None |
| **relstorage** (PostgreSQL, MySQL, Oracle, SQLite) | Production, horizontal scaling | Yes (multiple app processes) | Optional (history-preserving mode) | RDBMS server |
| **zeo** | Production, moderate scaling | Yes (multiple app processes) | Yes (built-in) | ZEO server process |
| **pgjsonb** | Cloud-native, SQL-queryable ZODB | Yes (multiple app processes) | Optional (history-preserving mode) | PostgreSQL 14+ |

## Direct filestorage

Direct filestorage is the simplest backend. It stores all object data in a
single `Data.fs` file on the local filesystem. No external database server is
required.

**When to use it:**

- Local development
- Single-process deployments (one Zope/Plone instance)
- Quick prototyping and testing

**Limitations:**

Only one operating system process can open a filestorage at a time. If you
need to run multiple Zope application processes for load balancing, you must
use one of the other backends.

Filestorage is history-preserving by nature: every transaction is appended to
the file. The file grows over time and must be packed periodically to reclaim
space from old revisions.

## RelStorage

[RelStorage](https://relstorage.readthedocs.io/) stores ZODB object pickles
in a relational database. PostgreSQL is the recommended RDBMS, but MySQL,
Oracle, and SQLite are also supported.

**When to use it:**

- Production environments that need horizontal scaling (multiple Zope
  processes sharing one database)
- Environments where you already have a well-managed RDBMS
- When you need mature, battle-tested multi-process ZODB

**Architecture:**

Each Zope application process connects directly to the relational database.
Object pickles are stored as binary data in database rows. RelStorage handles
conflict resolution, garbage collection, and (optionally) history
preservation.

**Trade-offs:**

- Requires an RDBMS server to be provisioned and maintained
- Blob handling requires choosing between *cache* mode (blobs in the RDBMS,
  cached locally) or *shared* mode (blobs on a shared filesystem)
- History-free mode gives better performance but disables ZODB-level undo

## ZEO (Zope Enterprise Objects)

[ZEO](https://zeo.readthedocs.io/) is the original client-server protocol
for ZODB. A dedicated ZEO server process manages the filestorage, and
multiple Zope client processes connect to it over TCP.

**When to use it:**

- Production environments where you prefer a pure-Python, ZODB-native
  solution without an external RDBMS
- Deployments where shared NFS blob storage is readily available
- Existing infrastructure already running ZEO

**Architecture:**

The ZEO server holds the actual filestorage and mediates access. Each Zope
client maintains a local object cache (in memory and optionally on disk) for
performance. Invalidation messages keep client caches consistent.

**Trade-offs:**

- The ZEO server is a single point of failure (though you can configure
  failover addresses)
- Blob sharing typically requires a network filesystem (NFS)
- Somewhat lower throughput than RelStorage under heavy write loads

## PGJsonb

[zodb-pgjsonb](https://pypi.org/project/zodb-pgjsonb/) is a newer storage
adapter that stores ZODB object state as PostgreSQL JSONB columns rather than
opaque binary pickles. A Rust-based codec
([zodb-json-codec](https://pypi.org/project/zodb-json-codec/)) transcodes
between Python pickle format and JSON.

**When to use it:**

- Cloud-native deployments where a managed PostgreSQL service (RDS, Cloud SQL,
  AlloyDB, etc.) replaces local filestorage and blob directories
- When you want to query ZODB data directly with SQL/JSONB operators
- Modern PostgreSQL-centric architectures
- Integration with tools that consume JSON natively (analytics, reporting)

**Architecture:**

Object state is transcoded from pickle to JSON on write, and from JSON back
to pickle on read. The JSON representation is stored in a PostgreSQL JSONB
column, making it indexable and queryable. Blobs are stored in PostgreSQL
`bytea` columns by default, with optional tiering to S3-compatible object
storage for large blob volumes.

**Trade-offs:**

- Requires PostgreSQL 14 or later
- Transcoding adds CPU overhead on every read/write (mitigated by the Rust
  implementation)
- Newer and less battle-tested than RelStorage or ZEO
- Blob handling is fundamentally different from the other backends

## S3 Blob Wrapper (z3blobs)

[zodb-s3blobs](https://pypi.org/project/zodb-s3blobs/) is not a fifth storage
backend but a **wrapper** that can be applied to any of the first three backends
(`direct`, `relstorage`, or `zeo`). When enabled, it intercepts all blob
operations and redirects them to S3-compatible object storage, maintaining a
local LRU cache for performance.

**When to use it:**

- Deployments where local or shared filesystem blob storage is impractical
- Containerized environments where blob data must survive container restarts
- When you want to offload large blob volumes to object storage

**How it works:**

The selected backend (e.g. filestorage or RelStorage) handles all non-blob
ZODB operations normally. The z3blobs wrapper takes over blob reads and writes,
storing blobs in an S3 bucket and caching recently accessed blobs locally.
The inner storage's own blob directives are suppressed automatically.

**Not compatible with PGJsonb:**

PGJsonb handles blobs natively via PostgreSQL `bytea` with optional S3 tiering.
Wrapping PGJsonb with z3blobs is a configuration error and will be rejected
during instance generation.

## Choosing a backend

For most teams, the decision comes down to:

1. **Development or single-process?** Use `direct`.
2. **Need multi-process with an existing RDBMS?** Use `relstorage`.
3. **Need multi-process, prefer ZODB-native simplicity?** Use `zeo`.
4. **Cloud-native or want SQL-queryable ZODB data on PostgreSQL?** Use `pgjsonb`.
5. **Need S3 blob storage with direct, relstorage, or zeo?** Enable `db_z3blobs_enabled`.

All four backends support the same ZODB API, so switching between them is a
configuration change (plus data migration). Your application code does not
need to change.
