#!/usr/bin/env python

"""
This script is a stand-alone module.

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


def get_codeup_blog_links(path, num_pages):
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


def get_codeup_blog_texts(blog_link, num_pages, cache=True):
    if cache and os.path.exists('codeup_blog_articles.json'):
        blog_texts = json.load(open('codeup_blog_articles.json'))
    else:
        data = get_codeup_blog_links(blog_link, num_pages)
        blog_texts = []
        for value in traverse(data):
            blog_texts.append(get_codeup_article(value))
        json.dump(blog_texts, open('codeup_blog_articles.json', 'w'))
    return blog_texts



# =============
# NEWS ARTICLES
# =============


def get_news_article(url, category):
    """
    Takes a single complete url and returns a dictionary.
    """
    headers = {'User-Agent': 'Codeup Ada Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title')
    article = soup.find('a', class_='clickable', attrs={'href': re.compile("^/en/news")})
    
#     d = dict()
#     d['title'] = title.text
#     d['category'] = category
#     d['content'] = article.text

    return article.text

def get_news_links(url, category):
    """
    Takes a url and returns a list of links on that url's page.
    """
    headers = {'User-Agent': 'Codeup Ada Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title')
    links = []
    for link in soup.findAll('a', class_='clickable', attrs={'href': re.compile("^/en/news")}):
        links.append('https://inshorts.com' + link.get('href'))
    return links

def get_news_texts(*categories):
    """
    """
    
    all_news = []
    for category in categories:
        links = get_news_links(("https://inshorts.com/en/read/") + category, category)
        for link in links:
            all_news.append({
                "link": link,
                "category": category,
                "content": get_news_article(link, category)
            }) 
            
    return all_news





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

    links = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',
             'https://codeup.com/data-science-myths/',
             'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',
             'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',
             'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/',
            ]


    corpus = []

    for link in links:
        corpus.append(get_codeup_article(link))

    print(f'1. CODEUP BLOG ARTICLES \n')
    print(f'{corpus} \n')
    print(f'BONUS \n')
    print(f'{get_codeup_links("https://codeup.com/blog")} \n')
    print(f'BONUS BONUS \n')
    print(f'{get_codeup_blog_texts("https://codeup.com/blog/", 7)} \n')

    print(f'2. NEWS ARTICLES \n')

    corpus = get_news_texts('business',
                            'sports',
                            'technology',
                            'entertainment')

    print(corpus)


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

