#!/usr/bin/env python

"""
The access log can be downloaded at:
http://python.zach.lol/access.log
"""




# ===========
# ENVIRONMENT
# ===========


import acquire as ac
import os
import sys
import pandas as pd
import numpy as np

from datetime import datetime




# =======
# ACQUIRE
# =======


# imported from acquire.py




# =======
# PREPARE
# =======


def remove_space(df, column):
    """
    Removes the colon between date and hour.
    """
    return df[column].str.replace(':', ' ', 1)


def process_datetime(df, column, locale):
    """
    Pre-processess timestamp column.
    """
    df[column] = remove_space(df, column)
    df[column] = convert_to_datetime(df, column)
    df = df.set_index(column)
    return set_utc(df, locale)


# Write a function to convert a date to a datetime data type.
def convert_to_datetime(df, column):
    """
    Converts string object to datetime object.
    """
    datetime_format = '%a, %d %b %Y %H:%M:%S %Z'
    return pd.to_datetime(df[column], format=datetime_format)


# Write a function to change a datetime to UTC.
def set_utc(df, locale):
    """
    Converts to UTC time.
    """
    return df.tz_localize('utc').tz_convert(None)


# Write a function to parse a date column into 6 additional
# columns (while keeping the original date): year, quarter,
# month, day of month, day of week, weekend vs. weekday¶
def add_year(df, column):
    return df[column].dt.year


def add_quarter(df, column):
    return df[column].dt.quarter


def add_month(df, column):
    return df[column].dt.month


def add_day(df, column):
    return df[column].dt.day


def add_hour(df, column):
    return df[column].dt.hour


def add_dayofweek(df, column):
    return df[column].dt.weekday
    

def add_weekday(df, column):
    # return df[column].dt.weekday
    return ((pd.DatetimeIndex(df[column]).weekday) // 5 == 1).astype(float)


def add_date_columns(df, column):
    df.reset_index(inplace=True)
    df['year'] = add_year(df, column)
    df['quarter'] = add_quarter(df, column)
    df['month'] = add_month(df, column)
    df['day'] = add_day(df, column)
    df['dayofweek'] = add_dayofweek(df, column)
    df['weekday'] = add_weekday(df, column)
    return df


# Add a column to your dataframe, sales_total, which is a
# derived from sale_amount (total items) and item_price.
def add_sum_total(df, column1, column2):
    return df[column1] * df[column2]


#




# ==================================================
# MAIN
# ==================================================


def clear():
    """
    Clears the terminal screen.
    """
    os.system("cls" if os.name == "nt" else "clear")

def main():
    """
    Main entry point for the script.
    """
    df = ac.get_data()
    df['sale_date'] = convert_to_datetime(df, 'sale_date')
    df = df.set_index('sale_date')
    df = set_utc(df, 'America/Chicago')
    df = add_date_columns(df, 'sale_date')
    df['sales_total'] = add_sum_total(df, 'sale_amount', 'item_price')

    # Create a new dataframe that aggregates the sales_total and
    # sale_amount(item count) using sum and median by day of week.
    df_stotal_sum = pd.DataFrame(df.groupby('weekday')['sales_total'].sum())
    df_stotal_mean = pd.DataFrame(df.groupby('weekday')['sales_total'].mean())
    df_samount_sum = pd.DataFrame(df.groupby('weekday')['sale_amount'].sum())
    df_samount_mean = pd.DataFrame(df.groupby('weekday')['sale_amount'].mean())
    dfa = pd.merge(df_stotal_sum, df_stotal_mean, right_index=True, left_index=True)
    dfb = pd.merge(df_samount_sum, df_samount_mean, right_index=True, left_index=True)
    dfc = pd.merge(dfa, dfb, right_index=True, left_index=True)
    dfc.columns = ['sales_total_sum', 'sales_total_mean', 'sales_amount_sum', 'sales_amount_mean']

    # Explore the pandas DataFrame.diff() function. Create a new
    # column that is the result of the current sales - the previous
    # days sales.
    df['sales_diff'] = df.sales_total.diff()

    # Write a function to set the index to be the datetime variable.
    df = df.set_index('sale_date')

    print('Done and doner.')

    print(df.head(10))


if __name__ == '__main__':
    sys.exit(main())












__author__ = "Ednalyn C. De Dios, et al."
__copyright__ = "Copyright 2019, Codeup Data Science"
__credits__ = ["Maggie Guist", "Zach Gulde"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ednalyn C. De Dios"
__email__ = "ednalyn.dedios@gmail.com"
__status__ = "Prototype"