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


def make_single_only(df):
	'''
	include only single unit properties (e.g. no duplexes, no land/lot, ...)
	'''
	return df.loc[(df['unitcnt'] == 1) | ((df['bathroomcnt'] >= 1) & (df['bathroomcnt'] <= 7))]


def convert_to_string(df, *cols):
    '''
	takes in a dataframe and a list of columns names and returns the dataframe
	with the datatypes of those columns changed to a non-numeric type
	'''
    for col in cols:
        df[col] = df[col].astype(str)
    return df


def missing_values_col(df):
	'''
	Write or use a previously written function to return the
	total missing values and the percent missing values by column.
	'''
    null_count = df.isnull().sum()
    null_percentage = (null_count / df.shape[0]) * 100
    empty_count = pd.Series(((df == ' ') | (df == '')).sum())
    empty_percentage = (empty_count / df.shape[0]) * 100
    nan_value = pd.Series(((df == 'nan') | (df == 'NaN')).sum())
    nan_percentage = (nan_value / df.shape[0]) * 100
    return pd.DataFrame({'num_missing': null_count, 'percentage': null_percentage,
                         'num_empty': empty_count, 'nan_value': nan_value})


def missing_values_row(df):
	'''
	Write or use a previously written function to return the
	total missing values and the percent missing values by row.
	'''
    null_count = df.isnull().sum(axis=1)
    null_percentage = (null_count / df.shape[1]) * 100
    return pd.DataFrame({'num_missing': null_count, 'percentage': null_percentage})


def fill_with_zeroes(df, *cols):
	'''
	Write a function that will take a dataframe and list of
	column names as input and return the dataframe with the
	null values in those columns replace by 0.
	'''
    for col in cols:
        df[col] = df[col].fillna(0)
    return df


def prep_zillow_data():
	df = join_zillow_data()
	make_single_only(df)
	convert_to_string(df, 'id', 'airconditioningtypeid', 'architecturalstyletypeid', 'buildingclasstypeid',
                  'buildingqualitytypeid', 'decktypeid', 'fips', 'hashottuborspa', 'heatingorsystemtypeid',
                  'pooltypeid10', 'pooltypeid2', 'pooltypeid7', 'propertylandusetypeid', 'rawcensustractandblock',
                  'regionidcity', 'regionidcounty', 'regionidneighborhood', 'regionidzip', 'storytypeid',
                  'typeconstructiontypeid', 'fireplaceflag', 'taxdelinquencyflag' )

