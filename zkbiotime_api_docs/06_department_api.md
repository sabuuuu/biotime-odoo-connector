# Department

## List

### Request

- **Method:** GET
- **Url:** /personnel/api/departments/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Query Parameters**

| Parameter | Description |
| --- | --- |
| page | Which page is displayed |
| page_size | Show the number of data on this page |
| dept_code | Use this field to query |
| dept_name | Use this field to query |
| dept_code_icontains | Query the data that this field contains |
| dept_name_icontains | Query the data that this field contains |
| ordering | id, dept_code, dept_name |

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
            "dept_code": "1",
            "dept_name": "WORLD",
            "parent_dept": null
        },
        {
            "id": 93,
            "dept_code": "5190062",
            "dept_name": "shenzhen",
            "parent_dept": null
        },
        ...
        ...
}
```

## Read

### Request

- **Method:** GET
- **Url:** /personnel/api/departments/{id}/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Path Parameters**

| Parameter | Description |
| --- | --- |
| id | required |

### Response

```text
- **Url:** /personnel/api/departments/1/
{
    "id": 1,
    "dept_code": "1",
    "dept_name": "WORLD",
    "parent_dept": null
}
```

## Create

- **Method:** POST
- **Url:** /personnel/api/departments/
- **Headers:**
  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "dept_code": "test dept code",
    "dept_name": "test dept name",
    "parent_dept": null
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| dept_code | Y | String | Department Code |
| dept_name | Y | String | Department Name |
| parent_dept | N | Integer | Parent Department |

### Response

```json
{
    "id": 100,
    "dept_code": "test dept code",
    "dept_name": "test dept name",
    "parent_dept": null
}
```

## Update

### Request

- **Method:** PUT
- **Url:** /personnel/api/departments/{id}/
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
    "dept_code": "11",
    "dept_name": "test dept name",
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| dept_code | Y | String | Department Code |
| dept_name | Y | String | Department Name |
| parent_dept | N | Integer | Parent Department |

### Response

```text
- **Url:** PUT /personnel/api/departments/1/
{
    "id": 1,
    "dept_code": "11",
    "dept_name": "WORLD WORLD",
    "parent_dept": null
}
```

## Delete

### Request

- **Method:** DELETE
- **Url:** /personnel/api/departments/{id}/
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
