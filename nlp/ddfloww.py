#!/usr/bin/env python

"""
This script contains code used by the following jupytr notebooks:

1. nlp.ipynb
2. scraping.ipynb
3.
"""



import os
import sys

import pandas as pd
import re

from requests import get
from bs4 import BeautifulSoup
from django.urls import path
# from functools import wraps, partial, WRAPPER_ASSIGNMENTS



def select(df, *args, **kwargs):
    return pd.concat([
        df[list(args)],
        df[list(kwargs.keys())].rename(columns=kwargs)
    ], axis=1)


def show_all_matches(regexes, subject, re_length=6):
    print('Sentence:')
    print()
    print('    {}'.format(subject))
    print()
    print(' regexp{} | matches'.format(' ' * (re_length - 6)))
    print(' ------{} | -------'.format(' ' * (re_length - 6)))
    for regexp in regexes:
        fmt = ' {:<%d} | {!r}' % re_length
        matches = re.findall(regexp, subject)
        if len(matches) > 8:
            matches = matches[:8] + ['...']
        print(fmt.format(regexp, matches))


def get_article_text():
    # if we already have the data, read it locally
    if os.path.exists('article.txt'):
        with open('article.txt') as f:
            return f.read()

    # otherwise go fetch the data
    url = 'https://codeup.com/codeups-data-science-career-accelerator-is-here/'
    headers = {'User-Agent': 'Codeup Ada Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text)
    article = soup.find('div', class_='mk-single-content')

    # save it for next time
    with open('article.txt', 'w') as f:
        f.write(article.text)

    return article.text










# ==================================================
# MAIN
# ==================================================


def clear():
	os.system("cls" if os.name == "nt" else "clear")

def main():
    """Main entry point for the script."""
    pass


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

