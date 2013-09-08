#--- Standard ---
import os
import sys 
import pickle
import time
import csv
from collections import defaultdict

#--- Scrapy ---
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from meme_scraper.items import Meme_Item

#--- My Files ---
from common_utilities import print_welcome, print_message, print_error, print_status, print_inner_status
from MemeSpider import MemeSpider



# Class: MakeAMemeSpider
# ---------------------
# crawls MakeAMeme.org
class MakeAMemeSpider (MemeSpider):

    #--- Scraper Identity ---
    name = "makeameme"
    allowed_domains = ["makeameme.org"]


    ########################################################################################################################
    ###################[ --- Constructor/Initialization/Destructor --- ]###################################################################
    ########################################################################################################################

    # Function: constructor
    # ---------------------
    # starts up selenium and begins the requests and makes the appropriate directories
    def __init__ (self):

        ### Step 1: initialization ###
        self.initialize ()








    ########################################################################################################################
    ###################[ --- URL Transformation Utilities --- ]#############################################################
    ########################################################################################################################

    # Functions: get_meme_page_url
    # ----------------------------
    # given a meme name, this returns the url of its first page
    def get_meme_page_url (self, meme_name):

        return "http://makeameme.org/character/" + meme_name + '/1'


    # Function: get_next_page_url
    # ---------------------------
    # given an htmlxpathselector, this will return an xpath to 
    # the next page. returns None if there are no more pages
    def get_next_page_url (self, meme_name):

        self.current_page_index[meme_name] += 1
        return "http://makeameme.org/character/" + meme_name + '/' + str(self.current_page_index[meme_name])









    ########################################################################################################################
    ###################[ --- Getting Memes --- ]############################################################################
    ########################################################################################################################

    # Function: parse
    # ---------------
    # gets called on the main pages that have thumbnails
    def parse (self, response):

        ### Step 1: get the meme_type ###
        meme_type = response.meta['meme_type']

        ### Step 2: get an xpath selector for this entire page ###
        hxs = HtmlXPathSelector(response)
        
        ### Step 3: get urls to the individual memes ###
        meme_urls_xpath = '//div[@class="freepin"]/a/@href'
        meme_urls = hxs.select (meme_urls_xpath).extract ()

        ### Step 4: generate requests for each of the individual memes ###
        requests = []
        for meme_url in meme_urls:
            full_url = 'http://makeameme.org' + meme_url
            requests.append (Request(url=full_url, meta={'meme_type':meme_type}, callback=self.parse_meme_page))

        ### Step 5: generate a request for the next page of memes ###
        requests.append (Request(url=self.get_next_page_url(meme_type), meta={'meme_type':meme_type}))


        return requests


    # Function: parse_meme_page
    # -------------------------
    # parses a page dedicated to a specific meme
    def parse_meme_page (self, response):
        
        print_status ("Spider", "Parse meme Page")

        meme_type = response.meta['meme_type']

        hxs = HtmlXPathSelector (response)
        title_xpath = "//title/text()"
        title = hxs.select (title_xpath).extract ()[0]

        splits = title.split('-')
        top_text = splits[0]
        bottom_text = splits [1]
        
        meme_item = Meme_Item ()
        meme_item['meme_type'] = meme_type
        meme_item['top_text'] = top_text
        meme_item['bottom_text'] = bottom_text
        self.meme_counts[meme_type] += 1

        return meme_item












