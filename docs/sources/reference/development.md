# Development

<!-- diataxis: reference -->

Settings for debug mode, verbose security, and profiling.

## Debug Settings

| Setting | Default | Allowed Values |
|---|---|---|
| `debug_mode` | `false` | `true`, `false` |
| `debug_exceptions` | `false` | `true`, `false` |
| `verbose_security` | `false` | `true`, `false` |

**`debug_exceptions`** -- This switch controls how exceptions are handled. If it is set to `false` (the default), Zope's own exception handling is active. Exception views or a `standard_error_message` are used to handle them. If set to `true`, exceptions are not handled by Zope and can propagate into the WSGI pipeline, where they may be handled by debugging middleware. This setting should always be `false` in production. It is useful for developers and while debugging site issues.

**`verbose_security`** -- Switches verbose security on (and switches to the Python security implementation).

## Profiling with repoze.profile

| Setting | Default | Allowed Values |
|---|---|---|
| `profile_repoze` | `false` | `true`, `false` |
| `profile_repoze_log_filename` | `{{ cookiecutter.location_log }}/repoze_profile.raw.log` | path |
| `profile_repoze_cachegrind_filename` | `{{ cookiecutter.location_log }}/repoze_cachegrind.out.bar` | path |
| `profile_repoze_discard_first_request` | `true` | `true`, `false` |
| `profile_repoze_path` | `/__profile__` | URL path |
| `profile_repoze_flush_at_shutdown` | `true` | `true`, `false` |
| `profile_repoze_unwind` | `false` | `true`, `false` |

**`profile_repoze`** -- Enable profiling with [repoze.profile](https://repozeprofile.readthedocs.io/). Ensure to execute `pip install repoze.profile` before switching this on.

**`profile_repoze_log_filename`** -- Filename of the raw profile data. This file contains the raw profile data for further analysis.

**`profile_repoze_cachegrind_filename`** -- If the package `pyprof2calltree` is installed, another file is written. It is meant for consumption with any cachegrind compatible application.

**`profile_repoze_path`** -- The path for through-the-web access to the last profiled request. See [repoze.profile docs](https://repozeprofile.readthedocs.io/en/latest/#configuration-via-python) for details.
