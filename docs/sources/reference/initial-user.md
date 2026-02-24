# Initial User

<!-- diataxis: reference -->

Settings for the initial Zope administrator account.

| Setting | Default |
|---|---|
| `initial_user_name` | `admin` |
| `initial_user_password` | *(empty, generated)* |

**`initial_user_name`** -- Creates an initial user with the given name and "Manager" role (full web access).

**`initial_user_password`** -- Creates an initial password for the initial user. If empty, a password will be generated and printed after the cookiecutter generation process run.
