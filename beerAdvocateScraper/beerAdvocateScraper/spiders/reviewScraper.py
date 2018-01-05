# -*- coding: utf-8 -*-
import sys
from scrapy import Spider, Item, Field
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
import scrapy

sys.path.insert(0, '/Users/johnzupan/mystuff/pivo_rec')

import scraper

BAReviewList = scraper.scrapyBeerList()

class reviewData(Item):
    beerName = Field()
    reviewText = Field()

class ReviewscraperSpider(Spider):
    name = 'reviewScraper'
    allowed_domains = ['www.beeradvocate.com/beer/profile/']
    start_urls = [url for url in BAReviewList]

    def parse(self, response):
        reviews = response.xpath('//*[@id="rating_fullview_content_2"]/text()[2]').extract()
        for review in reviews:
            beerName = 'PracticeBeer'
            reviewText = review
            
            item = reviewData(beerName=beerName, reviewText=reviewText)
            
            yield item