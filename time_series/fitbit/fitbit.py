# Operating System
import os
import sys

# Data Wrangling
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns

# Modeling
from sklearn.linear_model import LinearRegression
from matplotlib.figure import Figure
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, median_absolute_error

def get_fitbit_data():
    """
    Reads a merged csv file of the fitbit dataset.
    """
    # Snowhite and the Seven Dwarfs
    df1 = pd.read_csv('fitbit/data1.csv', low_memory=False)
    df2 = pd.read_csv('fitbit/data2.csv', low_memory=False)
    df3 = pd.read_csv('fitbit/data3.csv', low_memory=False)
    df4 = pd.read_csv('fitbit/data4.csv', low_memory=False)
    df5 = pd.read_csv('fitbit/data5.csv', low_memory=False)
    df6 = pd.read_csv('fitbit/data6.csv', low_memory=False)
    df7 = pd.read_csv('fitbit/data7.csv', low_memory=False)
    
    # Merge into one dataframe.
    df = pd.concat(df1, df2, df3, df4, df5, df6, df7)
    df.head(10)