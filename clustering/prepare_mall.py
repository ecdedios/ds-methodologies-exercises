from sklearn.preprocessing import LabelEncoder
from acquire_mall import get_mall_data


def get_upper_outliers(s, k):
    '''
    Given a series and a cutoff value, k, returns the upper outliers for the
    series.

    The values returned will be either 0 (if the point is not an outlier), or a
    number that indicates how far away from the upper bound the observation is.
    '''
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    upper_bound = q3 + k * iqr
    return s.apply(lambda x: max([x - upper_bound, 0]))

def encode_gender(df):
	# Encode the gender using a sklearn label encoder.
	encoder = LabelEncoder()
	encoder.fit(df.gender)
	df['gender_id'] = encoder.transform(df.gender)
	return df


def wrangle_mall_data(df):
	print(get_upper_outliers(df['annual_income'], 1.5))
	encode_gender(df)
	return df

