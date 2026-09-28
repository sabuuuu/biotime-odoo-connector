# Resign

## List

### Request

- **Method:** GET
- **Url:** /personnel/api/resigns/
- **Headers:**
  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Query Parameters**

| Parameter | Description |
| --- | --- |
| page | Which page is displayed |
| page_size | Show the number of data on this page |
| employee | Use this field to query |
| resign_type | Use this field to query |
| resign_date | Use this field to query |

### Response

```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "msg": "",
    "code": 0,
    "data": [
        {
            "id": 5,
            "resign_date": "2020-06-04",
            "resign_type": 1,
            "disableatt": true,
            "employee": {
                "id": 3,
                "emp_code": "11111122",
                "first_name": "aaabb",
                "last_name": ""
            },
            "first_name": "aaabb",
            "last_name": ""
        },
        ......
    ]
}
```

## Read

### Request

- **Method:** GET
- **Url:** /personnel/api/resigns/{id}/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Path Parameters**

| Parameter | Description |
| --- | --- |
| id | required |

### Response

- **Url:** /personnel/api/resigns/5/

```json
{
    "id": 5,
    "resign_date": "2020-06-04",
    "resign_type": 1,
    "disableatt": true,
    "employee": {
        "id": 3,
        "emp_code": "11111122",
        "first_name": "aaabb",
        "last_name": ""
    },
    "first_name": "aaabb",
    "last_name": ""
}
```

## Create

- **Method:** POST
- **Url:** /personnel/api/resigns/
- **Headers:**
  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "employee": 3,
    "disableatt": true,
    "resign_type": 1,
    "resign_date": "2020-06-01",
    "reason": ""
}
```

|Parameter|Required|Type| Description | | ----- | ----- |---------------------------------------------| |resign_type|Y|Integer| default value:1, can input(1-5)five options | |disableatt|Y|Bool| true or false | |resign_date|Y|String| format: yyyy-mm-dd | |employee|Y|Integer| emp ID | |reason|N|String| max length:200 char |

### Response

```json
{
    "id": 5,
    "resign_date": "2020-06-01",
    "resign_type": 1,
    "disableatt": true,
    "employee": {
        "id": 3,
        "emp_code": "11111122",
        "first_name": "aaabb",
        "last_name": ""
    },
    "first_name": "aaabb",
    "last_name": ""
}
```

## Update

### Request

- **Method:** PUT
- **Url:** /personnel/api/resigns/{id}/
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
    "resign_date": "2020-06-02"
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| resign_type | N | Integer | default value:1, can input(1-5)five options |
| disableatt | N | Bool | true or false |
| disableatt | N | String | format: yyyy-mm-dd |
| reason | N | String | max length:200 char |

### Response

- **Url:** /personnel/api/resigns/5/

```json
{
    "id": 5,
    "resign_date": "2020-06-02",
    "resign_type": 1,
    "disableatt": true,
    "employee": {
        "id": 3,
        "emp_code": "11111122",
        "first_name": "aaabb",
        "last_name": ""
    },
    "first_name": "aaabb",
    "last_name": ""
}
```

## Delete

### Request

- **Method:** DELETE
- **Url:** /personnel/api/resigns/{id}/
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

## Reinstatement

### Request

- **Method:** POST
- **Url:** /personnel/api/resigns/reinstatement/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "resigns": [1]
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| resigns | Y | List | resign id list example: [1, 2, 3, ...] |
