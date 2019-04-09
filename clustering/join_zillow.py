import pandas as pd

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