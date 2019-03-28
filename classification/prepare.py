# Create a function named prep_iris that accepts the untransformed iris data, and
# returns the data with the transformations above applied.
def prep_iris(df):
    df = acquire.get_iris_data()
    df = df.drop(['species_id', 'measurement_id'], axis=1)
    df = df.rename(columns={'species_name': 'species'})
    encoder = LabelEncoder()
    encoder.fit(df.species)
    df.species = encoder.transform(df.species)
    return df

# Create a function named prep_titanic that accepts the untransformed titanic data, and
# returns the data with the transformations above applied.
def prep_titanic(df):
    df.embark_town.value_counts(dropna=False)
    df.embark_town.fillna('Other', inplace=True)
    df.embark_town.value_counts(dropna=False)
    df.embarked.value_counts(dropna=False)
    df.embarked.fillna('Other', inplace=True)
    df.embarked.value_counts(dropna=False)
    df.drop(columns=['deck'], inplace=True)
    df.info()
    encoder = LabelEncoder()
    encoder.fit(df.embarked)
    df.embarked = encoder.transform(df.embarked)
    return df