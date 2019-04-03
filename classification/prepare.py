import os
from pandas import DataFrame
from sklearn.preprocessing import LabelEncoder
import acquire

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

def prep_iris_data(df):
    df = acquire.get_iris_data()
    df = df.drop(['species_id', 'measurement_id'], axis=1)
    df = df.rename(columns={'species_name': 'species'})
    encoder = LabelEncoder()
    encoder.fit(df.species)
    df.species = encoder.transform(df.species)
    return df