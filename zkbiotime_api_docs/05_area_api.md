# Area

## List

### Request

- **Method:** GET
- **Url:** /personnel/api/areas/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Query Parameters**

| Parameter | Description |
| --- | --- |
| page | Which page is displayed |
| page_size | Show the number of data on this page |
| area_code | Use this field to query |
| area_name | Use this field to query |
| area_code_icontains | Query the data that this field contains |
| area_name_icontains | Query the data that this field contains |
| ordering | id, area_code, area_name |

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
            "area_code": "1",
            "area_name": "WORLD",
            "parent_area": null
        },
        {
            "id": 93,
            "area_code": "5190062",
            "area_name": "shenzhen",
            "parent_area": null
        },
        ...
        ...
}
```

## Read

### Request

- **Method:** GET
- **Url:** /personnel/api/areas/{id}/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Path Parameters**

| Parameter | Description |
| --- | --- |
| id | required |

### Response

```text
- **Url:** /personnel/api/areas/1/
{
    "id": 1,
    "area_code": "1",
    "area_name": "WORLD",
    "parent_area": null
}
```

## Create

- **Method:** POST
- **Url:** /personnel/api/areas/
- **Headers:**
  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "area_code": "test area code",
    "area_name": "test area name",
    "parent_area": null
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| area_code | Y | String | Area Code |
| area_name | Y | String | Area Name |
| parent_area | N | Integer | Parent Area |

### Response

```json
{
    "id": 100,
    "area_code": "test area code",
    "area_name": "test area name",
    "parent_area": null
}
```

## Update

### Request

- **Method:** PUT
- **Url:** /personnel/api/areas/{id}/
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
    "area_code": "11",
    "area_name": "test area name",
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| area_code | Y | String | Area Code |
| area_name | Y | String | Area Name |
| parent_area | N | Integer | Parent Area |

### Response

```text
- **Url:** PUT /personnel/api/areas/1/
{
    "id": 1,
    "area_code": "11",
    "area_name": "WORLD WORLD",
    "parent_area": null
}
```

## Delete

### Request

- **Method:** DELETE
- **Url:** /personnel/api/areas/{id}/
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
