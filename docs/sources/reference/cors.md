# CORS

<!-- diataxis: reference -->

Plone offers [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
handling with the [plone.rest](https://pypi.org/project/plone.rest/) package.
CORS configuration is needed if you want to access the Plone REST API from a
different domain than the one Plone is running on.

| Setting | Default | Allowed Values |
|---|---|---|
| `cors_enabled` | `false` | `true`, `false` |
| `cors_allow_credentials` | `true` | `true`, `false` |
| `cors_allow_headers` | `Accept,Authorization,Content-Type,Lock-Token` | comma-separated list |
| `cors_allow_methods` | `DELETE,GET,OPTIONS,PATCH,POST,PUT` | comma-separated list |
| `cors_allow_origin` | `http://localhost:3000,http://127.0.0.1:3000` | comma-separated origins or `*` |
| `cors_expose_headers` | `Content-Length` | comma-separated list |
| `cors_max_age` | `3600` | integer (seconds) |

**`cors_allow_origin`** -- Origins that are allowed access to the resource. Either a comma separated list of origins, e.g. `https://example.com,https://otherexample.com`, or `*` for all.
