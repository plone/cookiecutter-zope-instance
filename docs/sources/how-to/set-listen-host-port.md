# Set the listen host and port

<!-- diataxis: how-to -->

This guide shows you how to set the host and TCP port your instance listens
on for HTTP requests.

## Prerequisites

- New to this template? Start with {doc}`/tutorials/first-zope-instance`.

## Step 1: set the listen address

In your `instance.yaml`, set `wsgi_listen` to a `host:port` value:

```yaml
default_context:
    wsgi_listen: localhost:8080
```

The default is `localhost:8080`, which accepts connections only from the
local machine.

To accept connections from any network interface, bind to `0.0.0.0`:

```yaml
default_context:
    wsgi_listen: 0.0.0.0:8080
```

```{important}
When the instance runs behind a reverse proxy, bind to `127.0.0.1` so that
only the proxy can reach it directly:

    wsgi_listen: 127.0.0.1:8080
```

## Step 2: enable a fast listen socket (optional)

`wsgi_fast_listen` configures a second socket served by
[waitress-fastlisten](https://pypi.org/project/waitress-fastlisten/).
Install that package, then set the address:

```yaml
default_context:
    wsgi_listen: 127.0.0.1:8080
    wsgi_fast_listen: 127.0.0.1:8081
```

Leave `wsgi_fast_listen` empty to disable the fast socket.

## Verify

After generating the instance, start it and confirm the bound address in the
startup log:

```shell
runwsgi instance/etc/zope.ini
```

The log reports the host and port Waitress serves on.

## Next steps

- {doc}`/reference/basic-config` -- Full reference for `wsgi_listen`,
  `wsgi_fast_listen`, trusted proxies, and other WSGI server settings.
- {doc}`/reference/sample-configurations` -- Complete, copy-paste
  configurations for every backend.
