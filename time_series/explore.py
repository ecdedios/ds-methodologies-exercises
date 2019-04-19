#!/usr/bin/env python

"""
Make subplots where each is plotting sales over different periods
(daily, weekly, monthly, e.g.). The sales should be grouped by store
(color to represent store).

I want to see the number of each type of item that are sold over 
time for each store. Find a way to chart this. Hints: subplots for
the piece with the fewest distinct values (like store), x = time,
y = count, color = item. If you have too many distinct items, you
may need to plot the top n, while aggregating the others into an
'other' bucket.
"""




# ===========
# ENVIRONMENT
# ===========

import acquire as ac
import prepare as prep

import os
import sys
import pandas as pd
import numpy as np










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
    df['sale_date'] = prep.convert_to_datetime(df, 'sale_date')
    df = df.set_index('sale_date')
    df = prep.set_utc(df, 'America/Chicago')
    df = prep.add_date_columns(df, 'sale_date')
    df['sales_total'] = prep.add_sum_total(df, 'sale_amount', 'item_price')

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