import requests
import json

url = "http://127.0.0.1:4998/send_group_msg"

payload = json.dumps({
   "group_id": "260503685",
   "message": [
      {
         "type": "music",
         "data": {
            "type": "163",
            "id": "1867921493"
         }
      }
   ]
})
headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
