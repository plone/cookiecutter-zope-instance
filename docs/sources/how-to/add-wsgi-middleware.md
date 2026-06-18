# Add WSGI middleware to the pipeline

<!-- diataxis: how-to -->

This guide shows you how to inject WSGI/PasteDeploy filters into the generated
`zope.ini` pipeline -- for example the request-metrics and OpenTelemetry
middleware from [plone.observability](https://github.com/plone/plone.observability).

## Prerequisites

- New to this template? Start with {doc}`/tutorials/first-zope-instance`.
- The middleware package must be installed and expose a
  `paste.filter_app_factory` entry point.

## Step 1: define the filters

Set `wsgi_filters` in your `instance.yaml` to a dictionary. Each key is the
filter name; its value configures that filter:

```yaml
default_context:
    wsgi_filters:
        observability:
            use: "egg:plone.observability#observability"
        opentelemetry:
            use: "egg:plone.observability#opentelemetry"
```

Each entry's value supports these fields:

- `use` (required) -- the PasteDeploy entry point of the filter.
- `options` (optional) -- a mapping of additional `key: value` lines rendered
  verbatim into the `[filter:<name>]` section.
- `position` (optional) -- `outer` (the default) places the filter ahead of the
  built-in `profile`/`translogger` filters, so it wraps the whole request;
  `inner` places it closest to the application, just before
  `egg:Zope#httpexceptions`.

Reserved names that cannot be used: `zope`, `profile`, `translogger`,
`httpexceptions`, `main`.

## Step 2: check the generated output

This renders one `[filter:<name>]` section per entry, wired into
`[pipeline:main]`:

```ini
[pipeline:main]
pipeline =
    observability
    opentelemetry
    egg:Zope#httpexceptions
    zope

[filter:observability]
use = egg:plone.observability#observability

[filter:opentelemetry]
use = egg:plone.observability#opentelemetry
```

## Next steps

- {doc}`/reference/basic-config` -- Reference for `wsgi_filters` and the other
  core settings.
