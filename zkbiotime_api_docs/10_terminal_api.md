# Device

## List

### Request

- **Method:** GET
- **Url:** /iclock/api/terminals/
- **Headers:**
  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Query Parameters**

| Parameter | Description |
| --- | --- |
| page | Which page is displayed |
| page_size | Show the number of data on this page |
| sn | Use this field to query |
| alias | Use this field to query |
| state | Use this field to query |
| area | Use this field to query |
| sn_icontains | Query the data that this field contains |
| alias_icontains | Query the data that this field contains |

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
            "id": 5,
            "sn": "A6KX192060002",
            "ip_address": "172.30.7.162",
            "alias": "Auto add",
            "terminal_name": null,
            "fw_ver": null,
            "push_ver": null,
            "state": 1,
            "terminal_tz": 8,
            "area": {
                "id": 1,
                "area_code": "1",
                "area_name": "Not Authorized"
            },
            "last_activity": "2020-06-02 15:04:38",
            "user_count": null,
            "fp_count": null,
            "face_count": null,
            "palm_count": null,
            "transaction_count": null,
            "push_time": null,
            "transfer_time": "00:00;14:05",
            "transfer_interval": 1,
            "is_attendance": 1,
            "area_name": "Not Authorized"
        },
        ......
    ]
}
```

## Read

### Request

- **Method:** GET
- **Url:** /iclock/api/terminals/{id}/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Path Parameters**

| Parameter | Description |
| --- | --- |
| id | required |

### Response

- **Url:** /iclock/api/terminals/5/

```json
{
    "id": 5,
    "sn": "A6KX192060002",
    "ip_address": "172.30.7.162",
    "alias": "Auto add",
    "terminal_name": null,
    "fw_ver": null,
    "push_ver": null,
    "state": 1,
    "terminal_tz": 8,
    "area": {
        "id": 1,
        "area_code": "1",
        "area_name": "Not Authorized"
    },
    "last_activity": "2020-06-02 15:04:38",
    "user_count": null,
    "fp_count": null,
    "face_count": null,
    "palm_count": null,
    "transaction_count": null,
    "push_time": null,
    "transfer_time": "00:00;14:05",
    "transfer_interval": 1,
    "is_attendance": 1,
    "area_name": "Not Authorized"
}
```

## Create

- **Method:** POST
- **Url:** /iclock/api/terminals/
- **Headers:**
  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "sn": "111111111",
    "alias": "test device",
    "ip_address": "127.0.0.1",
    "terminal_tz": 8,
    "heartbeat": 10,
    "area": 1
}
```

|Parameter|Required|Type| Description | | ----- | ----- |------------------| |sn|Y|String| Serial Number | |alias|Y|String| Device Name | |ip_address|Y|String| Device IP | |terminal_tz|N|Integer| 54 options | |heartbeat|N|Integer| default value:10 | |area|N|Integer| area | |...|N|String| | |...|N|String| |

### Response

```json
{
    "id": 9,
    "sn": "111111111",
    "ip_address": "127.0.0.1",
    "alias": "test device",
    "terminal_name": null,
    "fw_ver": null,
    "push_ver": null,
    "state": 1,
    "terminal_tz": 8,
    "area": {
        "id": 1,
        "area_code": "1",
        "area_name": "Not Authorized"
    },
    "last_activity": "2020-06-02 15:04:38",
    "user_count": null,
    "fp_count": null,
    "face_count": null,
    "palm_count": null,
    "transaction_count": null,
    "push_time": null,
    "transfer_time": "00:00;14:05",
    "transfer_interval": 1,
    "is_attendance": 1,
    "area_name": "Not Authorized"
}
```

## Update

### Request

- **Method:** PUT
- **Url:** /iclock/api/terminals/{id}/
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
    "sn": "111111111",
    "alias": "test device",
    "ip_address": "127.0.0.1",
    "terminal_tz": 8,
    "heartbeat": 10,
    "area": 1
}
```

|Parameter|Required|Type| Description | | ----- | ----- |------------------| |sn|Y|String| Serial Number | |alias|Y|String| Device Name | |ip_address|Y|String| Device IP | |terminal_tz|N|Integer| 54 options | |heartbeat|N|Integer| default value:10 | |area|N|Integer| area | |...|N|String| | |...|N|String| |

## Delete

### Request

- **Method:** DELETE
- **Url:** /iclock/api/terminals/{id}/
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

## Clear command

### Request

- **Method:** POST
- **Url:** /iclock/api/terminals/clear_command/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "terminals": [1]
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| terminals | Y | List | terminal id list example: [1, 2, 3, ...] |

## Clear command

### Request

- **Method:** POST
- **Url:** /iclock/api/terminals/clear_command/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "terminals": [1]
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| terminals | Y | List | terminal id list example: [1, 2, 3, ...] |

## Clear capture

### Request

- **Method:** POST
- **Url:** /iclock/api/terminals/clear_capture/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "terminals": [1]
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| terminals | Y | List | terminal id list example: [1, 2, 3, ...] |

## Clear all

### Request

- **Method:** POST
- **Url:** /iclock/api/terminals/clear_all/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "terminals": [1]
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| terminals | Y | List | terminal id list example: [1, 2, 3, ...] |

## Upload all

### Request

- **Method:** POST
- **Url:** /iclock/api/terminals/upload_all/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "terminals": [1]
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| terminals | Y | List | terminal id list example: [1, 2, 3, ...] |

## Upload transaction

### Request

- **Method:** POST
- **Url:** /iclock/api/terminals/upload_transaction/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "terminals": [1]
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| terminals | Y | List | terminal id list example: [1, 2, 3, ...] |

## Reboot

### Request

- **Method:** POST
- **Url:** /iclock/api/terminals/reboot/
- **Headers:**

  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Request Body**

```json
{
    "terminals": [1]
}
```

| Parameter | Required | Type | Description |
| --- | --- | --- | --- |
| terminals | Y | List | terminal id list example: [1, 2, 3, ...] |
