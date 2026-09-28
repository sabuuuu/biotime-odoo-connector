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
