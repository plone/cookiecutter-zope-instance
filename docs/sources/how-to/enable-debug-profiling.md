# Enable debug mode and profiling

<!-- diataxis: how-to -->

This guide shows you how to turn on debug mode and request profiling for
local development.

```{warning}
These settings are for development only.
Never enable debug mode, exception propagation, or profiling in production.
```

## Prerequisites

- New to this template? Start with {doc}`/tutorials/first-zope-instance`.

## Step 1: enable debug mode

Turn on debug mode and verbose security in your `instance.yaml`:

```yaml
default_context:
    debug_mode: true
    verbose_security: true
```

To let exceptions propagate into the WSGI pipeline so debugging middleware
can handle them, also set `debug_exceptions`:

```yaml
default_context:
    debug_mode: true
    verbose_security: true
    debug_exceptions: true
```

## Step 2: enable profiling

Profiling uses [repoze.profile](https://repozeprofile.readthedocs.io/).
Install it first:

```shell
pip install repoze.profile
```

Then enable it and choose the through-the-web path for inspecting the last
profiled request:

```yaml
default_context:
    profile_repoze: true
    profile_repoze_path: /__profile__
```

## Step 3: inspect the results

Start the instance, make a few requests, then open the profile path in your
browser to see the most recent profiled request:

```text
http://localhost:8080/__profile__
```

The raw profile data is also written to `profile_repoze_log_filename` for
offline analysis.

## Next steps

- {doc}`/reference/development` -- Full reference for debug, verbose security,
  and `repoze.profile` settings.
