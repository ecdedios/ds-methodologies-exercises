#!/usr/bin/env python

"""
The access log can be downloaded at:
http://python.zach.lol/access.log
"""



# ===========
# ENVIRONMENT
# ===========


import acquire
import os
import sys
import pandas as pd
import numpy as np

from datetime import datetime




# =======
# ACQUIRE
# =======


df = get_data()




# =======
# PREPARE
# =======


def parse_log(loglines):
    """
    Parses records from the access log and returns a dataframe.
    """

    logs = []

    for logline in loglines:
        log = logline.split(' ')

        ip_address = log[0]

        timestamp = (log[3] + ' ' + log[4]).replace(' ', '')
        timestamp = timestamp.replace(']', '')
        timestamp = timestamp.replace('[', '')

        http_method = (log[5]).replace('\"', '')
        path = (log[6]).replace('\"', '')
        protocol = (log[7]).replace('\"', '')
        status = int(log[8])
        size = int(log[9])
        user_agent = log[11].replace('\"', '')
        
        log_string = [ip_address,
                      timestamp,
                      http_method,
                      path,
                      protocol,
                      status,
                      size,
                      user_agent]
        print(log_string)

        logs.append(log_string)
        logs

    return pd.DataFrame(logs,columns=['ip_address',
                                      'timestamp',
                                      'http_method',
                                      'path',
                                      'protocol',
                                      'status',
                                      'size',
                                      'user_agent'])


def remove_space(df, column):
    """
    Removes the colon between date and hour.
    """
    return df[column].str.replace(':', ' ', 1)


def convert_to_datetime(df, column):
    """
    Converts string object to datetime object.
    """
    return pd.to_datetime(df[column])


def set_utc(df, locale):
    """
    Converts to UTC time.
    """
    return df.tz_localize('utc').tz_convert(locale)


def process_datetime(df, column, locale):
    """
    Pre-processess timestamp column.
    """
    df[column] = remove_space(df, column)
    df[column] = convert_to_datetime(df, column)
    df = df.set_index(column)
    return set_utc(df, locale)


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


def add_weekday(df, column):
    return df[column].dt.weekday


def add_date_columns(df, column):
    df.reset_index(inplace=True)
    df['year'] = add_year(df, column)
    df['quarter'] = add_quarter(df, column)
    df['month'] = add_month(df, column)
    df['day'] = add_day(df, column)
    df['hour'] = add_hour(df, column)
    df['weekday'] = add_weekday(df, column)
    return df




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
    df = parse_log(get_log())
    df = process_datetime(df, 'timestamp', 'America/Chicago')
    df = add_date_columns(df, 'timestamp')

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