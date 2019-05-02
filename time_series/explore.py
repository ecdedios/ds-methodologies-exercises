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
    df, dfc = prep.prep_data(ac.get_data())

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