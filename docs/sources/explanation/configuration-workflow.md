# The configuration workflow

<!-- diataxis: explanation -->

This page explains how a configuration travels from a small YAML file to a
running instance, and why the containerized workflow is shaped the way it is.

## From YAML to instance

The template is driven by a single `instance.yaml` file.
Its `default_context` section maps directly to the template variables, and
`cookiecutter` renders those variables into the concrete `zope.conf`,
`zope.ini`, and `site.zcml` files that Zope reads at startup.

This indirection is deliberate.
You describe *intent* in a compact, reviewable file, and the template expands
it into the verbose, interdependent configuration files that Zope expects.
Changing one value in the YAML and re-rendering is safer than hand-editing
several generated files and keeping them consistent.

## Why a transform layer

Baking configuration into a container image is convenient but wrong for
anything that varies between environments or must stay secret.
Database hostnames, credentials, and listen addresses differ between staging
and production, and secrets must never be committed to an image.

The `transform_from_environment.py` helper bridges this gap.
It reads the base `instance.yaml`, merges every `INSTANCE_*` environment
variable on top of it, and writes an effective configuration that
`cookiecutter` then renders.
The base file carries the stable defaults; the environment carries the
per-deployment and secret values.

## The naming conventions

Each environment variable named `INSTANCE_<key>` sets `<key>` in
`default_context`.
The prefix is stripped, and the remainder becomes the configuration key.
Setting a variable to an empty string clears that key, which is how a feature
is disabled in production -- for example, clearing a development password so
that a fresh one is generated.

Some template variables are dictionaries rather than scalars.
The `_DICT_` infix addresses a single entry inside such a dictionary, so
`INSTANCE_environment_DICT_TZ=Europe/Berlin` sets the `TZ` entry of the
`environment` dictionary without replacing the whole mapping.

## Why generate at container start

The transform and `cookiecutter` run in the container *entrypoint*, on every
start, not at image build time.
This is the crucial design choice for containerized deployments.

Build time is too early.
The `INSTANCE_*` variables that carry secrets and per-deployment values only
exist at runtime, injected by the orchestrator.
Rendering the configuration at startup is what lets one image serve every
environment.

## Why pin and vendor the template

The image downloads a pinned version of the template and the transform helper
at build time, then runs entirely from those local files at startup.

Pinning a specific version makes builds reproducible: the same image always
renders the same configuration.
Vendoring the template into the image means the entrypoint needs no network
access at startup, which removes a class of runtime failures and shrinks the
container's attack surface.

## See also

- {doc}`/how-to/use-environment-variables` -- The task-oriented procedure.
- {doc}`/tutorials/docker-deployment` -- The same workflow applied end-to-end.
- {doc}`/reference/helpers` -- Reference for the helper scripts.
