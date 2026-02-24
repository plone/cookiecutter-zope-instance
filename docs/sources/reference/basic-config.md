# Basic Configuration

<!-- diataxis: reference -->

Core WSGI server, environment, and request-handling settings.

## WSGI Server

`location_log`
: Base directory for all log files.

  **Default:** `{{ cookiecutter.location_clienthome }}/log`

`wsgi_listen`
: IP address or hostname with port the HTTP server binds to.

  **Default:** `localhost:8080`

`wsgi_fast_listen`
: Like `wsgi_listen`, but uses [waitress_fastlisten](https://pypi.org/project/waitress-fastlisten/).
  Needs the latter package to be installed (add it to *requirements.txt*).

  **Default:** empty string (switched off)

`wsgi_threads`
: Specify the number of worker threads used to service requests.

  **Default:** `4` (the waitress default)

`wsgi_max_request_body_size`
: Specify the maximum request body size in bytes.

  **Default:** `1073741824` (the waitress default)

`wsgi_clear_untrusted_proxy_headers`
: Tells Waitress (WSGI server) to remove any untrusted proxy headers
  (`Forwarded`, `X-Forwarded-For`, `X-Forwarded-By`, `X-Forwarded-Host`,
  `X-Forwarded-Port`, `X-Forwarded-Proto`) not explicitly allowed by
  `trusted_proxy_headers`.

  Allowed values: `true`, `false`

  **Default:** `false`

`wsgi_app_entrypoint`
: Configurable WSGI application entrypoint.

  **Default:** `egg:Zope#main`

## Environment

`environment`
: The environment set in `zope.conf`.

  Values: a dictionary with key/value pairs.

  **Default:**

  ```json
  {
      "zope_i18n_compile_mo_files": "true",
      "CHAMELEON_CACHE": "{{ cookiecutter.location_clienthome }}/cache"
  }
  ```

  :::{attention}
  Due to a [bug in cookiecutter 2.2.0 to 2.5.0](https://github.com/plone/cookiecutter-zope-instance/issues/15)
  the value of the environment variable is not added or updated but replaced!
  :::

`environment_paths`
: Since all relative paths are turned into absolute ones, we need to tell the
  cookiecutter which environment variables are paths. When customizing, always
  include `CHAMELEON_CACHE`.

  **Default:** `["CHAMELEON_CACHE"]`

## DOS Protection

`dos_protection_available`
: In Zope 5.8.4 and later, DOS protection is available.
  For older versions of Zope set this to `false`.

  Allowed values: `true`, `false`

  **Default:** `true`

`dos_protection_form_memory_limit`
: The maximum size for each part in a multipart post request, for the complete
  body in an urlencoded post request and for the complete request body when
  accessed as bytes (rather than a file).

  **Default:** `1MB`

`dos_protection_form_disk_limit`
: The maximum size of a POST request body.

  **Default:** `1GB`

`dos_protection_form_memfile_limit`
: The value of form variables of type file with larger size are stored on disk
  rather than in memory.

  **Default:** `4KB`

## XML-RPC and WebDAV

`enable_xmlrpc`
: Turn Zope's built-in XML-RPC support on or off.
  Available starting with Zope 5.13.

  Zope has built-in support for XML-RPC requests. It will attempt to use
  XML-RPC for POST requests with Content-Type header `text/xml`. By default
  the XML-RPC request support is enabled.

  Due to the limited use of XML-RPC nowadays and its potential for abuse by
  malicious actors you can set this to `false` to turn off support for XML-RPC.
  Incoming XML-RPC requests will be refused with a BadRequest (HTTP status 400)
  response.

  Allowed values: `true`, `false`

  **Default:** `true`

`enable_ms_public_header`
: Set this directive to `true` to enable sending the `Public` header in response
  to a WebDAV OPTIONS request -- but only those coming from Microsoft WebDAV
  clients.

  Though recent WebDAV drafts mention this header, the original WebDAV RFC did
  not mention it as part of the standard. Very few web servers include this
  header in their replies, most notably IIS and Netscape Enterprise 3.6.

  **Default:** `false`

`webdav_source_port`
: This value designates a network port number as WebDAV source port.

  WebDAV requires special handling for GET requests. A WebDAV client expects to
  receive the un-rendered source in the returned response body, not the rendered
  result a web browser would get.

  If this value is set to a positive integer, any GET request coming into Zope
  via the designated port will be marked up to signal that this is a WebDAV
  request. This request markup resembles what ZServer did for requests coming
  through its designated WebDAV source server port, so it is backwards-compatible
  for existing code that offers WebDAV handling under ZServer.

  Please note that Zope itself has no server capabilities and cannot open
  network ports. You need to configure your WSGI server to listen on the
  designated port.

  **Default:** `0`

## HTTP Realm

`http_realm`
: The HTTP `Realm` header value sent by this Zope instance.
  This value often shows up in basic authentication dialogs.

  **Default:** `Zope`
