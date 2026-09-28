# Position

## List

### Request

- **Method:** GET
- **Url:** /personnel/api/positions/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Query Parameters**

| Parameter | Description |
| --- | --- |
| page | Which page is displayed |
| page_size | Show the number of data on this page |
| position_code | Use this field to query |
| position_name | Use this field to query |
| position_code_icontains | Query the data that this field contains |
| position_name_icontains | Query the data that this field contains |
| ordering | id, position_code, position_name |

### Response

```json
{
    "count": 27,
    "next": "null",
    "previous": null,
    "msg": "",
    "code": 0,
    "data": [
        {
            "id": 1,
            "position_code": "1",
            "position_name": "WORLD",
            "parent_position": null
        },
        {
            "id": 93,
            "position_code": "5190062",
            "position_name": "shenzhen",
            "parent_position": null
        },
        ...
        ...
}
```

## Read

### Request

- **Method:** GET
- **Url:** /personnel/api/positions/{id}/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Path Parameters**

| Parameter | Description |
| --- | --- |
| id | required |

### Response

```text
- **Url:** /personnel/api/positions/1/
{
    "id": 1,
    "position_code": "1",
    "position_name": "WORLD",
    "parent_position": null
}
```

## Create

- **Method:** POST
- **Url:** /personnel/api/positions/
- **Headers:**
  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "position_code": "test position code",
    "position_name": "test position name",
    "parent_position": null
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| position_code | Y | String | Position Code |
| position_name | Y | String | Position Name |
| parent_position | N | Integer | Parent Position |

### Response

```json
{
    "id": 100,
    "position_code": "test position code",
    "position_name": "test position name",
    "parent_position": null
}
```

## Update

### Request

- **Method:** PUT
- **Url:** /personnel/api/positions/{id}/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Path Parameters**

| Parameter | Description |
| --- | --- |
| id | required |

- **Request Body**

```json
{
    "position_code": "11",
    "position_name": "test position name",
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| position_code | Y | String | Position Code |
| position_name | Y | String | Position Name |
| parent_position | N | Integer | Parent Position |

### Response

```text
- **Url:** PUT /personnel/api/positions/1/
{
    "id": 1,
    "position_code": "11",
    "position_name": "WORLD WORLD",
    "parent_position": null
}
```

## Delete

### Request

- **Method:** DELETE
- **Url:** /personnel/api/positions/{id}/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Path Parameters**

| Parameter | Description |
| --- | --- |
| id | required |

### Response

```text
None
```
