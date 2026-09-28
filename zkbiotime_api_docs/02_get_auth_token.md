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
