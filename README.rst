=================================
It bakes configuration for Zope 5
=================================

**WIP: ALPHA QUALITY CODE**

``cookiecutter-zope-instance`` is a cookiecutter template to create a full and complex configuration of a `Zope <https://zope.org>`_ WSGI instance.

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

    .. code-block:: json

        {
            "zope_i18n_compile_mo_files": "true",
            "CHAMELEON_CACHE": "{{ cookiecutter.var_location }}/cache"
        }

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
- As soon as you run more than one instance of Zope/Plone a storage server needs to e configured.
- We recommend to use a Postgresql database over RelStorage as the storage server in production environments.
- RelStorage also supports MySQL (and derivates) and Oracle as storae servers.
- Since Zope comes with an own storage server (ZEO - Zope Enterprise Objects) this is supported here as well. It can be used in production environment too.
- Blobs (binary large objects, like files and images) are handled in a special way:

  - They either are stored within the primary database or as a separate filesystem storage.
  - in direct storage Blob files are in an own directory
  - If stored  the primary database it is possible to choose how blobs are handled.

    - Options are to store blobs in the primary database or in a shared filesystem.
    - If Blobs are in the primary database, the client needs only a local Blob cache.
    - If Blobs are stored side-by-side in the filesystem, it needs a central shared folder (if spread over many servers using NFS or similar).
    - For Postgresql it is recommend to store blobs in the database.
      However, it can be configured to store them separatly.
      Read the RelStorage documentation for details on other databases.
    - For ZEO blobs can be configured to be stored within ZEO or in a shared folder.
      Recommendation is to use a shared folder.


Direct storage
~~~~~~~~~~~~~~

If you have only one application process, it can open ``filestorage`` database files directly without running a database server process.


``filestorage_location``
    The filename where the ZODB data file will be stored.

    Defaults: ``{{ cookiecutter.var_location }}/filestorage/Data.fs``.

``blobs_location``
    The name of the directory where the ZODB blob data will be stored.

    Default: ``{{ cookiecutter.var_location }}/blobs``.

RelStorage
~~~~~~~~~~

**not implemented**

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
