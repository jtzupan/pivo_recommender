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

#def getReviews(singleBeerURL):
#    listOfReviewText = []
#    rePattern = re.compile(r'</span><br/><br/>([\d\D]*)\.<br/>')
#    beerReview = requests.get(singleBeerURL)
#    beerReviewSoup = BeautifulSoup(beerReview.text, 'html5lib')
#    for review in beerReviewSoup.find_all('div', id='rating_fullview_content_2'):
#        reviewMatch = re.findall(rePattern, str(review))
#        if reviewMatch:
#            listOfReviewText.append(reviewMatch)
#    return listOfReviewText


#def runScraper(startingURL='https://www.beeradvocate.com/lists/top/'):
#    review_count = 0
#    topBeersHTML = getHTMLText(startingURL)
#    topBeersList = createBeerList(topBeersHTML)[:2]
#    allReviewPages = createReviewPageList(topBeersList)
#    intermediate_directory = os.path.join('.', 'intermediate')
#    review_txt_filepath = os.path.join(intermediate_directory,'review_text_all.txt')
#    with open(review_txt_filepath, 'w', encoding='utf_8') as review_txt_file:
#        for page in allReviewPages:
#            allReviews = getReviews(page)
#            for review in allReviews:
#                formattedReview = review[0].replace('<br/>',' ').replace('&amp;','')
#                review_txt_file.write(formattedReview.replace('\n', '') + '\n')
#                review_count += 1
#        
#    print(f'Collect {review_count} beer reviews')
#    return None

def scrapyBeerList(startingURL='https://www.beeradvocate.com/lists/top/'):
    topBeersHTML = getHTMLText(startingURL)
    topBeersList = createBeerList(topBeersHTML)[:2]
    allReviewPages = createReviewPageList(topBeersList)

    return allReviewPages

