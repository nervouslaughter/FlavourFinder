import base64
import json
import requests

from base64 import b64encode



headers = {"Authorization": "Client-ID db886f20c5da9f2"}

api_key = 'e86eff8c1b826b265c544c9e383933ca1375c743'

url = "https://api.imgur.com/3/upload.json"

j1 = requests.post(
    url, 
    headers = headers,
    data = {
        'key': api_key, 
        'image': b64encode(open('img8.jpg', 'rb').read()),
        'type': 'base64',
        
    }


)
data = json.loads(j1.text)['data']; print(data['link'], data['id'], data['deletehash'])