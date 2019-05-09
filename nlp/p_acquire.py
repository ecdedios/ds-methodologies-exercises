#!/usr/bin/env python

"""
This script is used by the following.

"""



import os
import sys

import pandas as pd
import re
import json

from requests import get
from bs4 import BeautifulSoup



# ===============
# CODEUP ARTICLES
# ===============


def get_codeup_article(url):
    headers = {'User-Agent': 'Codeup Ada Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title')
    article = soup.find('div', class_='mk-single-content')
    
    d = dict()
    d['title'] = title.text
    d['content'] = article.text

    return d


def get_codeup_links(link):
    headers = {'User-Agent': 'Codeup Ada Data Science'}
    response = get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title')
    links = []

    for link in soup.findAll('a', class_='mk-readmore', attrs={'href': re.compile("^https?://")}):
        links.append(link.get('href'))

    return links


def get_github_links(path, num_pages):
    blog_links = []
    for i in range(num_pages):      # Number of pages plus one
        page = i + 1
        headers = {'User-Agent': 'Codeup Ada Data Science'}
        response = get(path + str(page), headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        blog_links.append(get_codeup_links(path + str(page)))
#         print(blog_links)
    return blog_links


def traverse(o, tree_types=(list, tuple)):
    if isinstance(o, tree_types):
        for value in o:
            for subvalue in traverse(value, tree_types):
                yield subvalue
    else:
        yield o


def get_github_texts(blog_link, num_pages, cache=True):
    if cache and os.path.exists('github_articles.json'):
        blog_texts = json.load(open('github_articles.json'))
    else:
        data = get_github_links(blog_link, num_pages)
        blog_texts = []
        for value in traverse(data):
            blog_texts.append(get_codeup_article(value))
        json.dump(blog_texts, open('github_articles.json', 'w'))
    return blog_texts



# ==================================================
# MAIN
# ==================================================


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    """Main entry point for the script."""

    print(f'{get_github_texts("https://github.com/search?q=san+antonio+data&type=Repositories", 3)} \n')


if __name__ == '__main__':
    sys.exit(main())










__author__ = "Ednalyn C. De Dios"
__copyright__ = "Copyright 2019, Codeup Data Science"
__credits__ = ["Maggie Guist", "Zach Gulde", "Ryan Orsinger"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ednalyn C. De Dios"
__email__ = "ednalyn.dedios@gmail.com"
__status__ = "Prototype"

