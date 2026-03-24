# Logging

<!-- diataxis: reference -->

Complete reference for logging configuration variables.

```{versionchanged} 2.5
Logging is now fully configurable. The default changed from file-based logging to stdout (12-factor pattern). If you relied on file logging, add `log_file: true` to your configuration.
```

## Format and level

| Setting | Default | Allowed values |
|---|---|---|
| `log_format` | `text` | `text`, `json` |
| `log_format_class` | *(unset)* | Python dotted name |
| `log_format_string` | *(unset)* | Python logging format string |
| `log_level` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

**`log_format`** — Output format for all handlers.
`text` uses the classic Zope format: `%(asctime)s %(levelname)-7.7s [%(name)s:%(lineno)s][%(threadName)s] %(message)s`.
`json` uses [python-json-logger](https://pypi.org/project/python-json-logger/) for structured JSON output (requires installation).

**`log_format_class`** — Custom Python formatter class (dotted name). When set, overrides `log_format`. The class must be importable at runtime.

**`log_format_string`** — Format string passed to the custom formatter class.

**`log_level`** — Root logger level. Individual loggers in `logging_loggers` can override this.

## stdout handler

| Setting | Default | Allowed values |
|---|---|---|
| `log_stdout` | `true` | `true`, `false` |
| `log_stdout_stream` | `stderr` | `stdout`, `stderr` |

**`log_stdout`** — Enable logging to stdout or stderr. Default is `true` (12-factor pattern).

**`log_stdout_stream`** — Which stream to use. Default is `stderr`. Container deployments often prefer `stdout`.

## File handler

| Setting | Default | Allowed values |
|---|---|---|
| `log_file` | `false` | `true`, `false` |
| `log_file_path` | *(unset)* | Absolute file path |

**`log_file`** — Enable file-based logging. Default is `false`.

**`log_file_path`** — Full path to the event log file. When unset, falls back to `<location_log>/instance.log`. The access log path is derived by inserting `-access` before the file extension (e.g. `instance.log` → `instance-access.log`).

## Syslog handler

| Setting | Default | Allowed values |
|---|---|---|
| `log_syslog` | `false` | `true`, `false` |
| `log_syslog_host` | `localhost` | hostname or IP |
| `log_syslog_port` | `514` | integer |
| `log_syslog_facility` | `1` | integer 0–23 |
| `log_syslog_protocol` | `udp` | `udp`, `tcp` |

**`log_syslog`** — Enable syslog remote logging via Python's `SysLogHandler`.

**`log_syslog_facility`** — Syslog facility as integer:

| Value | Name |
|---|---|
| 1 | LOG_USER (default) |
| 16 | LOG_LOCAL0 |
| 17 | LOG_LOCAL1 |
| 18 | LOG_LOCAL2 |
| 19 | LOG_LOCAL3 |
| 20 | LOG_LOCAL4 |
| 21 | LOG_LOCAL5 |
| 22 | LOG_LOCAL6 |
| 23 | LOG_LOCAL7 |

**`log_syslog_protocol`** — `udp` (default) or `tcp`. TCP is recommended for production to prevent silent message loss.

## Access log

| Setting | Default | Allowed values |
|---|---|---|
| `access_log_enabled` | `true` | `true`, `false` |

**`access_log_enabled`** — Enable WSGI access logging via the Paste `translogger` filter. When `false`, the `translogger` filter and the `wsgi` logger are removed entirely. Set to `false` when your ingress controller or reverse proxy handles access logging.

## Per-package log levels

| Setting | Default | Allowed values |
|---|---|---|
| `logging_loggers` | `{"plone": "INFO", "waitress.queue": "INFO", "waitress": "INFO"}` | dict of `name: level` |

**`logging_loggers`** — Dict mapping logger names to log levels. The template generates a `[logger_X]` section for each entry. Reserved keys `root` and `wsgi` are silently ignored (they are managed by the template).

Logger names with dots use underscore mapping for ini section names (e.g. `plone.restapi` → `[logger_plone_restapi]`) with `qualname` set to the original dotted name.
