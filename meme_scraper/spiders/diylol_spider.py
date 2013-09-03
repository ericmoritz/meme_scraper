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
sys.path.append ('../../')  #base-level directory
from meme_types import meme_types


# Class: DiyLolSpider
# -----------------
# spider to crawl through quickmeme and scrape text from advice animals.
# currently only scrapes meme types that are hard-coded in.
class DiyLolSpider (BaseSpider):

    #--- Scraper Identity ---
    name = "diylol"
    allowed_domains = ["diylol.com"]
    start_urls = []

    #--- Directories ---
    data_directory      = '../../data/'     #directory where all data will be stored
    save_filename       = None              #filename for a specific 

    #--- on the list of advice animals we will be scraping... ---
    current_meme_name = ''
    data_directory = os.path.join(os.getcwd(), 'data/')
    captions_filename = ''

    #--- Data Parameters ---
    max_meme_instances = 5000

    #--- Data ---
    meme_types      = []                                 #list of meme_types         
    meme_counts     = defaultdict(lambda: 0)      #dict mapping meme_type -> number of instances gathered


    ########################################################################################################################
    ###################[ --- Constructor/Initialization/Destructor --- ]###################################################################
    ########################################################################################################################

    # Function: start_requests
    # ------------------------
    # returns a list of the initial requests for diylol
    def start_requests (self):
        requests = []
        for meme_type in self.meme_types:
            requests.append ( Request (self.get_meme_page_url(meme_type), meta={'meme_type':meme_type}) )
        return requests



    # Function: constructor
    # ---------------------
    # starts up selenium and begins the requests and makes the appropriate directories
    def __init__ (self):

        self.meme_types = meme_types
        print "##### Scraping Meme Types: #####"
        for meme_type in self.meme_types:
            print " " + meme_type

        
    # Function: destructor
    # --------------------
    # pickles all of the captions
    def __del__(self):

        ### Step 1: pickle all meme instances ###
        for meme_type in self.meme_types:
            print "---> Pickling " + meme_type
            self.pickle_meme_instances (meme_type)








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

        return return_objects











