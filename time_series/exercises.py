import requests


base_url = 'https://python.zach.lol'
response = requests.get("https://python.zach.lol/api/v1/items")

data = response.json()
print(data.keys()

data["payload"].keys()