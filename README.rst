=================================
It bakes configuration for Zope 5
=================================

**BETA QUALITY CODE** - all features are in, but more real world testing is needed, please try and report!

``cookiecutter-zope-instance`` is a `cookiecutter <https://cookiecutter.readthedocs.io>`_ template to create a full and complex configuration of a `Zope <https://zope.org>`_ WSGI instance.

.. contents :: **Contents**

Features
========

- Creates basic file-system structure with ``zope.conf``, ``zope.ini``, ``site.zcml`` and  inital user.
- Set Zope's main configuration options.
- Configure different database backends such as local file-system storage`, `RelStorage` or `ZEO`.
- Enable development options.

All non-ancient features of `plone.recipe.zope2instance <https://pypi.org/project/plone.recipe.zope2instance/>`_ are provided plus new features.


Usage
=====

Install latest cookiecutter from GitHub with ``pip install "cookiecutter"``.

Prepare a ``instance.yaml`` with the parameters needed. A minimal example is (add option as needed):

.. code-block:: YML

    default_context:
        initial_user_name: 'admin'
        initial_user_password: 'admin'

        load_zcml:
            package_includes: ['my.awesome.addon']

        db_storage: direct

Run:

.. code-block:: bash

    cookiecutter -f --no-input --config-file instance.yaml gh:plone/cookiecutter-zope-instance


Options
=======

Base Locations
--------------

``target``
    The target directory name of the cookiecutter generated configuration.
    This is also the so called *INSTANCEHOME*.

    Attention, this is relative to current directory or to cookiecutters command line options if given (``-o PATH`` or ``--output-dir PATH``).

    Default: ``instance``

``location_clienthome``
    Zope's **clienthome** directory is were by default all writable files are written.
    Such as database with blobs, logs, PID-file, ...
    This is the only place, where the user the WSGI process is started with needs to have write access.
    Traditionally this is the **var** directory of the *instancehome*.

    Default: ``{{ cookiecutter.target }}/var``

Basic configuration
-------------------

``location_log``
    Base directory for all log files.

    Default: ``{{ cookiecutter.location_clienthome }}/log``

``wsgi_listen``
    IP address or hostname with port the HTTP server binds to.

    Default: ``localhost:8080``

``wsgi_fast_listen``
    Like *wsgi_listen*, but uses [waitress_fastlisten](https://pypi.org/project/waitress-fastlisten/).
    Needs latter package to be installed (add it to *requirements.txt*).

    Default: empty string. Switched off.


``wsgi_threads``
    Specify the number of worker threads used to service requests.

    Default: ``4`` (since this is the waitress default)

``wsgi_max_request_body_size``
    Specify the maximum request body size in bytes.

    Default: ``1073741824`` (since this is the waitress default)

``wsgi_clear_untrusted_proxy_headers``
    This tells Waitress (WSGI server) to remove any untrusted proxy headers ("Forwarded", "X-Forwarded-For", "X-Forwarded-By", "X-Forwarded-Host", "X-Forwarded-Port", "X-Forwarded-Proto") not explicitly allowed by trusted_proxy_headers.

    Allowed values: ``false`` or ``true``

    Default: ``false``

TODO: support https://docs.pylonsproject.org/projects/waitress/en/latest/arguments.html

``environment``
    The environment set in ``zope.conf``.

    Values: It is a dictionary with key/value pairs.

    Default:

    .. code-block:: JSON

        {
            "zope_i18n_compile_mo_files": "true",
            "CHAMELEON_CACHE": "{{ cookiecutter.location_clienthome }}/cache"
        }

Initial user
------------

``initial_user_name``
    Creates an initial user with the given name an "Manager" role (full web access).

    Default: ``admin``

``initial_user_password``
    Creates an initial password for the initial user.
    If empty, a password will be generated and printed after the cookiecutter generation process run.

    Default: empty string

ZCML
----

The ZCML is loaded and defined in a dictionary ``load_zcml``.

Keys and values of the dictionary are:

``package_meta``
    A list of values of ``meta.zcml`` files from packages to include.

    Default: unused, empty list.

``package_include``
    A list of values of ``configure.zcml`` files from packages to include.

    Default: unused, empty list.

``package_overrides``
    A list of values of ``overrides.zcml`` files from packages to include.

    Default: unused, empty list.

``include_file_location``
    A (relative to ``TARGET/etc``) path to a ZCML file to include.

    Default: unused, empty string.

``overrides_file_location``
    A (relative to ``TARGET/etc``) path to an overrides ZCML file to include.

    Default: unused, empty string.

``resources_directory_location``
    A relative to ``TARGET/etc``) path to an Plone resource directory to include.
    Please refer to `plone.resource <https://pypi.org/project/plone.resource>`_ for more details and setup instructions.

    Default: unused, empty string.

``locales_directory_location``
    Specify a (relative to ``TARGET/etc``) locales directory.

    Default: unused, empty string

    This registers a locales directory with extra or different translations.
    Given you want to override a few translations from the ``plone`` domain in the English language.
    Then  add a ``en/LC_MESSAGES/plone.po`` file in this directory, with standard headers at the top, followed by something like this:

    .. code-block:: po

        #. Default: "You are here:"
        msgid "you_are_here"
        msgstr "You are very welcome here:"

    Translations for other message ids are not affected and will continue
    to work.

Example:

.. code-block:: JSON

    {
        ...
        "load_zcml": {
            "package_metas": ["my.fancy.project"],
            "package_includes": ["my.fancy.project"],
            "package_overrides": ["my.fancy.project"],
            "include_file_location": "../../my_fancy_project.zcml",
            "overrides_file_location": "../../my_fance_overrides.zcml",
            "resources_directory_location": "../../my_fancy_project_resources",
            "locales_directory_location": "../../my_fancy_project_locales",
        },
        ...
    }

Database
--------

Zope/Plone offers different ZODB storage backends for different environments and needs:

- For development a simple local file based *direct* storage is all you need (aka filestorage).
- As soon as you want multiple application processes of Zope/Plone (horizontal scaling) you need to run a separate database server process and connect to it.

  - We recommend to use a Postgresql database using the *RelStorage* implementation for ZODB with *psycopg2* driver as database server in production environments.
    RelStorage supports very well MySQL (and derivatives), Oracle and SQLite 3 as database servers.
  - Zope and ZODB comes with *ZEO* (Zope Enterprise Objects). This more lightweight storage server is supported here too. It is widely used in production environment.

*Blobs* (binary large objects, like files and images) are handled in a special way:

In *direct* storage blob files are stored in a dedicated directory in filesystem.

With a *RelStorage* or *ZEO* there are two options:

1. Blobs stored within the primary database server as data.
   The application client needs a local (non-shared) cache directory for the blobs.
   This is recommended in general for *RelStorage*
2. Blobs stored in a separate dedicated filesystem directory.
   This directory is in shared usage by all application processes.
   If application processes are spread over many servers, a network filesystem such as NFS or similar must be used.
   This is recommend for *ZEO*.


Core database options:

TODO check here https://zodb.org/en/latest/reference/zodb.html#database-text-configuration

``db_storage``
    Which storage type to be configured.

    Allowed values: ``direct``, ``relstorage``, ``zeo``

    Default: ``direct``

``db_cache_size``
    Set the ZODB cache target maximum number of non-ghost objects, i.e. the number of objects which the ZODB cache will try to hold in RAM per connection.
    The actual size depends on the data.
    For each connection in the connection pool of the application process one cache is created.
    In other words one cache is created for each active parallel running thread.
    If in doubt do not touch.
    On the other hand it is a powerful setting to tune your application.

    Default: ``30000``.

``db_cache_size_bytes``
    Set the ZODB cache target total memory usage of non-ghost objects in each connection object cache.
    This setting sets an additional limit on top of ``db_cache_size``.
    The cache is kept below the value of either ``db_cache_size`` or ``db_cache_size_bytes``, whatever limit was hit first.
    If value is ``0`` the byte size check is switched off and only ``db_cache_size`` is taken into account.

    Allowed values: byte-size (integer format with postfix KB, MB, GB)

    Default: unset, empty string, database default of ``0`` is active.

``db_large_record_size``
    When object records are saved that are larger than this, a warning is issued, suggesting that blobs should be used instead.

    Allowed values: byte-size (integer format with postfix KB, MB, GB)

    Default: unset, empty string, database default of ``16MB`` is active.

``db_pool_size``
    The expected maximum number of simultaneously open connections.
    There is no hard limit (as many connections as are requested will be opened, until system resources are exhausted).
    Exceeding pool-size connections causes a warning message to be logged, and exceeding twice pool-size connections causes a critical message to be logged.

    Allowed values: integer

    Default: unset, empty string, database default of ``7`` is active.

Blobs Settings
~~~~~~~~~~~~~~

The blob settings are valid for all storages.

``db_blobs_mode``
    Set if blobs are stored *shared* within all clients or are they stored on the storage backend and the client only operates as temporary *cache*.
    For *direct* storage only *shared* applies (operates like shared with one single client).
    Attention: Do not forget to set this to *cache* if you use RelStorage!

    Allowed values: ``shared``, ``cache``

    Default: ``shared``

``db_blobs_location``
    The name of the directory where the ZODB blob data or cache (depends on *db_blobs_mode*) will be stored.

    Default: ``{{ cookiecutter.location_clienthome }}/blobs``.

``db_blobs_cache_size``
    Set the maximum size of the blob cache, in bytes.
    With many blobs and enough disk space on the client hardware this should be increased.
    If not set, then the cache size isn't checked and the blob directory will grow without bound.
    Only valid for *db_blobs_mode* *cache*.

    Default: ``6312427520`` (5GB).

``db_blobs_cache_size_check``
    Set the ZEO check size as percent of ``blobss_cache_size`` (for example, ``10`` for 10%).
    The ZEO cache size will be checked when this many bytes have been loaded into the cache.
    Only valid for *db_blobs_mode* *cache*.

    Defaults: ``10`` (10% of the blob cache size).


Direct filestorage
~~~~~~~~~~~~~~~~~~

If you have only one application process, it can open a direct ``filestorage`` database files directly without running a database server process.
For details read the `Zope configuration reference <_https://zope.readthedocs.io/en/latest/operation.html#zope-configuration-reference>`_

``db_filestorage_location``
    The filename where the ZODB data file will be stored.
    Note: Side by side with the given file other ``Data.fs.*`` files (like locks and indexes) are created.

    Defaults: ``{{ cookiecutter.location_clienthome }}/filestorage/Data.fs``.

``db_filestorage_pack_keep_old``
    If switched on, a copy of the database before packing is kept in a ``.old`` file.

    Allowed values: ``true``, ``false``.

    Default: ``true``.

``db_filestorage_quota``
    Maximum allowed size of the storage file.
    Operations which would cause the size of the storage to exceed the quota will result in a ``ZODB.FileStorage.FileStorageQuotaError`` being raised.

    Allowed values: byte-size (integer format with postfix KB,MB,GB)

    Default: unset, empty string

``db_filestorage_packer``
    The dotted name (dotted module name and object name) of a packer object.
    This is used to provide an alternative pack implementation.

    Allowed values: dotted-name (string)

    Default: unset, empty string

``db_filestorage_pack_gc``
    If switched off, then no garbage collection will be performed when packing.
    This can make packing go much faster and can avoid problems when objects are referenced only from other databases.

    Allowed values: ``true``, ``false``.

    Default: ``true``.


RelStorage
~~~~~~~~~~

`RelStorage <https://pypi.org/project/RelStorage/>`_ is a storage implementation for ZODB that stores pickles in a relational database (RDBMS).

``db_relstorage``
    Set the database server to be used.

    Allowed values: ``postgresql``, ``mysql``, ``oracle``, ``sqlite3``

    Default: ``postgresql``

``db_relstorage_keep_history``
    If this option is switched on, the adapter will create and use a history-preserving database schema (like FileStorage or ZEO).
    A history-preserving schema supports ZODB-level undo, but also grows more quickly and requires extensive packing on a regular basis.

    If this option is switched off, the adapter will create and use a history-free database schema.
    Undo will not be supported, but the database will not grow as quickly.
    The database will still require regular garbage collection (which is accessible through the database pack mechanism.)

    Allowed values: ``true``, ``false``.

    Default: ``true``.

``db_relstorage_read_only``
    If switched on, only reads may be executed against the storage.

    Allowed values: ``false``, ``true``.

    Default: ``false``.

``db_relstorage_create_schema``
    Normally, RelStorage will create or update the database schema on start-up.
    Switch it off if you need to connect to a RelStorage database without automatic creation or updates.

    Allowed values: ``true``, ``false``.

    Default: ``true``.

``db_relstorage_commit_lock_timeout``
    During commit, RelStorage acquires a database-wide lock.
    This option specifies how long to wait for the lock before failing the attempt to commit.
    Consult and understand the RelStorage documentation before using this setting.

    Default: unset, empty string, RelStorage default of ``30`` seconds is active.

RelStorage provides advanced blob caching options.
For details about caching read `RelStorage: Blobs <https://relstorage.readthedocs.io/en/latest/relstorage-options.html#blobs>`_.

``db_relstorage_blob_cache_size_check_external``
    For details read original RelStorage documentation.

    Allowed values: ``false``, ``true``.

    Default: ``false``.

``db_relstorage_blob_chunk_size``
    For details read original RelStorage documentation.

    Default: unset, empty string, RelStorage default of ``1048576`` (1 megabyte) is active.
    This option allows suffixes such as “mb” or “gb”.

RelStorage provides advanced RAM and persistent caching options.
For details about caching read `RelStorage: Database Caching <https://relstorage.readthedocs.io/en/latest/relstorage-options.html#database-caching>`_.
The descriptions below are copied mainly from there (consult the original source, it may have changed!).

``db_relstorage_cache_local_mb``
    Configures the approximate maximum amount of memory the cache should consume, in megabytes.
    Set to ``0`` to *disable* the in-memory cache (this is not recommended).

    Default: unset, empty string, RelStorage default of ``10`` is active.

``db_relstorage_cache_local_object_max``
    Configures the maximum size of an object’s pickle (in bytes) that can qualify for the *local* cache.
    The size is measured after compression.
    Larger objects can still qualify for the remote cache.

    Default: unset, empty string, RelStorage default of 16384 (1 << 14) bytes is active.

``db_relstorage_cache_local_compression``
    Configures compression within the *local* cache.
    This option names a Python module that provides two functions, "compress()" and "decompress()".
    Supported values include zlib, bz2, and none (no compression).
    If you use the compressing storage wrapper "zc.zlibstorage", this option automatically does nothing.
    With other compressing storage wrappers this should be set to none.

    Default: unset, empty string, RelStorage default of ``none`` is active (to avoid copying data more than necessary).

``db_relstorage_cache_local_dir``
    The path to a directory where the local cache will be saved when the database is closed.
    On startup, RelStorage will look in this directory for cache files to load into memory.
    The cache files must be located on a local (not network) filesystem.
    Consult and understand the *Database Caching* manual before using this setting.

``db_relstorage_cache_prefix``
    The prefix used as part of persistent cache file names.
    All clients using a database should use the same cache-prefix.

    Default: unset, empty string, RelStorage default of the database name is active.

RelStorage has extra parameters for blobs.

If your database runs replicated, RelStorage supports handling of replications.
For details about replication options read `RelStorage: Replication <https://relstorage.readthedocs.io/en/latest/relstorage-options.html#replication>`_.

``db_relstorage_replica_conf``
    For details read original RelStorage documentation.

    Default: unset, empty string

``db_relstorage_ro_replica_conf``
    For details read original RelStorage documentation.

    Default: unset, empty string

``db_relstorage_replica_timeout``
    For details read original RelStorage documentation.

    Default: unset, empty string

``db_relstorage_replica_revert_when_stale``
    For details read original RelStorage documentation.

    Default: unset, empty string

Postgresql
""""""""""

For details about the options read: `RelStorage: PostgreSQL adapter options <https://relstorage.readthedocs.io/en/latest/postgresql/options.html>`_

``db_relstorage_postgresql_driver``:
    Driver to use.

    Allowed values: ``psycopg2``, ``psycopg2 gevent``, ``psycopg2cffi``, ``pg8000``.

    Default: ``psycopg2``

``db_relstorage_postgresql_dsn``
    Specifies the data source name for connecting to PostgreSQL. A PostgreSQL DSN is a list of parameters separated with whitespace. A typical DSN looks like:
    ``dbname='plone' user='username' host='localhost' password='secret'``

    Default: unset, empty string

MySQL
"""""

For details about the options read: `RelStorage: MySQL adapter options <https://relstorage.readthedocs.io/en/latest/mysql/options.html>`_

``db_relstorage_mysql_driver``:
    Driver to use.

    Allowed values: ``MySQLdb``, ``gevent MySQLdb``, ``PyMySQL``, ``C MySQL Connector/Python``.

    Default: ``psycopg2``

``db_relstorage_mysql_parameters``:
    A dictionary with all MySQL parameters. This depends on the driver.

    Example:

    .. code-block:: JSON

        {
            ...
            "db_relstorage_mysql_parameters": {
                "host": "localhost",
                "user": "plone",
                "passwd": "secret",
                "db": "plone"
            },
            ...
        }

Oracle
""""""

For details about the options read: `RelStorage: Oracle adapter options <https://relstorage.readthedocs.io/en/latest/mysql/options.html>`_

``db_relstorage_oracle_user``
    The Oracle account name.

    Default: unset, empty string

``db_relstorage_oracle_password``
    The Oracle account password.

    Default: unset, empty string

``db_relstorage_oracle_dsn``
    The Oracle data source name. The Oracle client library will normally expect to find the DSN in ``/etc/oratab``

    Default: unset, empty string

``db_relstorage_commit_lock_id``
    During commit, RelStorage acquires a database-wide lock.
    This option specifies the lock ID.
    This option currently applies only to the Oracle adapter, but is documented under the global settings.

    Default: unset, empty string

SQLite
""""""

For details about the options read: `RelStorage: SQLite adapter options <https://relstorage.readthedocs.io/en/latest/sqlite3/options.html>`_

``db_relstorage_sqlite3_driver``
    Allowed values: ``sqlite3``, ``gevent sqlite3``

    Default: ``sqlite3``

``db_relstorage_sqlite3_data_dir``
    The path to a directory to hold the data.
    Choosing a dedicated directory is strongly recommended.
    A network filesystem is generally not recommended.

    Default: ``{{ cookiecutter.location_clienthome }}/sqlite3/``

``db_relstorage_sqlite3_gevent_yield_interval``
    Only used if the driver is ``gevent sqlite``

    Default: unset, empty string - RelStorage has an internal default of 100.

``db_relstorage_sqlite3_pragma``
    For advanced tuning, nearly the entire set of SQLite PRAGMAs are available.

    Default: unset, empty dictionary.


ZEO
~~~

ZEO is a mature client-server storage created for ZODB for sharing a single storage among many clients.

All options can be found in the `Zope Configuration Reference under "<zeoclient> (ZODB.config.ZEOClient)"" <https://zope.readthedocs.io/en/latest/operation.html#zope-configuration-reference>`_

Main settings:

``db_zeo_server``
    Set the server address of the ZEO server.
    You can set more than one address (white space delimited).
    Alternative addresses will be used if the primary address is down.

    Default: ``localhost:8100``.

``db_zeo_name``
    Set the storage name of the ZEO storage.

    Default: ``1``.

Caching settings

*db_cache_size* and *db_cache_size_bytes* is taken into account.
Additional persistent caching is possible.

TODO: figure out what *cache-size* in ZEO client means.

``db_zeo_client``
    Enables persistent cache files.
    Set the persistent cache name that is used to construct the cache filenames.
    This enables the ZEO cache to persist across application restarts.

    Persistent cache files are disabled by default.
    If disabled, the client creates a temporary cache that will only be used by the current object.

    The string passed here is used to construct the cache filenames.

    Allowed values: string.

    Default: unset.

``db_zeo_var``
    The directory where persistent cache files are stored.
    By default cache files, if they are persistent, are stored in the current directory.    Used in the ZEO storage snippets to configure the ZEO var folder, which is used to store persistent ZEO client cache files.

    Default: unset, empty string, the system temporary folder is used.

``db_zeo_cache_size``
    Set the size of the file based ZEO client cache.
    The ZEO cache is a disk based cache shared between application threads.
    It is stored either in temporary files or, in case you activate persistent cache files with the option ``client`` (see below), in the folder designated by the ``db_zeo_var`` option.

    Default: ``128MB``.

ZEO supports authentication.
You need to activate ZEO authentication on the server side as well, for this to work.
Without this anyone that can connect to the database servers socket can read and write arbitrary data.

``db_zeo_username``
    Enable ZEO authentication and use the given username when accessing the ZEO server.
    It is obligatory to also specify a zeo-password.

    Default: unset, empty string, no authentication.

``db_zeo_password``
    Password to use when connecting to a ZEO server with authentication enabled.

    Default: unset, empty string.

``db_zeo_realm``
    Authentication realm to use when authentication with a ZEO server.

    Default: ``ZEO``.

ZEO has some advance options.
If in doubt better do not touch them.


``db_zeo_read_only_fallback``
    A flag indicating whether a read-only remote storage should be acceptable as a fallback when no writable storages are available.

    Allowed values: ``false``, ``true``.

    Default: ``false``

``db_zeo_read_only``
    Set zeo client as read only.

    Allowed values: ``false``, ``true``.

    Default: ``false``

``db_zeo_drop_cache_rather_verify``
    Indicates that the cache should be dropped rather than verified when the verification optimization is not available
    (e.g. when the ZEO server restarted).

    Allowed values: ``false``, ``true``.

    Default: ``false``.

Development
-----------

``debug_mode``
    Allowed values: ``true``, ``false``.

``verbose_security``
    Switches verbose security on (and switch to the Python security implementation).

    Allowed values: ``true``, ``false``.

    Default: ``false``


Enable profiling with `repoze.profile <>`_.
Ensure to execute ``pip install repoze.profile`` before switching this on.

``profile_repoze``
    Allowed values: ``true``, ``false``.

``profile_repoze_log_filename``
  Filename of the raw profile data.
  Default to ``profile-SECTIONNAME.raw``.
  This file contains the raw profile data for further analysis.

``profile_repoze_cachegrind_filename``
  If the package ``pyprof2calltree`` is installed, another file is written.
  It is meant for consumption with any cachegrind compatible application.
  Defaults to ``cachegrind.out.SECTIONNAME``.

``profile_repoze_discard_first_request``
  Defaults to ``true``.
  See `repoze.profile docs <https://repozeprofile.readthedocs.io/en/latest/#configuration-via-python>`_ for details.

``profile_repoze_path``
  Defaults to ``/__profile__``.
  The path for through the web access to the last profiled request.

``profile_repoze_flush_at_shutdown``
  Defaults to ``true``.
  See `repoze.profile docs <https://repozeprofile.readthedocs.io/en/latest/#configuration-via-python>`_ for details.

``profile_repoze_unwind``
  Defaults to ``false``.
  See `repoze.profile docs <https://repozeprofile.readthedocs.io/en/latest/#configuration-via-python>`_ for details.


Example Configuration
=====================

TODO

This looks like so:

.. code-block:: JSON

    {}



Rationale
=========

Base
----

Problem
    We no longer want to use buildout and need a replacement for the old feature rich buildout recipe `plone.recipe.zope2instance` to configure zope.
    The old recipe uses python string templates and is not very intuitive to write and maintain.

Idea
    `cookiecutter <https://cookiecutter.readthedocs.io>`_ is a widespread utility to create text-based code and configuration file-system structures.
    Let's utilize it's power and wrap it with a thin package to simplify it's usage and add minor features needed for out use case.

Difference
----------

to ``plone.recipe.zope2instance``

variable names
    They changed.
    "Namespaces are one honking great idea -- let's do more of those!" (import this)

``Sentry``
    It was possible to configure Sentry.
    Now use `collective.sentry <https://pypi.org/project/collective.sentry/>`_ - much better.

The ``ctl.py``
    Move now to plonectl?

Contributors
============

Idea and initial implementation by Jens Klein (`Klein & Partner KG <https://kleinundpartner.at>`_ of `BlueDynamics Alliance <https://bluedynamics.com>`_).
Then donated to the Plone Foundation.
