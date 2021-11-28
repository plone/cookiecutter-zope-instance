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
    - The target directory name of the generated configuration.
    - Attention, this is relative to current directory of to cookiecutters command line options if given ()``-o`` or ``--output-dir PATH``).
    - Default: ``instance``

``var_location``
    - Zope's ``var`` directory.
    - Default: ``{{ cookiecutter.target }}/var``

``log_location``
    - Base directory for all log files.
    - Default: ``{{ cookiecutter.var_location }}/log``

``http_host``
    - IP address or hostname the HTTP server binds to.
    - Default: ``localhost``

``http_port``
    - Port number the HTTP server binds to.
    - Default: ``8080``

``threads``
    - Specify the number of worker threads used to service requests.
    - Default: ``4`` (since this is the waitress default)

``max_request_body_size``
    - Specify the maximum request body size in bytes.
    - Default: ``1073741824`` (since this is the waitress default)

``clear_untrusted_proxy_headers``
    - TODO
    - Allowed values: ``false`` or ``true``
    - Default: ``false``

``environment``
    - The environment set in ``zope.conf``.
    - Values: It is a dictionary with key/value pairs.
    - Default:

    .. code-block:: JSON
    {
        "zope_i18n_compile_mo_files": "true",
        "CHAMELEON_CACHE": "{{ cookiecutter.var_location }}/cache"
    }


Development
-----------

TODO

ZCML
----

TODO

Locales
-------

``locales``
    Specify a locales directory.
    Relative to the targets ``etc`` directory.
    Default: empty

    This registers a locales directory with extra or different translations.
    Given you want to override a few translations from the ``plone`` domain in the English language.
    Then  add a ``en/LC_MESSAGES/plone.po`` file in this directory, with standard headers at the top, followed by something like this:

    .. code-block:: po

        #. Default: "You are here:"
        msgid "you_are_here"
        msgstr "You are very welcome here:"

    Translations for other message ids are not affected and will continue
    to work.

Database
--------

TODO

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
