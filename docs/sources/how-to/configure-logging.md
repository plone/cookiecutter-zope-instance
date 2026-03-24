# Configure logging

<!-- diataxis: how-to -->

How to configure logging for different deployment scenarios.

## Cloud-native deployment (Docker / Kubernetes)

For containers, log to stdout in JSON format.
The 12-factor app methodology recommends treating logs as event streams — write to stdout and let the execution environment handle routing.

```{code-block} yaml
:caption: instance.yaml

default_context:
    log_format: json
    log_stdout: true
    log_stdout_stream: stdout
    log_file: false
    access_log_enabled: false
    log_level: WARNING
    logging_loggers:
        plone: INFO
```

```{important}
JSON format requires the [python-json-logger](https://pypi.org/project/python-json-logger/) package.
Add it to your `requirements.txt` or `constraints.txt`:

    pip install python-json-logger
```

Set `access_log_enabled: false` when your ingress controller or reverse proxy already handles access logging.

## Traditional deployment with file logging

For non-containerized servers, log to files:

```{code-block} yaml
:caption: instance.yaml

default_context:
    log_stdout: false
    log_file: true
    log_file_path: /var/log/plone/instance.log
    logging_loggers:
        plone: INFO
        waitress: WARNING
```

The access log is automatically created alongside the event log (`instance-access.log`).

## Hybrid: stdout and remote syslog

Combine local stdout with centralized log collection via syslog:

```{code-block} yaml
:caption: instance.yaml

default_context:
    log_stdout: true
    log_syslog: true
    log_syslog_host: logserver.internal
    log_syslog_protocol: tcp
    logging_loggers:
        plone: DEBUG
```

```{tip}
Use TCP (`log_syslog_protocol: tcp`) in production to avoid silent message loss with UDP.
```

## Debug a specific package

Increase the log level for specific packages without changing the global level:

```{code-block} yaml
:caption: instance.yaml

default_context:
    log_level: WARNING
    logging_loggers:
        plone: DEBUG
        plone.restapi: DEBUG
        waitress: WARNING
```

## Use a custom formatter

Point to any Python formatter class:

```{code-block} yaml
:caption: instance.yaml

default_context:
    log_format_class: mypackage.logging.MyFormatter
    log_format_string: "%(message)s"
```

The custom class must be importable in the Zope instance's Python environment.

## Migrate from `location_log`

```{deprecated} 2.5
The `location_log` setting is deprecated.
Use `log_file_path` instead for explicit control over the log file location.
```

If you currently rely on `location_log`, add `log_file: true` and `log_file_path` to your configuration:

```{code-block} yaml
:caption: instance.yaml — before (deprecated)

default_context:
    location_log: /var/log/plone

```

```{code-block} yaml
:caption: instance.yaml — after

default_context:
    log_file: true
    log_file_path: /var/log/plone/instance.log
```
