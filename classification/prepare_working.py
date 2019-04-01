from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder


def drop_column(df, col):
    return df.drop(columns=[col])

def rename_column(df, col_old, col_new):
    return df.rename(columns={col_old: col_new})

def fill_null(df, col_name, col_value):
    return df.col_name.fillna(col_value, inplace=True)


def encode_species(df):
    encoder = LabelEncoder()
    encoder.fit(df.species)
    return df.assign(species_encode = encoder.transform(df.species))


def prep_iris_data(df):
    df = df.drop(['species_id', 'measurement_id'], axis=1)
    df = df.rename(columns={'species_name': 'species'})
    encoder = LabelEncoder()
    encoder.fit(df.species)
    return df.assign(species_encode = encoder.transform(df.species))


def handle_missing_values(df):
    return df.assign(
        embark_town=df.embark_town.fillna('Other'),
        embarked=df.embarked.fillna('O'),
    )

def remove_columns(df):
    return df.drop(columns=['deck'])

def encode_embarked(df):
    encoder = LabelEncoder()
    encoder.fit(df.embarked)
    return df.assign(embarked_encode = encoder.transform(df.embarked))

def prep_titanic_data(df):
    df = df\
        .pipe(handle_missing_values)\
        .pipe(remove_columns)\
        .pipe(encode_embarked)
    return df