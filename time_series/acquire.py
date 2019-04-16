import requests
import pandas as pd

base_url = 'https://python.zach.lol'

def get_data(location):
	response = requests.get(base_url + '/api/v1/' + location + '?page=1')
	data = response.json()

	df = pd.DataFrame(data['payload'][location])

	for i in range((data['payload']['max_page'])):
		print(base_url + '/api/v1/' + location + '?page=' + (str(i+1)))
		data = response.json()
		print(df.shape)
		df = pd.concat([df, pd.DataFrame(data['payload'][location])])
	return df


df_items = get_data('items')
df_stores = get_data('stores')
df_sales = get_data('sales')

df = df_sales.join(df_items.set_index('item_id'), on='item')
df = df_sales.join(df_stores.set_index('store_id'), on='store')

# df = pd.merge(df_items, df_sales, how='left', left_on='item_id', right_on='item')
# df = pd.merge(df_stores, df_sales, how='left', left_on='store_id', right_on='store')

print(df.shape)
print(df.columns)