# Employee

## List

### Request

- **Method:** GET
- **Url:** /personnel/api/employees/
- **Headers:**
  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Query Parameters**

| Parameter | Description |
| --- | --- |
| page | Which page is displayed |
| page_size | Show the number of data on this page |
| emp_code | Use this field to query |
| emp_code_icontains | Query the data that this field contains |
| first_name | Use this field to query |
| first_name_icontains | Query the data that this field contains |
| last_name | Use this field to query |
| last_name_icontains | Query the data that this field contains |
| department | Use this field to query |
| areas | Use this field to query |

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
            "emp_code": "007",
            "first_name": "",
            "last_name": null,
            "nickname": null,
            "device_password": null,
            "card_no": null,
            "department": {
                "id": 3715,
                "dept_code": "4",
                "dept_name": "MARS Egypt"
            },
            "position": null,
            "hire_date": "2020-06-01",
            "gender": null,
            "birthday": null,
            "verify_mode": 0,
            "emp_type": null,
            "contact_tel": null,
            "office_tel": null,
            "mobile": null,
            "national": null,
            "city": null,
            "address": null,
            "postcode": null,
            "email": null,
            "enroll_sn": "CEUY201760002",
            "ssn": null,
            "religion": null,
            "enable_att": true,
            "enable_overtime": false,
            "enable_holiday": true,
            "dev_privilege": 0,
            "area": [
                {
                    "id": 136,
                    "area_code": "1111.111.11",
                    "area_name": "test1"
                }
            ],
            "app_status": 0,
            "app_role": 1,
            "update_time": "2020-06-01 19:37:35",
            "fingerprint": "Ver 10:1",
            "face": "-",
            "palm": "-",
            "vl_face": "-"
        },
        ......
    ]
}
```

## Read

### Request

- **Method:** GET
- **Url:** /personnel/api/employees/{id}/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Path Parameters**

| Parameter | Description |
| --- | --- |
| id | required |

### Response

- **Url:** /personnel/api/employees/1/

```json
{
    "id": 1,
    "emp_code": "007",
    "first_name": "",
    "last_name": null,
    "nickname": null,
    "device_password": null,
    "card_no": null,
    "department": {
        "id": 3715,
        "dept_code": "4",
        "dept_name": "MARS Egypt"
    },
    "position": null,
    "hire_date": "2020-06-01",
    "gender": null,
    "birthday": null,
    "verify_mode": 0,
    "emp_type": null,
    "contact_tel": null,
    "office_tel": null,
    "mobile": null,
    "national": null,
    "city": null,
    "address": null,
    "postcode": null,
    "email": null,
    "enroll_sn": "CEUY201760002",
    "ssn": null,
    "religion": null,
    "enable_att": true,
    "enable_overtime": false,
    "enable_holiday": true,
    "dev_privilege": 0,
    "area": [
        {
            "id": 136,
            "area_code": "1111.111.11",
            "area_name": "test1"
        }
    ],
    "app_status": 0,
    "app_role": 1,
    "update_time": "2020-06-01 19:37:35",
    "fingerprint": "Ver 10:1",
    "face": "-",
    "palm": "-",
    "vl_face": "-"
}
```

## Create

- **Method:** POST
- **Url:** /personnel/api/employees/
- **Headers:**
  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "emp_code": "111111111",
    "department": 1,
    "area": [1, 2]
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| emp_code | Y | String | Employee Code |
| department | Y | Integer | department id, example: [1, 2, 3, ...] |
| area | Y | List | area id |
| hire_date | N | String | format: yyyy-mm-dd, default today |
| first_name | N | String | max length:25 char |
| last_name | N | String | max length:25 char |
| gender | N | String | S, F, M |
| mobile | N | String | max length:20 char |
| national | N | String | max length:50 char |
| address | N | String | max length:200 char |
| email | N | String | max length:50 char, input right format |
| app_status | N | Integer | (1, 'Enable');(0, 'Disable') |
| ... | N | String |  |
| ... | N | String |  |

### Response

```json
{
    "id": 100,
    "emp_code": "111111111",
    "first_name": "",
    "last_name": null,
    "nickname": null,
    "device_password": null,
    "card_no": null,
    "department": {
        "id": 1,
        "dept_code": "default dept",
        "dept_name": "default dept"
    },
    "position": null,
    "hire_date": "2020-06-01",
    "gender": null,
    "birthday": null,
    "verify_mode": 0,
    "emp_type": null,
    "contact_tel": null,
    "office_tel": null,
    "mobile": null,
    "national": null,
    "city": null,
    "address": null,
    "postcode": null,
    "email": null,
    "enroll_sn": "",
    "ssn": null,
    "religion": null,
    "enable_att": true,
    "enable_overtime": false,
    "enable_holiday": true,
    "dev_privilege": 0,
    "area": [
        {
            "id": 1,
            "area_code": "default dept",
            "area_name": "default dept"
        },
        {
            "id": 2,
            "area_code": "default dept1",
            "area_name": "default dept1"
        }
    ],
    "app_status": 0,
    "app_role": 1,
    "update_time": "2020-06-01 19:37:35",
    "fingerprint": -,
    "face": "-",
    "palm": "-",
    "vl_face": "-"
}
```

## Update

### Request

- **Method:** PUT
- **Url:** /personnel/api/employees/{id}/
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
    "emp_code": "111111111",
    "department": 1,
    "area": [1, 2]
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| emp_code | Y | String | Employee Code |
| department | Y | Integer | department id, example: [1, 2, 3, ...] |
| area | Y | List | area id |
| hire_date | N | String | format: yyyy-mm-dd, default today |
| first_name | N | String | max length:25 char |
| last_name | N | String | max length:25 char |
| gender | N | String | S, F, M |
| mobile | N | String | max length:20 char |
| national | N | String | max length:50 char |
| address | N | String | max length:200 char |
| email | N | String | max length:50 char, input right format |
| app_status | N | Integer | (1, 'Enable');(0, 'Disable') |
| ... | N | String |  |
| ... | N | String |  |

### Response

```json
{
    "id": 100,
    "emp_code": "111111111",
    "first_name": "",
    "last_name": null,
    "nickname": null,
    "device_password": null,
    "card_no": null,
    "department": {
        "id": 1,
        "dept_code": "default dept",
        "dept_name": "default dept"
    },
    "position": null,
    "hire_date": "2020-06-01",
    "gender": null,
    "birthday": null,
    "verify_mode": 0,
    "emp_type": null,
    "contact_tel": null,
    "office_tel": null,
    "mobile": null,
    "national": null,
    "city": null,
    "address": null,
    "postcode": null,
    "email": null,
    "enroll_sn": "",
    "ssn": null,
    "religion": null,
    "enable_att": true,
    "enable_overtime": false,
    "enable_holiday": true,
    "dev_privilege": 0,
    "area": [
        {
            "id": 1,
            "area_code": "default dept",
            "area_name": "default dept"
        },
        {
            "id": 2,
            "area_code": "default dept1",
            "area_name": "default dept1"
        }
    ],
    "app_status": 0,
    "app_role": 1,
    "update_time": "2020-06-01 19:37:35",
    "fingerprint": -,
    "face": "-",
    "palm": "-",
    "vl_face": "-"
}
```

## Delete

### Request

- **Method:** DELETE
- **Url:** /personnel/api/employees/{id}/
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

## Adjust area

### Request

- **Method:** POST
- **Url:** /personnel/api/employees/adjust_area/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "employees": [1, 2],
    "areas": [3, 4]
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| employees | Y | List | employee id list example: [1, 2, 3, ...] |
| areas | Y | List | area id list, example: [1, 2, 3, ...] |

## Adjust department

### Request

- **Method:** POST
- **Url:** /personnel/api/employees/adjust_department/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "employees": [1, 2],
    "department": 2
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| employees | Y | List | employee id list example: [1, 2, 3, ...] |
| department | Y | Integer | department id |

## Adjust regsin

### Request

- **Method:** POST
- **Url:** /personnel/api/employees/adjust_regsin/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "employees": [1, 2],
    "resign_date": 2,
    "resign_type": 1,
    "reason": "test reason",
    "disableatt": True
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| employees | Y | List | employee id list example: [1, 2, 3, ...] |
| resign_date | Y | String | format: yyyy-mm-dd |
| resign_type | Y | Integer | (1, quit), (2, dismissed), (3, resign), (4, transfer), (5, retainJobWithoutSalary), |
| reason | N | String | max length:200 char |
| disableatt | Y | Bool | true, false |

## Del bio template

### Request

- **Method:** POST
- **Url:** /personnel/api/employees/del_bio_template/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "employees": [1, 2],
    "finger_print": true,
    "face": false,
    "finger_vein": true,
    "palm": true
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| employees | Y | List | employee id list example: [1, 2, 3, ...] |
| finger_print | N | Bool | true, false |
| face | N | Bool | true, false |
| finger_vein | N | Bool | true, false |
| palm | N | Bool | true, false |

## Resync to device

### Request

- **Method:** POST
- **Url:** /personnel/api/employees/resync_to_device/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "employees": [1, 2]
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| employees | Y | List | employee id list example: [1, 2, 3, ...] |
