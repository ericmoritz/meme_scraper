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

# Class: DiyLolSpider
# -----------------
# spider to crawl through quickmeme and scrape text from advice animals.
# currently only scrapes meme types that are hard-coded in.
class DiyLolSpider (MemeSpider):

    #--- Scraper Identity ---
    name = "diylol"
    allowed_domains = ["diylol.com"]


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

        return "http://www.diylol.com/meme-generator/" + meme_name + "/popular/"


    # Function: get_next_page_url
    # ---------------------------
    # given an htmlxpathselector, this will return an xpath to 
    # the next page. returns None if there are no more pages
    def get_next_page_url (self, hxs):

        next_page_url_xpath = '//a[@class="next_page"]/@href'
        result = hxs.select (next_page_url_xpath)
        if len(result) == 0:
            return None
        else:
            return 'http://www.diylol.com' + result[0].extract ()









    ########################################################################################################################
    ###################[ --- Page Parsing --- ]#############################################################################
    ########################################################################################################################

    # Function: parse
    # ---------------
    # this function will parse a hard-coded meme-type's page and extract
    # links to each individual meme instance's page.
    def parse (self, response):


        ### Step 1: get the meme_type ###
        meme_type = response.meta['meme_type']

        ### Step 3: get an xpath selector for this entire page ###
        hxs = HtmlXPathSelector(response)
        
        ### Step 4: get the 'image' tables ###
        image_divs_xpath = '//body//div[@class="img-w-txt-headers"]'
        image_divs = hxs.select (image_divs_xpath)

        ### Step 5: extract the top/bottom lines from them ###
        top_text_xpath      = './/h3[@class="post_line1"]/text()'
        bottom_text_xpath   = './/h3[@class="post_line2"]/text()' 

        meme_items = []
        for image_div in image_divs:

            top_text = ''
            bottom_text = ''

            ### Step 6: get the top/bottom text out, continue to the next iteration if its not entirely ascii ###
            try:
                top_text        = image_div.select (top_text_xpath).extract       ()[0].lower().strip().decode('ascii')
            except:
                continue
            try:
                bottom_text     = image_div.select (bottom_text_xpath).extract    ()[0].lower().strip().decode('ascii')
            except: 
                continue 

            meme_item = Meme_Item ()
            meme_item['meme_type'] = meme_type
            meme_item['top_text'] = top_text
            meme_item['bottom_text'] = bottom_text
            meme_items.append (meme_item)
            self.meme_counts[meme_type] += 1



        ### Step 7: return a request for the next page ###
        return_objects = []
        return_objects += meme_items
        next_page_url = self.get_next_page_url (hxs)
        if next_page_url != None:
            return_objects.append( Request (url=self.get_next_page_url(hxs), meta=response.meta))

        print "Length of return_objects: ", len(return_objects)

        return return_objects











