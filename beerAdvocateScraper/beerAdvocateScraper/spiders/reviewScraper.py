# -*- coding: utf-8 -*-
import os
import sys
from scrapy import Spider, Item, Field
import scrapy

scraperPath = os.path.normpath(os.getcwd()+ os.sep +os.pardir+os.sep+ 'tools')

sys.path.insert(0, scraperPath)

import scraper

BAReviewList = scraper.scrapyBeerList(topN=3)

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
        allText = response.xpath('//*[@id="rating_fullview_content_2"]/text()').extract()
        allTextJoin = ''.join(allText)
        for line in allTextJoin.split('\xa0'):
            if not (line=='' or line=='rDev '):
                if line.startswith('rDev'):
                    currentReview = line.replace('rDev ', '').replace('\n','')

                beerID = response.meta['beerID']
                reviewText = currentReview
                item = reviewData(beerID=beerID, reviewText=reviewText)
                
                yield item
