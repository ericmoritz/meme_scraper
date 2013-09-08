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
    name = "trollme"
    allowed_domains = ["troll.me"]


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

        return "http://troll.me/meme/" + meme_name + '/page/1'


    # Function: get_next_page_url
    # ---------------------------
    # given an htmlxpathselector, this will return an xpath to 
    # the next page. returns None if there are no more pages
    def get_next_page_url (self, meme_name):

        self.current_page_index[meme_name] += 1
        return "http://troll.me/meme/" + meme_name + '/page/' + str(self.current_page_index[meme_name]) + '/'









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
        alt_texts_xpaths = '//img[@class="apostimg"]/@alt'
        alt_texts = hxs.select (alt_texts_xpaths).extract()

        meme_items = []
        for alt_text in alt_texts:

            content = alt_text.split('-')[1].strip()
            splits = content.split(',')
            if len(splits) <= 1:
                continue
            top_text = splits[0]
            bottom_text = splits [1]

            meme_item = Meme_Item ()
            meme_item['meme_type'] = meme_type
            meme_item['top_text'] = top_text.lower ()
            meme_item['bottom_text'] = bottom_text.lower ()
            meme_items.append (meme_item)
            self.meme_counts[meme_type] += 1


         ### Step 7: return a request for the next page ###
        return_objects = []
        return_objects += meme_items
        next_page_url = self.get_next_page_url (meme_type)
        if next_page_url != None:
            return_objects.append( Request (url=next_page_url, meta=response.meta))

        return return_objects













 