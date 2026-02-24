# Base Locations

<!-- diataxis: reference -->

These settings control the base directory structure of the generated Zope instance.

| Setting | Default |
|---|---|
| `target` | `instance` |
| `location_clienthome` | `{{ cookiecutter.target }}/var` |

**`target`** -- The target directory name of the cookiecutter generated configuration. This is also the so called *INSTANCEHOME*. Attention: this is relative to the current directory or to cookiecutter command line options if given (`-o PATH` or `--output-dir PATH`).

**`location_clienthome`** -- Zope's **clienthome** directory is where by default all writable files are written, such as the database with blobs, logs, PID file, etc. This is the only place where the user of the WSGI process needs write access. Traditionally this is the **var** directory of the *instancehome*.
