=================================
It bakes configuration for Zope 5
=================================

**WIP: ALPHA QUALITY CODE**

``cookiecutter-zope-instance`` is a cookiecutter template to create a full and complex configuration of a `Zope <https://zope.org>`_ WSGI instance.

.. contents :: **Contents**

Features
========

- Creates basic filesystem structure with ``zope.conf``, ``zope.ini`` and ``site.zcml`` with package-includes.
- Add inituser
- Set Zope's main configuration options
- Configure different database backends such as local filesystem storage`, `RelSorage` or `ZEO`.
- Enable profiling.

In future all non-ancient features of `plone.recipe.zope2instance <>`_ are planned to provide.


Usage
=====

Run ``cookiecutter -f https://github.com/bluedynamics/cookiecutter-zope-instance`` and answer tons of questions.

Better: Prepare a ``cookiecutter.json`` with all option given and run cookiecutter with it.


Options
=======

Basic configuration
-------------------

``target``
    The target directory name of the generated configuration.

    Attention, this is relative to current directory or to cookiecutters command line options if given ()``-o`` or ``--output-dir PATH``).

    Default: ``instance``

``var_location``
    Zope's ``var`` directory.

    Default: ``{{ cookiecutter.target }}/var``

``log_location``
    Base directory for all log files.

    Default: ``{{ cookiecutter.var_location }}/log``

``http_host``
    IP address or hostname the HTTP server binds to.

    Default: ``localhost``

``http_port``
    Port number the HTTP server binds to.

    Default: ``8080``

``threads``
    Specify the number of worker threads used to service requests.

    Default: ``4`` (since this is the waitress default)

``max_request_body_size``
    Specify the maximum request body size in bytes.

    Default: ``1073741824`` (since this is the waitress default)

``clear_untrusted_proxy_headers``
    This tells Waitress (WSGI server) to remove any untrusted proxy headers ("Forwarded", "X-Forwared-For", "X-Forwarded-By", "X-Forwarded-Host", "X-Forwarded-Port", "X-Forwarded-Proto") not explicitly allowed by trusted_proxy_headers.

    Allowed values: ``false`` or ``true``

    Default: ``false``

``environment``
    The environment set in ``zope.conf``.

    Values: It is a dictionary with key/value pairs.

    Default:

    .. code-block:: JSON

        {
            "zope_i18n_compile_mo_files": "true",
            "CHAMELEON_CACHE": "{{ cookiecutter.var_location }}/cache"
        }

Initial user
------------

``initial_user_name``
    Creates an initial user with the given name an "Manager" role (full web access).

    Default: ``admin``

``initial_user_password``
    Creates an initial password for the initial user.
    If empty, a passwort will be generated and printed after the cookiecutter generation process run.

    Default: empty string

ZCML
----

The ZCML is loaded an defined in a dictionary ``load_zcml``.

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

Zope/Plone offers different storage backends for different environments and needs:

- For development a simple local file based direct storage is all you need.
- As soon as you run more than one instance of Zope/Plone (horizontal scaling) a storage server needs to e configured.
- We recommend to use a Postgresql database over RelStorage as the storage server in production environments.
- RelStorage also supports MySQL (and derivates) and Oracle as storae servers.
- Since Zope comes with an own storage server (ZEO - Zope Enterprise Objects) this is supported here as well. It can be used in production environment too.
- Blobs (binary large objects, like files and images) are handled in a special way:

  - They either are stored within the primary database or as a separate filesystem storage.
  - in direct storage Blob files are in an own directory
  - If stored  the primary database it is possible to choose how blobs are handled.

    - Options are to store blobs in the primary database or in a shared filesystem.
    - If Blobs are in the primary database, the client needs only a local Blob cache.
    - If Blobs are stored (side-by-side with the storageserver) in the filesystem, it needs a central *shared* folder (if spread over many servers using NFS or similar).
    - For Postgresql it is recommend to store blobs in the database.
      However, it can be configured to store them separatly.
      Read the RelStorage documentation for details on other databases.
    - For ZEO blobs can be configured to be stored within ZEO or in a shared folder.
      Recommendation is to use a shared folder.

Common options:

``database``
    Which storge type to be confiured.

    Allowed values: ``direct``, ``relstroage``, ``zeo``

    Default: ``direct``

``blobs_mode``
    Set if blobs are stored *shared* within all clients or are they stored on the storage backend and the client only operates as temporary *cache*.
    For *direct* storage only *shared* applies (operates like shared with one single client).
    Attention: Do not forget to set this to *cache* if you use RelStorage!

    Allowed values: ``shared``, ``cache``

    Default: ``shared``

``blobs_location``
    The name of the directory where the ZODB blob data or cache will be stored.

    Default: ``{{ cookiecutter.var_location }}/blobs``.



Direct storage
~~~~~~~~~~~~~~

If you have only one application process, it can open ``filestorage`` database files directly without running a database server process.


``filestorage_location``
    The filename where the ZODB data file will be stored.

    Defaults: ``{{ cookiecutter.var_location }}/filestorage/Data.fs``.

RelStorage
~~~~~~~~~~

> `RelStorage <https://pypi.org/project/RelStorage/>`_ is a storage implementation for ZODB that stores pickles in a relational database (RDBMS).

``relstorage``
    Set the database server to be used.

    Allowed values: ``postgresql``, ``mysql``, ``oracle``, ``sqllite3``

    Default: ``postgresql``

Postgresql
""""""""""

For details about the options read: `RelStorage: PostgreSQL adapter options <https://relstorage.readthedocs.io/en/latest/postgresql/options.html>`_

``postgresql_driver``:
    Driver to use.

    Allowed values: ``psycopg2``, ``psycopg2 gevent``, ``psycopg2cffi``, ``pg8000``.
    Default: ``psycopg2``

``dsn``
    Specifies the data source name for connecting to PostgreSQL. A PostgreSQL DSN is a list of parameters separated with whitespace. A typical DSN looks like:
    ``dbname='plone' user='username' host='localhost' password='secret'``

    Default: unset, empty string

MySQL
"""""

For details about the options read: `RelStorage: MySQL adapter options <https://relstorage.readthedocs.io/en/latest/mysql/options.html>`_

``mysql_driver``:
    Driver to use.

    Allowed values: ``MySQLdb``, ``gevent MySQLdb``, ``PyMySQL``, ``C MySQL Connector/Python``.

    Default: ``psycopg2``

``mysql_parameters``:
    A dictionary with all MySQL parameters. This depends on the driver.

    Example:

    .. code-block:: JSON

        {
            ...
            "mysql_parameters": {
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

``oracle_user``
    The Oracle account name.

    Default: unset, empty string

``oracle_password``
    The Oracle account password.

    Default: unset, empty string

``oracle_dsn``
    The Oracle data source name. The Oracle client library will normally expect to find the DSN in ``/etc/oratab``

    Default: unset, empty string

SQLite
""""""

For details about the options read: `RelStorage: SQLite adapter options <https://relstorage.readthedocs.io/en/latest/sqlite3/options.html>`_

``sqlite3_driver``
    Allowed values: ``sqlite3``, ``gevent sqlite3``

    Default: ``sqlite3``

``sqlite3_data_dir``
    The path to a directory to hold the data.
    Choosing a dedicated directory is strongly recommended.
    A network filesystem is generally not recommended.

    Default: ``{{ cookiecutter.var_location }}/sqlite3/``

``sqlite3_gevent_yield_interval``
    Only used if the driver is ``gevent sqlite``

    Default: unset, empty string - RelStorage has an internal default of 100.

``sqlite3_pragma``
    For advanced tuning, nearly the entire set of SQLite PRAGMAs are available.
    Default: unset, empty dictionary.


ZEO
~~~

**not implemented**

Development
-----------

``debug_mode``
    Allowed values: ``on``, ``off``.

``verbose_security``
    Switches verbose security on (and switch to the Python security implementation).

    Allowed values: ``on``, ``off``.

    Default: ``off``

TODO: (not implmented)

``use_profiler``
    Allowed values: ``on``, ``off``.

profile_log_filename
  Filename of the raw profile data.
  Default to ``profile-SECTIONNAME.raw``.
  This file contains the raw profile data for further analysis.

profile_cachegrind_filename
  If the package ``pyprof2calltree`` is installed, another file is written.
  It is meant for consumation with any cachegrind compatible application.
  Defaults to ``cachegrind.out.SECTIONNAME``.

profile_discard_first_request
  Defaults to ``true``.
  See `repoze.profile docs <https://repozeprofile.readthedocs.io/en/latest/#configuration-via-python>`_ for details.

profile_path
  Defaults to ``/__profile__``.
  The path for through the web access to the last profiled request.

profile_flush_at_shutdown
  Defaults to ``true``.
  See `repoze.profile docs <https://repozeprofile.readthedocs.io/en/latest/#configuration-via-python>`_ for details.

profile_unwind
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

Problem
    We no longer want to use buildout and need a replacement for the old feature rich buildout recipe `plone.recipe.zope2instance` to configure zope.
    The old recipe uses python string templates and is not very intuitive to write and maintain.

Idea
    `cookiecutter <https://cookiecutter.readthedocs.io>`_ is a widespread utility to create text-based code and configuration file-system structures.
    Let's utilize it's power and wrap it with a thin package to simplfy it's usage and add minor features needed for out use case.
