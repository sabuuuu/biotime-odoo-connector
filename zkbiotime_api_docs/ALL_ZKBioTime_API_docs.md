# ZKBioTime 8.0 API Documentation

Source: http://192.168.100.250:8083/docs/api-docs/


---

<!-- http://192.168.100.250:8083/docs/api-docs/ -->

# Overview

## Version

| Edition | description | date |
| --- | --- | --- |
| v1.0.0 | Initial Draft | 2024.0725 |

## other docs

[ZKBio Time9.0 drf api docs](../../drf-docs/)


---

<!-- http://192.168.100.250:8083/docs/api-docs/request_and_response.html -->

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


---

<!-- http://192.168.100.250:8083/docs/api-docs/get_auth_token.html -->

# Get Auth Token

## Get General Auth Token

### Request

- **Method:** POST
- **Url:** /api-token-auth/
- **Headers:**

  - **Content-Type**: application/json
- **Body:**

| Parameter name | Required | Type | Description |
| --- | --- | --- | --- |
| username | Y | String |  |
| password | Y | String |  |

```json
{
    "username": "username",
    "password": "password"
}
```

### Response

- **Data type:** application/json

| Field name | Type | Description |
| --- | --- | --- |
| token | String |  |

```json
{
    "token": "gP4K......biHUoy"
}
```

## Python example

```text
import json
import requests

url = "http://{host}:{port}/api-token-auth/"
headers = {
    "Content-Type": "application/json",
}
data = {
    "username": "admin",
    "password": "admin"
}

response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.text)
```

## Postman example

![postman1](/docs/assets/postman1-4HTIR9N0.png)![postman2](/docs/assets/postman2-Ce5q3qG4.png)

## Java example

```java
public static String doPost(String httpUrl, String param) {

    HttpURLConnection connection = null;
    InputStream is = null;
    OutputStream os = null;
    BufferedReader br = null;
    String result = null;
    try {
        URL url = new URL(httpUrl);
        connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setConnectTimeout(15000);
        connection.setReadTimeout(60000);

        connection.setDoOutput(true);
        connection.setDoInput(true);
        connection.setRequestProperty("Content-Type", "application/json");da3efcbf-0845-4fe3-8aba-ee040be542c0
        os = connection.getOutputStream();
        os.write(param.getBytes());
        if (connection.getResponseCode() == 200) {

            is = connection.getInputStream();
            br = new BufferedReader(new InputStreamReader(is, "UTF-8"));

            StringBuffer sbf = new StringBuffer();
            String temp = null;
            while ((temp = br.readLine()) != null) {
                sbf.append(temp);
                sbf.append("\r\n");
            }
            result = sbf.toString();
        }
    } catch (MalformedURLException e) {
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    } finally {
        if (null != br) {
            try {
                br.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        if (null != os) {
            try {
                os.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        if (null != is) {
            try {
                is.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        connection.disconnect();
    }
    return result;
}

public static String buildParams(String username, String password){
    String tmp = "{\"username\": \"" + username + "\"," +
        " \"password\": \""+ password + "\"}";
    return tmp;
}

public static void main(String[] args){
    // final String url = "http://{host}:{port}/api-token-auth/";
    final String url = "http://{host}:{port}/api-token-auth/";
    String param = buildParams("admin", "admin");
    String result = doPost(url, param);
}
```


---

<!-- http://192.168.100.250:8083/docs/api-docs/use_auth_token.html -->

# Use Auth Token

## Python example

```python
import json
import requests

url = "http://{host}:{port}/personnel/api/areas/"
# use General token
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token ae600......2b7",
}
# or use JWT tokn
headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT ey.........oQi98",
}

response = requests.get(url, headers=headers)
print(response.text)
```

## Postman example

![postman3](/docs/assets/postman3-Dp0TALtP.png)

## Java example

```java
public static String doGet(String httpUrl, String token){
    HttpURLConnection connection = null;
    InputStream is = null;
    OutputStream os = null;
    BufferedReader br = null;
    String result = null;
    try {
        URL url = new URL(httpUrl);
        connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        connection.setConnectTimeout(15000);
        connection.setReadTimeout(60000);
        connection.setRequestProperty("Content-Type", "application/json");
        connection.setRequestProperty("Authorization", token);
        connection.connect();
        if (connection.getResponseCode() == 200) {

            is = connection.getInputStream();
            br = new BufferedReader(new InputStreamReader(is, "UTF-8"));

            StringBuffer sbf = new StringBuffer();
            String temp = null;
            while ((temp = br.readLine()) != null) {
                sbf.append(temp);
                sbf.append("\r\n");
            }
            result = sbf.toString();
        }
    } catch (MalformedURLException e) {
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    } finally {
        if (null != br) {
            try {
                br.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        if (null != os) {
            try {
                os.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        if (null != is) {
            try {
                is.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        connection.disconnect();
    }
    return result;
}

public static void main(String[] args){
    final String url = "http://{host}:{port}/personnel/api/areas/";
    final String token = "Token ae600......2b7";
    String result = doGet(url, token);
}
```


---

<!-- http://192.168.100.250:8083/docs/api-docs/api_example.html -->

# Api Example

## Python example

### get area list

```python
import json
import requests

url = "http://{host}:{port}/personnel/api/areas/"
# use General token
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token ae600......2b7",
}
# or use JWT tokn
headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT ey.........oQi98",
}

response = requests.get(url, headers=headers)
print(response.text)
```

### add area

```python
import json
import requests

url = "http://{host}:{port}/personnel/api/areas/"
# use General token
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token ae600......2b7",
}
# or use JWT tokn
headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT ey.........oQi98",
}

data = {
    'area_code': '0001',
    'area_name': 'test area'
}

response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.text)
```

### filter area list

```python
import json
import requests

url = "http://{host}:{port}/personnel/api/areas/"
# use General token
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token ae600......2b7",
}
# or use JWT tokn
headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT ey.........oQi98",
}

filter_params = {
    'area_name': 'test area'
}

response = requests.get(url, params=filter_params, headers=headers)
print(response.text)
```

### edit area

```python
import json
import requests

url = "http://{host}:{port}/personnel/api/areas/"
# use General token
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token ae600......2b7",
}
# or use JWT tokn
headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT ey.........oQi98",
}

data = {
    'area_name': 'test area name'
}

response = requests.put(url, data=json.dumps(data), headers=headers)
print(response.text)
```

### get area info

```python
import json
import requests

url = "http://{host}:{port}/personnel/api/areas/2/"
# use General token
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token ae600......2b7",
}
# or use JWT tokn
headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT ey.........oQi98",
}

response = requests.get(url, headers=headers)
print(response.text)
```

### delete area

```python
import json
import requests

url = "http://{host}:{port}/personnel/api/areas/2/"
# use General token
headers = {
    "Content-Type": "application/json",
    "Authorization": "Token ae600......2b7",
}
# or use JWT tokn
headers = {
    "Content-Type": "application/json",
    "Authorization": "JWT ey.........oQi98",
}

response = requests.delete(url, headers=headers)
print(response.text)
```


---

<!-- http://192.168.100.250:8083/docs/api-docs/area_api.html -->

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


---

<!-- http://192.168.100.250:8083/docs/api-docs/department_api.html -->

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


---

<!-- http://192.168.100.250:8083/docs/api-docs/position_api.html -->

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


---

<!-- http://192.168.100.250:8083/docs/api-docs/employee_api.html -->

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


---

<!-- http://192.168.100.250:8083/docs/api-docs/resign_api.html -->

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


---

<!-- http://192.168.100.250:8083/docs/api-docs/terminal_api.html -->

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


---

<!-- http://192.168.100.250:8083/docs/api-docs/transaction_api.html -->

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


---

<!-- http://192.168.100.250:8083/docs/api-docs/att_report.html -->

# Transaction Report

## Request

- **Method:** GET
- **Url:** /att/api/transactionReport/
- **Headers:**
  - **Content-Type**: application/json
  - **Authorization**: "JWT ey.........oQi98"
- **Query Parameters**

| Parameter | Description |
| --- | --- |
| page | Which page is displayed |
| page_size | Show the number of data on this page |
| start_date | Use this field to query,example: ?start_date=2022-07-04 |
| end_date | Use this field to query,example: ?end_date=2022-07-05 |
| departments | Use this field to query,example: ?departments=1 |
| areas | Use this field to query,example:?area=1 |
