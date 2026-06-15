# How-to guides

<!-- diataxis: how-to -->

Goal-oriented guides for common tasks.

These guides follow the life of an instance, from first configuration through
production deployment to day-to-day operations.
Choose a storage backend such as {term}`FileStorage`, {term}`RelStorage`,
{term}`ZEO`, or {term}`PGJsonb`, then deploy and operate it.
New to the template? Start with the {doc}`/tutorials/index`.

## Set up the server

- {doc}`set-listen-host-port`

## Choose a storage backend

- {doc}`configure-filestorage`
- {doc}`configure-relstorage`
- {doc}`configure-pgjsonb`
- {doc}`configure-zeo`
- {doc}`configure-z3blobs`

## Configure the application

- {doc}`configure-cors`
- {doc}`configure-logging`
- {doc}`set-product-config`

## Deploy to production

- {doc}`run-behind-reverse-proxy`
- {doc}`use-environment-variables`

## Develop and debug

- {doc}`enable-debug-profiling`

## Operate

- {doc}`pack-and-gc`
- {doc}`backup-and-restore`
- {doc}`migrate-storage`

## Upgrade

- {doc}`upgrade-v1-to-v2`

```{toctree}
---
hidden: true
---
set-listen-host-port
configure-filestorage
configure-relstorage
configure-pgjsonb
configure-zeo
configure-z3blobs
configure-cors
configure-logging
set-product-config
run-behind-reverse-proxy
use-environment-variables
enable-debug-profiling
pack-and-gc
backup-and-restore
migrate-storage
upgrade-v1-to-v2
```
