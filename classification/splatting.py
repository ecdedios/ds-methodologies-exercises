import pandas as pd

from acquire import get_titanic_data
from prepare import prep_titanic_data

def set_features(df, target, *features):
    X = df[['pclass','age','fare','sibsp','parch']]
    y = df[[target]]
    return X, y

    
# Get and prepare the data
df = prep_titanic_data(get_titanic_data())

# Set the features
features = ['pclass','age','fare','sibsp','parch']
target = 'survived'
X,y = set_features(df, target, *features, )