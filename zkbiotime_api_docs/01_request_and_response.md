# Request & Response

## Request

- **url**

```text
http://{host}:{port}
```

- **public header**

> The public header parameter is a parameter used for interface authentication and user identification, For example, non-special interfaces (such as obtaining tokens) need to be added on each interface, and public parameters need to be uniformly placed in the HTTP Header request section.

| Parameter name | Required | Type | Description |
| --- | --- | --- | --- |
| Authorization | Y | String | authToken |
| Content Type | Y | String | default: application/json |
| Accept | N | String | default: application/json |

- **query parameter**

| Parameter name | Required | Type | Description |
| --- | --- | --- | --- |
| page | N | Integer | page number |
| page_size | N | Integer | each page count |

## Response

- **status code**
- status code < 400: request success
- 400 < status code < 500: client request error, check error message please.
- 500 < status code: biotime server error
