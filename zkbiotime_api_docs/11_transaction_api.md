# Transaction

## List

### Request

- **Method:** GET
- **Url:** /iclock/api/transactions/
- **Headers:**
  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Query Parameters**

| Parameter | Description |
| --- | --- |
| page | Which page is displayed |
| page_size | Show the number of data on this page |
| emp_code | Use this field to query |
| terminal_sn | Use this field to query |
| terminal_alias | Use this field to query |
| start_time | Use this field to query, example: ?start_time=2022-07-04 10:00:00 |
| end_time | Use this field to query, example: ?end_time=2022-07-04 10:00:00 |

### Response

```json
{
    "count": 6,
    "next": null,
    "previous": null,
    "msg": "",
    "code": 0,
    "data": [
        {
            "id": 1,
            "emp_code": "11111111122",
            "first_name": "",
            "last_name": "",
            "department": "Department",
            "position": "Position",
            "punch_time": "2020-06-05 00:00:00",
            "punch_state": "0",
            "punch_state_display": "Check In",
            "verify_type": 0,
            "verify_type_display": "Password",
            "work_code": "",
            "gps_location": "",
            "area_alias": null,
            "terminal_sn": "",
            "temperature": 0.0,
            "terminal_alias": null,
            "upload_time": "2020-06-05 08:47:59"
        },
        ......
    ]
}
```

## Read

### Request

- **Method:** GET
- **Url:** /iclock/api/transactions/{id}/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Path Parameters**

| Parameter | Description |
| --- | --- |
| id | required |

### Response

```text
- **Url:** /iclock/api/transactions/1/
{
    "id": 1,
    "emp_code": "11111111122",
    "first_name": "",
    "last_name": "",
    "department": "Department",
    "position": "Position",
    "punch_time": "2020-06-05 00:00:00",
    "punch_state": "0",
    "punch_state_display": "Check In",
    "verify_type": 0,
    "verify_type_display": "Password",
    "work_code": "",
    "gps_location": "",
    "area_alias": null,
    "terminal_sn": "",
    "temperature": 0.0,
    "terminal_alias": null,
    "upload_time": "2020-06-05 08:47:59"
}
```

## Delete

### Request

- **Method:** DELETE
- **Url:** /iclock/api/transactions/{id}/
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

## Export

### Request

- **Method:** GET
- **Url:** /iclock/api/transactions/export/
- **Headers:**
  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Query Parameters**

| Parameter | Description |
| --- | --- |
| export_type | required, csv, txt, xls |
| page | Which page need export |
| page_size | How many data need export per page |
| emp_code | export this field |
| terminal_sn | export this field |
| terminal_alias | export this field |
| start_time | export time start of this field |
| end_time | export time end of this field |

### Response

```text
response type: bytes
b'id,em......-06-05 08:48:00\r\n'
```
