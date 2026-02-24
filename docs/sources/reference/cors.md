# CORS

<!-- diataxis: reference -->

Plone offers [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
handling with the [plone.rest](https://pypi.org/project/plone.rest/) package.
CORS configuration is needed if you want to access the Plone REST API from a
different domain than the one Plone is running on.

`cors_enabled`
: Enable CORS support.

  Allowed values: `true`, `false`

  **Default:** `false`

`cors_allow_credentials`
: Indicates whether the resource supports user credentials in the request.

  Allowed values: `true`, `false`

  **Default:** `true`

`cors_allow_headers`
: A comma separated list of request headers allowed to be sent by the client.

  **Default:** `Accept,Authorization,Content-Type,Lock-Token`

`cors_allow_methods`
: A comma separated list of HTTP method names that are allowed by this CORS
  policy.

  **Default:** `DELETE,GET,OPTIONS,PATCH,POST,PUT`

`cors_allow_origin`
: Origins that are allowed access to the resource. Either a comma separated
  list of origins, e.g. `https://example.com,https://otherexample.com`, or
  `*` for all.

  **Default:** `http://localhost:3000,http://127.0.0.1:3000`

`cors_expose_headers`
: A comma separated list of response headers clients can access.

  **Default:** `Content-Length`

`cors_max_age`
: Indicates how long the results of a preflight request can be cached in
  seconds.

  **Default:** `3600`
