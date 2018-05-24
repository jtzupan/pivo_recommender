#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from collections import namedtuple
import os
import re
import requests


def getHTMLText(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html5lib")
    return soup


def createBeerList(htmlText):
    listOfBeers = []
    for a in htmlText.find_all('a', href=True):
        j = re.match(r'/beer/profile/\d+/\d+/', a['href'])
        if j is not None:
            listOfBeers.append(j.group(0))

    urlBase = 'https://www.beeradvocate.com'
    beerURLList = [urlBase + i for i in listOfBeers]
    return beerURLList


def createReviewPageList(listOfBeers):
    beerReviewPageList = []
    beerReviewTuple = namedtuple('beerReviewTuple','beerID, reviewURL')
    for page in listOfBeers:
        # not all beers will have this many pages of reviews
        # thats fine, the URL will still return a page with no reviews
        # future: check the number of reviews of each beer
        beerID = page.split('/')[-2]
        for index in range(0,100, 25):
            reviewPageURL = page + '?sort=topr&start=' + str(index)
            beerReviewPageList.append(beerReviewTuple(beerID, reviewPageURL))
    return beerReviewPageList


def scrapyBeerList(startingURL='https://www.beeradvocate.com/lists/top/'):
    topBeersHTML = getHTMLText(startingURL)
    topBeersList = createBeerList(topBeersHTML)
    allReviewPages = createReviewPageList(topBeersList)

    return allReviewPages

