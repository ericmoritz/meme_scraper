# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#--- Standard ---
import os
import sys
import pickle
from collections import defaultdict

#--- Scrapy ---
from scrapy import signals
from scrapy.contrib.exporter import JsonItemExporter

#--- My Files ---
from spiders.common_utilities import print_welcome, print_message, print_error, print_status, print_inner_status


class MemeScraperPipeline(object):

	#--- Filenames ---
	base_directory 			= None
	data_directory 			= None

	#--- Data ---
	site_name = None
	exporters = {}									# dict mapping meme_type -> exporters
	files = {}										# list of json files
	memes = defaultdict(lambda: [])					# dict mapping meme_type -> list of memes
	meme_types = []



	####################################################################################################
	###############[ --- Constructor/Destructor ---]################################################################
	####################################################################################################

	# Function: initialize_values
	# ---------------------------
	# copies over values from the spider
	def initialize_values (self, spider):

		self.site_name 	= spider.name
		self.meme_types = spider.meme_types
		self.base_directory = spider.base_directory
		self.data_directory = spider.data_directory


	# Function: open_spider
	# ---------------------
	# gets called when spider is open (basically a constructor)
	def open_spider (self, spider):

		### Step 1: set meme_types and data_directory straight ###
		print_status ("Pipeline", "Initializing values")
		self.initialize_values (spider)

		### Step 2: initialize exporters ###
		print_status ("Pipeline", "Initializing exporters")
		self.initialize_exporters ()


	# Function: close_spider
	# ----------------------
	# gets called when the spider is closed (basically a destructor)
	def close_spider (self, spider):

		### Step 1: finalize exporters ###
		print_status ("Pipeline", "Finalize exporters")
		self.finalize_exporters ()






	####################################################################################################
	###############[ --- Data Storage/Exporation ---]###################################################
	####################################################################################################		

    # Function: get_json_filename
    # -----------------------------
    # given a meme name, this returns the name (full filepath) of the file where
    # you should export all instances of it
	def get_json_filename (self, meme_type):

		return os.path.join (self.data_directory, meme_type + '_instances.json')


	# Function: initialize_exporters
	# ------------------------------
	# initializes exporters for every meme type
	def initialize_exporters (self):

		for meme_type in self.meme_types:

			json_filename = self.get_json_filename (meme_type)
			json_file = open(json_filename, 'w')
			self.files[meme_type] = json_file
			self.exporters[meme_type] = JsonItemExporter (json_file)
			self.exporters[meme_type].start_exporting ()


	# Function: finalize_exporters
	# ------------------------------
	# finalizes exporters for every meme type
	def finalize_exporters (self):

		for meme_type in self.meme_types:
			self.exporters[meme_type].finish_exporting ()
			self.files[meme_type].close ()








	####################################################################################################
	###############[ --- Processing Items ---]##########################################################
	####################################################################################################		

	# Function: process_item
	# ----------------------
	# converts the item in to a Meme object, stores it
	def process_item(self, item, spider):

		print_status ("Pipeline", "Processing item")
		meme_type = item['meme_type']
		print item
		# self.exporters[meme_type].export_item (item)
		return item

