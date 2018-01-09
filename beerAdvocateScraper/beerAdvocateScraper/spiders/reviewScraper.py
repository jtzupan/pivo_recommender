# -*- coding: utf-8 -*-
import os
import sys
from scrapy import Spider, Item, Field
import scrapy

scraperPath = os.path.normpath(os.getcwd() + os.sep + os.pardir+ os.sep + os.pardir)

sys.path.insert(0, scraperPath)

import scraper

BAReviewList = scraper.scrapyBeerList()

class reviewData(Item):
    beerID = Field()
    reviewText = Field()

class ReviewscraperSpider(Spider):
    name = 'reviewScraper'
    
    def start_requests(self):

        allowed_domains = ['www.beeradvocate.com/beer/profile/']
        for beerID, url in BAReviewList:
            yield scrapy.Request(url=url, callback=self.parse, meta={'beerID':beerID})

    def parse(self, response):
        reviews = response.xpath('//*[@id="rating_fullview_content_2"]/text()[2]').extract()
        for review in reviews:
            beerID = response.meta['beerID']
            reviewText = review
            
            item = reviewData(beerID=beerID, reviewText=reviewText)
            
            yield item