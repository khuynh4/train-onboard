import json
import requests
url = 'http://localhost:5000'
params = {
    'name' : 'Jake',
    'info' : 'pretty cool'
    }
r = requests.post(url, data=params)
r = json.loads(r.text)
print(r)