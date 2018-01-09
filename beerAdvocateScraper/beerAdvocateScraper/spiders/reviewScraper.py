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