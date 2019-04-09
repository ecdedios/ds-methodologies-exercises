import pandas as pd

def join_zillow_data():
	'''
	 return a single dataframe
	 '''

	# The FOUR HORSEMEN of the Apocalypse
	prop6_df = pd.read_csv('properties_2016.csv', low_memory=False)
	prop7_df = pd.read_csv('properties_2017.csv', low_memory=False)
	pred6_df = pd.read_csv('predictions_2016.csv', low_memory=False)
	pred7_df = pd.read_csv('predictions_2017.csv', low_memory=False)

	# Join predictions and properties together
	df6 = pd.merge(pred6_df, prop6_df, on='parcelid', how='inner')
	df7 = pd.merge(pred7_df, prop7_df, on='parcelid', how='inner')

	# Join 2016 and 2017 data together
	df = pd.concat([df6, df7])

	return df


def single_only(df):
	'''
	include only single unit properties (e.g. no duplexes, no land/lot, ...)
	'''
	return df.loc[df['unitcnt'] == 1].head(10)


def convert_to_string(df, *cols):
    '''
	takes in a dataframe and a list of columns names and returns the dataframe
	with the datatypes of those columns changed to a non-numeric type
	'''
    for col in cols:
        df[col] = df[col].astype(str)
    return df


def prep_zillow_data():
	df = join_zillow_data()
	single_only(df)
	convert_to_string(df)