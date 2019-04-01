# def drop_column(df, col):
#     return df.drop(columns=[col])

# def rename_column(df, col_old, col_new):
#     return df.rename(columns={col_old: col_new})

# def fill_null(df, col_name, col_value):
#     return df.col_name.fillna(col_value, inplace=True)


# def encode_species(df):
#     encoder = LabelEncoder()
#     encoder.fit(df.species)
#     return df.assign(species_encode = encoder.transform(df.species))

# def encode_embark_town(df):
#     encoder = LabelEncoder()
#     encoder.fit(df.embarked)
#     return df.assign(embarked_encode = encoder.transform(df.embarked))

# def encode_embarked(df):
#     encoder = LabelEncoder()
#     encoder.fit(df.embarked)
#     return df.assign(embarked_encode = encoder.transform(df.embarked))


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

# def prep_iris(df):
#     df = drop_column(df, 'species_id')
#     df = drop_column(df, 'measurement_id')
#     df = rename_column(df, 'species_name', 'species')
#     df = encode_species(df)
#     return df

# def prep_titanic(df):
#     df = fill_null(df, 'embark_town', 'Other')
#     df = fill_null(df, 'embarked', 'O')
#     df = drop_column(df, deck)
#     df = encode_embark_town(df)
#     df = encode_embarked(df)

# Create a function named prep_titanic that accepts the untransformed titanic data, and
# returns the data with the transformations above applied.
def prep_titanic(df):
    df.embark_town.value_counts(dropna=False)
    df.embark_town.fillna('Other', inplace=True)
    df.embark_town.value_counts(dropna=False)
    df.embarked.value_counts(dropna=False)
    df.embarked.fillna('O', inplace=True)
    df.embarked.value_counts(dropna=False)
    df.drop(columns=['deck'], inplace=True)
    df.info()
    encoder = LabelEncoder()
    encoder.fit(df.embarked)
    df.embarked = encoder.transform(df.embarked)
    return df