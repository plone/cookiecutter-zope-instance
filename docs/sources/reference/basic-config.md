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
| `wsgi_channel_timeout` | *(unset, default `120`)* | integer (seconds) |
| `wsgi_app_entrypoint` | `egg:Zope#main` | entrypoint |
| `trusted_proxy` | *(unset)* | comma-separated IPs/hostnames |

**`wsgi_fast_listen`** -- Like `wsgi_listen`, but uses [waitress_fastlisten](https://pypi.org/project/waitress-fastlisten/). Needs the latter package to be installed (add it to *requirements.txt*).

**`wsgi_clear_untrusted_proxy_headers`** -- Tells Waitress (WSGI server) to remove any untrusted proxy headers (`Forwarded`, `X-Forwarded-For`, `X-Forwarded-By`, `X-Forwarded-Host`, `X-Forwarded-Port`, `X-Forwarded-Proto`) not explicitly allowed by `trusted_proxy_headers`.

**`wsgi_channel_timeout`** -- Maximum time in seconds to receive a complete request from a client. If the client does not send a complete request within this time, the connection is closed. Default is 120 seconds.

**`trusted_proxy`** -- A comma-separated list of IP addresses or hostnames of trusted reverse proxies. When set, Zope will trust proxy-related headers (such as `X-Forwarded-For`) from these sources. Each value becomes a separate `trusted-proxy` directive in `zope.conf`. Example: `"10.0.0.1,10.0.0.2"`.

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
| `dos_protection_form_part_limit` | `1024` |

**`dos_protection_available`** -- In Zope 5.8.4 and later, DOS protection is available. For older versions of Zope set this to `false`. Allowed values: `true`, `false`.

**`dos_protection_form_memory_limit`** -- The maximum size for each part in a multipart post request, for the complete body in an urlencoded post request and for the complete request body when accessed as bytes (rather than a file).

**`dos_protection_form_disk_limit`** -- The maximum size of a POST request body.

**`dos_protection_form_memfile_limit`** -- The value of form variables of type file with larger size are stored on disk rather than in memory.

**`dos_protection_form_part_limit`** -- The maximum number of parts (fields + files) in a multipart POST request. Available starting with Zope 5.10.

## Product Configuration

| Setting | Default |
|---|---|
| `product_config` | `{}` (empty dict) |

**`product_config`** -- A dictionary of dictionaries for Zope `<product-config>` sections. Each top-level key becomes a section name, and its value (a dict) provides the key/value pairs within that section. This is used by Zope add-ons to read configuration. Example:

```json
{
    "product_config": {
        "my_addon": {
            "setting1": "value1",
            "setting2": "value2"
        }
    }
}
```

This generates:

```text
<product-config my_addon>
    setting1 value1
    setting2 value2
</product-config>
```

## XML-RPC and WebDAV

| Setting | Default | Allowed Values |
|---|---|---|
| `enable_xmlrpc` | `true` | `true`, `false` |
| `enable_ms_public_header` | `false` | `true`, `false` |
| `webdav_source_port` | `0` | integer |

**`enable_xmlrpc`** -- Turn Zope's built-in XML-RPC support on or off. Available starting with Zope 5.13. Zope has built-in support for XML-RPC requests. It will attempt to use XML-RPC for POST requests with Content-Type header `text/xml`. Due to the limited use of XML-RPC nowadays and its potential for abuse by malicious actors you can set this to `false` to turn off support. Incoming XML-RPC requests will be refused with a BadRequest (HTTP status 400) response.

**`enable_ms_public_header`** -- Set to `true` to enable sending the `Public` header in response to a WebDAV OPTIONS request -- but only those coming from Microsoft WebDAV clients.

**`webdav_source_port`** -- This value designates a network port number as WebDAV source port. If set to a positive integer, any GET request coming into Zope via the designated port will be marked up to signal that this is a WebDAV request. Please note that Zope itself has no server capabilities and cannot open network ports. You need to configure your WSGI server to listen on the designated port.

## Locale & Formatting

| Setting | Default | Allowed Values |
|---|---|---|
| `locale` | *(unset)* | locale string |
| `datetime_format` | *(unset, default `us`)* | `us`, `international` |

**`locale`** -- Enable locale (internationalization) support by setting this to a locale string such as `de_DE.UTF-8`. When set, Zope will set the `locale` directive in `zope.conf`, which configures the locale used by the Python `locale` module. Leave empty to use the system default.

**`datetime_format`** -- Controls how Zope formats date/time values. Set to `international` for ISO-style dates (YYYY-MM-DD). When unset, Zope uses the US format (MM/DD/YYYY).

## HTTP Realm

| Setting | Default |
|---|---|
| `http_realm` | `Zope` |

**`http_realm`** -- The HTTP `Realm` header value sent by this Zope instance. This value often shows up in basic authentication dialogs.
