#!/usr/bin/env python

"""
This script contains code used by the following jupytr notebooks:

- dd_acquire.ipynb
- jesse_acquire.ipynb 

Special care taken to avoid hardcoding as much as possible.
"""



# ===========
# ENVIRONMENT
# ===========

import os
import sys
import requests
import pandas as pd

base_url = 'https://python.zach.lol'



# def get_data(location):
# 	"""
# 	This function has a keyword input that is concatenated to create
# 	a valid URL path. It returns a dataframe containing all the data
# 	from all of its pages.
# 	"""
# 	response = requests.get(base_url + '/api/v1/' + location + '?page=1')
# 	data = response.json()

# 	df = pd.DataFrame(data['payload'][location])

# 	for i in range((data['payload']['max_page'])):
# 		print(base_url + '/api/v1/' + location + '?page=' + (str(i+1)))
# 		response = requests.get(base_url + '/api/v1/' + location + '?page=' + (str(i+1)))
# 		data = response.json()
# 		print(df.shape)
# 		df = pd.concat([df, pd.DataFrame(data['payload'][location])])
# 	return df

# Get the data and store it in a dataframe
# df_items = get_data('items')
# df_stores = get_data('stores')
# df_sales = get_data('sales')

# Saves the dataframes into local csv files
# df_items.to_csv('data_items.csv')
# df_stores.to_csv('data_stores.csv')
# df_sales.to_csv('data_sales.csv')

def get_data():
	"""
	Gets all the data by reading from csv files.
	"""
	df_items = pd.read_csv('data_items.csv')
	df_stores = pd.read_csv('data_stores.csv')
	df_sales = pd.read_csv('data_sales.csv')

	df_sales.rename(columns={'store': 'store_id', 'item': 'item_id'}, inplace=True)
	df = pd.merge(df_sales, df_items, on='item_id')
	df = pd.merge(df, df_stores, on='store_id')

	return df

def get_store_data():
    """
    Gets all the data by reading from csv files.
    """
    return pd.read_csv('saas.csv')

# Merge all three dataframes together into one big dataframe
# df = df_sales.join(df_items.set_index('item_id'), on='item', how='inner')
# df = df.join(df_stores.set_index('store_id'), on='store', how='inner')\

df = get_data()
print(df.head(10))

# Check shape for validity after merge
print(f'SHAPE: {df.shape}')
print(f'COLUMNS: {df.columns}')



# ==================================================
# MAIN
# ==================================================


def clear():
	os.system("cls" if os.name == "nt" else "clear")

def main():
    """Main entry point for the script."""
    pass


if __name__ == '__main__':
    sys.exit(main())










__author__ = "Ednalyn C. De Dios, et al."
__copyright__ = "Copyright 2019, Codeup Data Science"
__credits__ = ["Maggie Guist", "Zach Gulde"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ednalyn C. De Dios"
__email__ = "ednalyn.dedios@gmail.com"
__status__ = "Prototype"