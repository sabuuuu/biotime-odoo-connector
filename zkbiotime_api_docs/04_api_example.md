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
