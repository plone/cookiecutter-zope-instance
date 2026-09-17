# Use an alternative WSGI server

<!-- diataxis: how-to -->

By default the generated `zope.ini` runs Zope with [waitress](https://pypi.org/project/waitress/).
Any other [PasteDeploy](https://docs.pylonsproject.org/projects/pastedeploy/) capable server can be
configured with `wsgi_server_use` and `wsgi_server_options`.

## Example: pyruvate

[pyruvate](https://pypi.org/project/pyruvate/) is a WSGI server implemented in Rust.
Install it alongside your Zope/Plone packages, then configure:

```yaml
default_context:
  wsgi_server_use: "egg:pyruvate#main"
  wsgi_server_options:
    socket: "localhost:8080"
    workers: 2
  logging_loggers:
    pyruvate: INFO
```

This renders the `[server:main]` section as:

```ini
[server:main]
use = egg:pyruvate#main
socket = localhost:8080
workers = 2
```

The `logging_loggers` entry adds a `[logger_pyruvate]` section, so pyruvate's log output
reaches the configured root handlers.

## Notes

- With `wsgi_server_use` set, the waitress-specific options (`wsgi_listen`, `wsgi_threads`,
  `wsgi_max_request_body_size`, `wsgi_channel_timeout`, `wsgi_clear_untrusted_proxy_headers`)
  are ignored; a warning is printed if any of them is set.
- `wsgi_server_use` cannot be combined with `wsgi_fast_listen`.
- The WSGI pipeline (`wsgi_filters`, access log, profiling) is independent of the server
  and keeps working unchanged.
