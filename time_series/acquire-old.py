import requests
import pandas as pd

base_url = 'https://python.zach.lol'

response = requests.get('https://python.zach.lol/api/v1/items')
data = response.json()
print(data.keys())
print(data['payload'].keys())


location='sales'

response = requests.get(base_url + '/api/v1/' + location + '?page=' + (str(i+1)))
data = response.json()

df = pd.DataFrame(data['payload'][location])

for i in range((data['payload']['max_page'])):
    print(base_url + '/api/v1/' + location + '?page=' + (str(i+1)))
    data = response.json()
    print(df.shape)
    df = pd.concat([df, pd.DataFrame(data['payload'][location])])