# Glossary

```{glossary}
blob
    Binary large object.
    A large binary value, such as an uploaded file or image, stored outside
    the pickled object state -- either on the filesystem or in the storage
    backend.
    See {doc}`/explanation/blob-handling`.

FileStorage
    The default ZODB storage.
    A single process keeps all object data in one `Data.fs` file, with blobs
    in an adjacent directory.
    Configured with `db_storage: direct`.

PGJsonb
    A ZODB storage backend that keeps object state as PostgreSQL JSONB,
    making it queryable with SQL.
    Provided by [zodb-pgjsonb](https://pypi.org/project/zodb-pgjsonb/).

RelStorage
    A ZODB storage backend that stores pickled object state in a relational
    database such as PostgreSQL, letting many clients share one database.

ZEO
    Zope Enterprise Objects.
    A client-server ZODB storage that lets multiple Zope processes share a
    single database over the network.

ZODB
    The Zope Object Database, the transactional object store in which Zope and
    Plone persist their content.
```
