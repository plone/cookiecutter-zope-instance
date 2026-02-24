# Basic Configuration

<!-- diataxis: reference -->

Core WSGI server, environment, and request-handling settings.

## WSGI Server

| Setting | Default | Allowed Values |
|---|---|---|
| `location_log` | `{{ cookiecutter.location_clienthome }}/log` | path |
| `wsgi_listen` | `localhost:8080` | host:port |
| `wsgi_fast_listen` | *(unset)* | host:port |
| `wsgi_threads` | `4` | integer |
| `wsgi_max_request_body_size` | `1073741824` | integer (bytes) |
| `wsgi_clear_untrusted_proxy_headers` | `false` | `true`, `false` |
| `wsgi_app_entrypoint` | `egg:Zope#main` | entrypoint |

**`wsgi_fast_listen`** -- Like `wsgi_listen`, but uses [waitress_fastlisten](https://pypi.org/project/waitress-fastlisten/). Needs the latter package to be installed (add it to *requirements.txt*).

**`wsgi_clear_untrusted_proxy_headers`** -- Tells Waitress (WSGI server) to remove any untrusted proxy headers (`Forwarded`, `X-Forwarded-For`, `X-Forwarded-By`, `X-Forwarded-Host`, `X-Forwarded-Port`, `X-Forwarded-Proto`) not explicitly allowed by `trusted_proxy_headers`.

## Environment

| Setting | Default |
|---|---|
| `environment` | `{"zope_i18n_compile_mo_files": "true", "CHAMELEON_CACHE": "..."}` |
| `environment_paths` | `["CHAMELEON_CACHE"]` |

**`environment`** -- The environment set in `zope.conf`. Values: a dictionary with key/value pairs. Default includes `zope_i18n_compile_mo_files` set to `true` and `CHAMELEON_CACHE` set to `{{ cookiecutter.location_clienthome }}/cache`.

:::{attention}
Due to a [bug in cookiecutter 2.2.0 to 2.5.0](https://github.com/plone/cookiecutter-zope-instance/issues/15)
the value of the environment variable is not added or updated but replaced!
:::

**`environment_paths`** -- Since all relative paths are turned into absolute ones, we need to tell the cookiecutter which environment variables are paths. When customizing, always include `CHAMELEON_CACHE`.

## DOS Protection

| Setting | Default |
|---|---|
| `dos_protection_available` | `true` |
| `dos_protection_form_memory_limit` | `1MB` |
| `dos_protection_form_disk_limit` | `1GB` |
| `dos_protection_form_memfile_limit` | `4KB` |

**`dos_protection_available`** -- In Zope 5.8.4 and later, DOS protection is available. For older versions of Zope set this to `false`. Allowed values: `true`, `false`.

**`dos_protection_form_memory_limit`** -- The maximum size for each part in a multipart post request, for the complete body in an urlencoded post request and for the complete request body when accessed as bytes (rather than a file).

**`dos_protection_form_disk_limit`** -- The maximum size of a POST request body.

**`dos_protection_form_memfile_limit`** -- The value of form variables of type file with larger size are stored on disk rather than in memory.

## XML-RPC and WebDAV

| Setting | Default | Allowed Values |
|---|---|---|
| `enable_xmlrpc` | `true` | `true`, `false` |
| `enable_ms_public_header` | `false` | `true`, `false` |
| `webdav_source_port` | `0` | integer |

**`enable_xmlrpc`** -- Turn Zope's built-in XML-RPC support on or off. Available starting with Zope 5.13. Zope has built-in support for XML-RPC requests. It will attempt to use XML-RPC for POST requests with Content-Type header `text/xml`. Due to the limited use of XML-RPC nowadays and its potential for abuse by malicious actors you can set this to `false` to turn off support. Incoming XML-RPC requests will be refused with a BadRequest (HTTP status 400) response.

**`enable_ms_public_header`** -- Set to `true` to enable sending the `Public` header in response to a WebDAV OPTIONS request -- but only those coming from Microsoft WebDAV clients.

**`webdav_source_port`** -- This value designates a network port number as WebDAV source port. If set to a positive integer, any GET request coming into Zope via the designated port will be marked up to signal that this is a WebDAV request. Please note that Zope itself has no server capabilities and cannot open network ports. You need to configure your WSGI server to listen on the designated port.

## Locale

| Setting | Default |
|---|---|
| `locale` | *(unset)* |

**`locale`** -- Enable locale (internationalization) support by setting this to a locale string such as `de_DE.UTF-8`. When set, Zope will set the `locale` directive in `zope.conf`, which configures the locale used by the Python `locale` module. Leave empty to use the system default.

## HTTP Realm

| Setting | Default |
|---|---|
| `http_realm` | `Zope` |

**`http_realm`** -- The HTTP `Realm` header value sent by this Zope instance. This value often shows up in basic authentication dialogs.
