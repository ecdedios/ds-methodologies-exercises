#!/usr/bin/env python

""" Utility functions et cetera. """

import os
import sys

import pandas as pd
import env

from sklearn.linear_model import LinearRegression


# ============
# ACQUIRE DATA
# ============

def get_connection(db, user=env.user, host=env.host, password=env.password):
	'''
	Open a connection to a mySQL database. The name of the database
	should be the input to this function. Make sure your database
	credentials are not included in this file.
	'''
	return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_zillow_prop6():
    return pd.read_sql('SELECT p6.*,\
       ac.airconditioningdesc,\
       arc.architecturalstyledesc,\
       bldg.buildingclassdesc,\
       plut.propertylandusedesc,\
       st.storydesc,\
       tct.typeconstructiondesc,\
       horst.heatingorsystemdesc\
       FROM properties_2016 AS p6\
       LEFT OUTER JOIN airconditioningtype as ac\
       ON ac.airconditioningtypeid = p6.airconditioningtypeid\
       LEFT OUTER JOIN architecturalstyletype as arc\
       ON arc.architecturalstyletypeid = p6.architecturalstyletypeid\
       LEFT OUTER JOIN buildingclasstype as bldg\
       ON bldg.buildingclasstypeid = p6.buildingclasstypeid\
       LEFT OUTER JOIN propertylandusetype as plut\
       ON plut.propertylandusetypeid = p6.propertylandusetypeid\
       LEFT OUTER JOIN storytype as st\
       ON st.storytypeid = p6.storytypeid\
       LEFT OUTER JOIN typeconstructiontype as tct\
       ON tct.typeconstructiontypeid = p6.typeconstructiontypeid\
       LEFT OUTER JOIN heatingorsystemtype as horst\
       ON horst.heatingorsystemtypeid = p6.heatingorsystemtypeid;',
       get_connection('zillow'))

def get_zillow_prop7():
    return pd.read_sql('SELECT p7.*,\
       ac.airconditioningdesc,\
       arc.architecturalstyledesc,\
       bldg.buildingclassdesc,\
       plut.propertylandusedesc,\
       st.storydesc,\
       tct.typeconstructiondesc,\
       horst.heatingorsystemdesc\
       FROM properties_2017 AS p7\
       LEFT OUTER JOIN airconditioningtype as ac\
       ON ac.airconditioningtypeid = p7.airconditioningtypeid\
       LEFT OUTER JOIN architecturalstyletype as arc\
       ON arc.architecturalstyletypeid = p7.architecturalstyletypeid\
       LEFT OUTER JOIN buildingclasstype as bldg\
       ON bldg.buildingclasstypeid = p7.buildingclasstypeid\
       LEFT OUTER JOIN propertylandusetype as plut\
       ON plut.propertylandusetypeid = p7.propertylandusetypeid\
       LEFT OUTER JOIN storytype as st\
       ON st.storytypeid = p7.storytypeid\
       LEFT OUTER JOIN typeconstructiontype as tct\
       ON tct.typeconstructiontypeid = p7.typeconstructiontypeid\
       LEFT OUTER JOIN heatingorsystemtype as horst\
       ON horst.heatingorsystemtypeid = p7.heatingorsystemtypeid;',
       get_connection('zillow'))

def get_zillow_pred6():
    return pd.read_sql('SELECT pred6.parcelid,\
		pred6.logerror,\
        pred6.transactiondate\
        FROM predictions_2016 as pred6;',
       get_connection('zillow'))

def get_zillow_pred7():
    return pd.read_sql('SELECT pred7.parcelid,\
            pred7.logerror,\
        pred7.transactiondate\
        FROM predictions_2017 as pred7;',
       get_connection('zillow'))

def save_df():
	'''
	Saves the dataframe as a csv file locally.
	'''
	get_zillow_prop6().to_csv("properties_2016.csv", index=False)
	get_zillow_prop7().to_csv("properties_2017.csv", index=False)
	get_zillow_pred6().to_csv("predictions_2016.csv", index=False)
	get_zillow_pred7().to_csv("predictions_2017.csv", index=False)


# ============
# PREPARE DATA
# ============

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

def validate_coords(df):
	'''
	Only includes properties that include a latitude and longitude value
	'''
	return df.dropna(subset = ['latitude', 'longitude'])

def make_single_unit_only(df):
	'''
	include only single unit properties (e.g. no duplexes, no land/lot, ...)
	'''
	return df.loc[(df['unitcnt'] == 1) | ((df['bathroomcnt'] >= 1) & (df['bathroomcnt'] <= 3))]


def convert_to_string(df, *cols):
    '''
	takes in a dataframe and a list of columns names and returns the dataframe
	with the datatypes of those columns changed to a non-numeric type
	'''
    for col in cols:
        df[col] = df[col].astype(str)
    return df


def impute_missing(df):
	'''
	Impute the values in land square feet using linear regression
	with landtaxvaluedollarcnt as x and estimated land square feet as y.
	'''
	# imputing landtaxvaluedollarcnt
	df_clean = df.dropna(subset = ['landtaxvaluedollarcnt', 'lotsizesquarefeet'])
	df_dirty = df.loc[pd.isnull(df.lotsizesquarefeet)]

	# Create linear regression objects
	lm1 = LinearRegression(fit_intercept=True)

	lm1.fit(df_clean[['landtaxvaluedollarcnt']], df_clean[['lotsizesquarefeet']])
	print(lm1)

	lm1_y_intercept = lm1.intercept_
	print(lm1_y_intercept)

	lm1_coefficients = lm1.coef_
	print(lm1_coefficients)

	print('Univariate - final_exam = b + m * exam1')
	print('    y-intercept (b): %.2f' % lm1_y_intercept)
	print('    coefficient (m): %.2f' % lm1_coefficients[0])
	print()

	y_pred_lm1 = lm1.predict(df_dirty[['landtaxvaluedollarcnt']])

	df.loc[df.lotsizesquarefeet.isna(), 'lotsizesquarefeet'] = y_pred_lm1

	return df




















def summarize_data(df):
    
    head_df = df.head()
    print(f'HEAD\n{head_df}', end='\n\n')
   
    tail_df = df.tail()
    print(f'TAIL\n{tail_df}', end='\n\n')

    shape_tuple = df.shape
    print(f'SHAPE: {shape_tuple}', end='\n\n')
    
    describe_df = df.describe()
    print(f'DESCRIPTION\n{describe_df}', end='\n\n')
    
    df.info()
    print(f'INFORMATION')
    

    print(f'VALUE COUNTS', end='\n\n')
    for col in df.columns:
        n = df[col].unique().shape[0]
        col_bins = min(n, 10)
        print(f'{col}:')
        if df[col].dtype in ['int64', 'float64'] and n > 10:
            print(df[col].value_counts(bins=col_bins, sort=False, dropna=False))
        else:
            print(df[col].value_counts(dropna=False))
        print('\n')


def missing_values_col(df):
	'''
	Write or use a previously written function to return the
	total missing values and the percent missing values by column.
	'''
	null_count = df.isnull().sum()
	null_percentage = (null_count / df.shape[0]) * 100
	empty_count = pd.Series(((df == ' ') | (df == '')).sum())
	empty_percentage = (empty_count / df.shape[0]) * 100
	nan_count = pd.Series(((df == 'nan') | (df == 'NaN')).sum())
	nan_percentage = (nan_count / df.shape[0]) * 100
	return pd.DataFrame({'num_missing': null_count, 'missing_percentage': null_percentage,
	                     'num_empty': empty_count, 'empty_percentage': empty_percentage,
	                     'nan_count': nan_count, 'nan_percentage': nan_percentage})


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

def remove_columns(df, cols_to_remove):  
    df = df.drop(columns=cols_to_remove)
    return df

def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

def handle_outliers(s, k, m):
	'''
    Given a series and a cutoff value, k, returns the upper outliers for the
    series.

    The values returned will be either 0 (if the point is not an outlier), or a
    number that indicates how far away from the upper bound the observation is.
    '''
	if m == 'iqr':
		q1, q3 = s.quantile([.25, .75])
		iqr = q3 - q1
		upper_bound = q3 + k * iqr
		return s.apply(lambda x: max([x - upper_bound, 0]))
	elif m == 'std':
		pass
	elif m == 'pcnt':
		pass


def getprep_zillow(*cols):
	df = join_zillow_data()
	df = validate_coords(df)
	df = make_single_unit_only(df)
	df = convert_to_string(df, *cols)
	return df

def auto_remove(df, cols_to_remove=[], prop_required_column=.5, prop_required_row=.75):
    df = remove_columns(df, cols_to_remove)
    df = handle_missing_values(df, prop_required_column, prop_required_row)
    return df


# ===========
# EXPLORATION
# ===========














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
__credits__ = ["Maggie Guist", "Zach Gulde", "Michael P. Moran"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ednalyn C. De Dios"
__email__ = "ednalyn.dedios@gmail.com"
__status__ = "Prototype"
