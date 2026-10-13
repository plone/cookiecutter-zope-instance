# Run behind a reverse proxy

<!-- diataxis: how-to -->

This guide shows you how to run an instance behind a reverse proxy such as
nginx or Apache, so the proxy terminates TLS and forwards requests to Zope.

## Prerequisites

- New to this template? Start with {doc}`/tutorials/first-zope-instance`.
- A reverse proxy (nginx, Apache, or similar) in front of the instance.

## Step 1: bind to localhost

Set `wsgi_listen` to `127.0.0.1` so only the proxy on the same host can reach
the instance directly:

```yaml
default_context:
    wsgi_listen: 127.0.0.1:8080
```

## Step 2: declare the trusted proxy

List the proxy's address in `trusted_proxy` so Zope honors the forwarded
headers it sends:

```yaml
default_context:
    wsgi_listen: 127.0.0.1:8080
    trusted_proxy: "127.0.0.1"
```

`trusted_proxy` accepts a comma-separated list of IP addresses or hostnames.

## Step 3: clear untrusted proxy headers

Tell Waitress to strip forwarded headers that do not come from a trusted
proxy, so clients cannot spoof them:

```yaml
default_context:
    wsgi_listen: 127.0.0.1:8080
    trusted_proxy: "127.0.0.1"
    wsgi_clear_untrusted_proxy_headers: true
```

## Step 4: configure the proxy

Forward requests to the instance and pass the original host and scheme.
Use Zope virtual host rewriting so generated URLs match the public address.
A representative nginx location block:

```nginx
location / {
    proxy_pass http://127.0.0.1:8080/VirtualHostBase/https/$host:443/Plone/VirtualHostRoot/;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Replace `Plone` with the id of your Zope object (for example, the Plone site)
and adjust the scheme and port to match your deployment.

## Next steps

- {doc}`/reference/basic-config` -- Reference for `wsgi_listen`,
  `trusted_proxy`, and `wsgi_clear_untrusted_proxy_headers`.
- {doc}`configure-cors` -- Configure CORS when the API is served cross-origin.
