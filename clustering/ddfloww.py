#!/usr/bin/env python

"""
This script contains code used by the following jupytr notebooks:

1. acquire_zillow.ipynb
2. prepare_zillow.ipynb
3. explore_zillow.ipynb
4. model_zillow.ipynb

Special care taken to avoid hardcoding arguments as much as possible.
"""



# ===========
# ENVIRONMENT
# ===========


import os
import sys

import pandas as pd
import env
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns

from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, median_absolute_error
from sklearn.feature_selection import f_regression



# ===========
# ACQUISITION
# ===========


def get_connection(db, user=env.user, host=env.host, password=env.password):
	"""
	Open a connection to a mySQL database. The name of the database
	should be the input to this function. Make sure your database
	credentials are not included in this file.
	"""
	return f'mysql+pymysql://{user}:{password}@{host}/{db}'


def get_zillow_prop6():
	"""
	Returns dataset for properties_2016.csv
	"""
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
	"""
	Returns dataset for properties_2017.csv
	"""
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
	"""
	Returns dataset for predictions_2016.csv
	"""
	return pd.read_sql('SELECT pred6.parcelid,\
		pred6.logerror,\
		pred6.transactiondate\
		FROM predictions_2016 as pred6;',
		get_connection('zillow'))


def get_zillow_pred7():
	"""
	Returns dataset for predictions_2017.csv
	"""
	return pd.read_sql('SELECT pred7.parcelid,\
		pred7.logerror,\
		pred7.transactiondate\
		FROM predictions_2017 as pred7;',
		get_connection('zillow'))


def save_df():
	"""
	Saves the dataframe as a csv file locally.
	"""
	get_zillow_prop6().to_csv("properties_2016.csv", index=False)
	get_zillow_prop7().to_csv("properties_2017.csv", index=False)
	get_zillow_pred6().to_csv("predictions_2016.csv", index=False)
	get_zillow_pred7().to_csv("predictions_2017.csv", index=False)


def join_zillow_data():
	"""
	Generates a local csv of the Zillow dataset.
	"""

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

	# Saves a csv file locally for easy retrieval
	df.to_csv("zillow.csv", index=False)


def get_zillow():
	"""
	Reads in the zillow dataset.
	"""
	# save_df()
	# join_zillow_data()
	return pd.read_csv('zillow.csv', low_memory=False)



# ===========
# PREPARATION
# ===========


def handle_missing(df, prop_required_column = .5, prop_required_row = .75):
	"""
	Removes columns and rows whose count of missing values exceeds threshold.
	"""
	threshold = int(round(prop_required_column*len(df.index),0))
	df.dropna(axis=1, thresh=threshold, inplace=True)
	threshold = int(round(prop_required_row*len(df.columns),0))
	df.dropna(axis=0, thresh=threshold, inplace=True)
	return df


def remove_columns(df, cols_to_remove):
	"""
	Removes specified columns.
	""" 
	df = df.drop(columns=cols_to_remove)
	return df 


def validate_cols(df, cols_to_validate):
	"""
	Filters out rows with invalid latitude and longitude.
	"""
	return df.dropna(subset = cols_to_validate)


def make_single_unit(df):
	"""
	Estimates single unit homes.
	"""
	return df.loc[(df['unitcnt'] == 1) | ((df['bathroomcnt'] >= 1) &
				 (df['bathroomcnt'] <= 4) & (df['bedroomcnt'] <= 6))]


def prep_zillow(df, preq_col=.5, preq_row=.75, cols_to_remove=[], cols_to_validate=[]):
	df = handle_missing(df, preq_col, preq_row)
	df = remove_columns(df, cols_to_remove)
	df = validate_cols(df, cols_to_validate)
	df = make_single_unit(df)
	return df


# The code below inspires by Michael P. Moran's missing_vals_df().
def missing_values_col(df):
	"""
	Write or use a previously written function to return the
	total missing values and the percent missing values by column.
	"""
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
	"""
	Write or use a previously written function to return the
	total missing values and the percent missing values by row.
	"""
	null_count = df.isnull().sum(axis=1)
	null_percentage = (null_count / df.shape[1]) * 100
	return pd.DataFrame({'num_missing': null_count, 'percentage': null_percentage})


def impute_missing(df):
	"""
	Impute the values in land square feet using linear regression
	with landtaxvaluedollarcnt as x and estimated land square feet as y.
	"""
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

# The code below adapted from Michael P. Moran's snippet.
def summarize_data(df):
    
    df_head = df.head()
    print(f'HEAD\n{df_head}', end='\n\n')
   
    df_tail = df.tail()
    print(f'TAIL\n{df_tail}', end='\n\n')

    shape_tuple = df.shape
    print(f'SHAPE: {shape_tuple}', end='\n\n')
    
    df_describe = df.describe()
    print(f'DESCRIPTION\n{df_describe}', end='\n\n')
    
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


def fill_with_zeroes(df, *cols):
	"""
	Write a function that will take a dataframe and list of
	column names as input and return the dataframe with the
	null values in those columns replace by 0.
	"""
	for col in cols:
		df[col] = df[col].fillna(0)
	return df


def fill_with_median(df, *cols):
	"""
	Fill the NaN values with respective median values.
	"""
	for col in cols:
		df[col] = df[col].fillna(df[col].median())
	return df


def fill_with_none(df, *cols):
	"""
	Fill the NaN values with 'None' string value.
	"""
	for col in cols:
		df[col] = df[col].fillna('None')
	return df


def handle_outliers(s, k, m):
	"""
    Given a series and a cutoff value, k, returns the upper outliers for the
    series.

    The values returned will be either 0 (if the point is not an outlier), or a
    number that indicates how far away from the upper bound the observation is.
    """
	if m == 'iqr':
		q1, q3 = s.quantile([.25, .75])
		iqr = q3 - q1
		upper_bound = q3 + k * iqr
		return s.apply(lambda x: max([x - upper_bound, 0]))
	elif m == 'std':
		# TODO: handle outliers using standard deviation.
		pass
	elif m == 'pcnt':
		# TODO: handle outliers by top or bottom 1%
		pass


def convert_to_string(df, *cols):
    """
	takes in a dataframe and a list of columns names and returns the dataframe
	with the datatypes of those columns changed to a non-numeric type
	"""
    for col in cols:
        df[col] = df[col].astype(str)
    return df


def convert_to_int(df, *cols):
    """
	takes in a dataframe and a list of columns names and returns the dataframe
	with the datatypes of those columns changed to a non-numeric type
	"""
    for col in cols:
        df[col] = df[col].astype(int)
    return df


def convert_to_float(df, *cols):
    """
	takes in a dataframe and a list of columns names and returns the dataframe
	with the datatypes of those columns changed to a non-numeric type
	"""
    for col in cols:
        df[col] = df[col].astype(float)
    return df



# ===========
# EXPLORATION
# ===========


def standardize_data(df, columns):
	"""
	Standardizes the given variables using MixMax scaling.
	"""
	std_df = df
	for col in columns:
		std_df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
	return std_df


def plot_hist(df):
	"""
	Plots the distribution of the dataframe's variables.
	"""
	df.hist(figsize=(24, 20), bins=20)

# dd.plot_hist(df)


def plot_pairs(df, cols):
	"""
	Plots a pairplot of the dataframe with the given variables.
	"""
	sns.pairplot(df, vars=cols)

# dd.plot_pairs(df, num_cols)


def plot_heat(df):
	"""
	Plots a heatmap of the numerical variables.
	"""
	plt.figure(figsize=(12,8))
	sns.heatmap(df.corr(), cmap='RdYlBu', annot=True, center=0)

# df_heat = df[num_cols]
# dd.plot_heat(df_heat)


def plot_subs(df, cols):
	"""
	Creates subplots of boxplots.
	"""
	plt.figure(figsize=(16,20))
	for i, col in enumerate(cols):
	    plot_number = i + 1
	    plt.subplot(5,3,plot_number)
	    plt.title(col)
	    sns.boxplot(data=df[col])

# cols_to_plot = ['logerror', 'bathroomcnt', 'bedroomcnt', 'lotsizesquarefeet',
#                 'taxvaluedollarcnt', 'landtaxvaluedollarcnt']
# dd.plot_subs(df, *cols_to_plot)


def plot_rel(df, x, y, h):
	"""
	Creates a relplot.
	"""
	sns.relplot(x, y, h, data=df)


def plot_swarm(df, x, y, h):
	"""
	Creates subplots of swarmplots
	"""
	sns.swarmplot(x=x, y=y, data=df, hue=h)
	# TODO: finish this by making subplots.
	# TODO: replace this with another plot that run quickly.


def validate_tts(X_train, y_train, X_test, y_test, train, test):
    if X_train.shape[0] == y_train.shape[0]:
        print("X & y train rows ARE equal")
    else:
        print("X & y train rows ARE NOT equal")


    if X_test.shape[0] == y_test.shape[0]:
        print("X & y test rows ARE equal")
    else:
        print("X & y test rows ARE NOT equal")

    if train.shape[1] == test.shape[1]:
        print("Number of columns in train & test ARE equal")
    else:
        print("Number of columns in train & test ARE NOT equal")

    train_split = train.shape[0] / (train.shape[0] + test.shape[0])
    test_split = test.shape[0] / (train.shape[0] + test.shape[0])

    print("Train Split: %.2f" % train_split)
    print("Test Split: %.2f" % test_split)


# def see_elbow(df, col):
# 	df_temp = df[[col]]
# 	ks = range(1,10)
# 	sse = []
# 	for k in ks:
# 		kmeans = KMeans(n_clusters=k)
# 		kmeans.fit(df_temp)

# 		#intertia: Sum of squared distances of samples to their cluster center.
# 		sse.append(kmeans,inertia_)

# 	print(pd.DataFrame(dict(k=ks, see=sse)))

# 	plt.plot(ks, sse, 'bx-')
# 	plt.xlabel('k')
# 	plt.ylabel('SSE')
# 	plt.title('The Elbow Method Showing the Optimal k')
# 	plt.show()

# def add_clusters(df, col, estimators=[2,3]):
# 	pass


def model_linreg(X_train, y_train, features):
	# Create linear regression objects
	lm0 = LinearRegression()
	print(lm0)

	lm0.fit(X_train[features], y_train)
	print(lm0)

	lm0_y_intercept = lm0.intercept_
	print(lm0_y_intercept)

	lm0_coefficients = lm0.coef_
	print(lm0_coefficients)

	print()
	print('Univariate - log error = b + m1 * square feet')
	print('    y-intercept  (b): %.2f' % lm0_y_intercept)
	print('    coefficient (m1): %.2f' % lm0_coefficients[0][0])

	y_pred_lm0 = lm0.predict(X_train[features])

	mse_lm0 = mean_squared_error(y_train, y_pred_lm0)
	print("lm0\n  mse: {:.3}".format(mse_lm0)) 

	r2_lm0 = r2_score(y_train, y_pred_lm0)

	print('  {:.2%} of the variance in the log error can be explained by the number of square feet.'.format(r2_lm0))

	return lm0, r2_lm0



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

