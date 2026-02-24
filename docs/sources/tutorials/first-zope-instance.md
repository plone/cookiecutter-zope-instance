# Your First Zope Instance

<!-- diataxis: tutorial -->

## What you will build

In this tutorial you will generate a fully working Zope WSGI instance
with sensible default settings, ready to start and serve requests.

## Prerequisites

- **Python 3.10+** installed on your system
- **cookiecutter** (installed in a later step)
- A basic understanding of the command line

## Step 1: Install cookiecutter

Install `cookiecutter` into your Python environment:

```bash
pip install cookiecutter
```

Verify the installation:

```bash
cookiecutter --version
```

## Step 2: Create a configuration file

Cookiecutter reads its input from a YAML configuration file. Create a file
called `instance.yaml` with the following content:

```yaml
default_context:
    initial_user_name: 'admin'
    initial_user_password: 'admin'
    zcml_package_includes: my.awesome.addon
    db_storage: direct
```

This tells cookiecutter to:

- create an initial admin user with username `admin` and password `admin`,
- include the ZCML of the package `my.awesome.addon`, and
- use a direct (FileStorage) ZODB database.

## Step 3: Run cookiecutter

Generate the instance by pointing cookiecutter at the upstream template:

```bash
cookiecutter -f --no-input --config-file instance.yaml \
    gh:plone/cookiecutter-zope-instance
```

The flags used here:

- `-f` overwrites an existing `instance` directory if present.
- `--no-input` skips the interactive prompts — all values come from the YAML file.
- `--config-file instance.yaml` provides the configuration.

Cookiecutter will clone the template and render the output into a directory
called `instance/`.

## Step 4: Explore the generated files

After the command finishes you will find the following structure:

```text
instance/
├── etc/
│   ├── zope.conf      # Main Zope configuration
│   ├── zope.ini        # PasteDeploy WSGI pipeline
│   └── site.zcml       # ZCML root with your package includes
└── inituser            # Bootstrap admin credentials
```

| File | Purpose |
|---|---|
| `etc/zope.conf` | Database connection, debug mode, security settings |
| `etc/zope.ini` | WSGI server (waitress) host, port, pipeline |
| `etc/site.zcml` | Component architecture — which packages are loaded |
| `inituser` | One-time admin user created on first startup |

## Step 5: Start the instance

To start the instance you need a WSGI server such as **waitress** and the
Zope application itself installed in your Python environment. Then run:

```bash
runwsgi instance/etc/zope.ini
```

The server will listen on the address configured in `zope.ini`
(by default `0.0.0.0:8080`).

## What you learned

- Cookiecutter generates a complete Zope instance directory from a small YAML
  configuration file.
- The `default_context` section in the YAML maps directly to the template
  variables described in the {doc}`../reference/index`.
- Changing values in the YAML and re-running cookiecutter with `-f` lets you
  iterate quickly on the configuration.

Next, learn how to adapt this workflow for {doc}`docker-deployment`.
