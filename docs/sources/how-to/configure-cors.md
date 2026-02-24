# Configure CORS for REST API Access

<!-- diataxis: how-to -->

This guide shows how to configure Cross-Origin Resource Sharing (CORS) so
that browser-based frontend applications can access the Plone REST API from a
different origin.

CORS support is provided by
[plone.rest](https://pypi.org/project/plone.rest/) and is configured through
`cookiecutter-zope-instance` settings.

## Step 1: Enable CORS

By default, CORS is disabled. Enable it in your `instance.yaml`:

```yaml
default_context:
    cors_enabled: true
```

## Step 2: Configure allowed origins

Specify which origins may access your Plone site:

```yaml
default_context:
    cors_enabled: true
    cors_allow_origin: "https://frontend.example.com"
```

For multiple origins, use a comma-separated list:

```yaml
default_context:
    cors_allow_origin: "https://frontend.example.com,https://admin.example.com"
```

Use `*` to allow all origins (not recommended for production):

```yaml
default_context:
    cors_allow_origin: "*"
```

## Example: Volto development setup

When developing with [Volto](https://github.com/plone/volto) (the default
Plone 6 frontend), the React dev server typically runs on
`http://localhost:3000`. The default CORS origin settings already cover this:

```yaml
default_context:
    initial_user_name: admin
    initial_user_password: admin

    zcml_package_includes: my.site.addon
    db_storage: direct

    # CORS for Volto dev server
    cors_enabled: true
    cors_allow_origin: "http://localhost:3000,http://127.0.0.1:3000"
    cors_allow_credentials: true
    cors_allow_headers: "Accept,Authorization,Content-Type"
    cors_allow_methods: "DELETE,GET,OPTIONS,PATCH,POST,PUT"
```

```{tip}
The default value for `cors_allow_origin` is already
`http://localhost:3000,http://127.0.0.1:3000`, so for local Volto development
you only need to set `cors_enabled: true`.
```

## Example: Production with specific domains

```yaml
default_context:
    cors_enabled: true
    cors_allow_origin: "https://www.example.com,https://cms.example.com"
    cors_allow_credentials: true
    cors_allow_headers: "Accept,Authorization,Content-Type"
    cors_allow_methods: "DELETE,GET,OPTIONS,PATCH,POST,PUT"
    cors_expose_headers: "Content-Length"
    cors_max_age: 3600
```

## Next steps

- {doc}`/reference/cors` -- Full reference for all CORS configuration options.
