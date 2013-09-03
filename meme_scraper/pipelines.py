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
sys.path.append (os.path.join(os.getcwd(), '../'))  #base-level directory
from meme_types import meme_types

class MemeScraperPipeline(object):

	#--- Instance Variables ---
	data_directory = os.path.join (os.getcwd(), '../data')		# location of the data directory
	exporters = {}												# dict mapping meme_type -> exporters
	files = {}
	memes = defaultdict(lambda: [])								# dict mapping meme_type -> list of memes
	meme_types = []

	####################################################################################################
	###############[ --- Constructor/Destructor ---]################################################################
	####################################################################################################

	# Function: open_spider
	# ---------------------
	# gets called when spider is open (basically a constructor)
	def open_spider (self, spider):

		print "---> Pipeline: open_spider"
		self.meme_types = meme_types

		### Step 1: initialize the exporters ###
		print "---> Pipeline: initialize exporters"		
		self.initialize_exporters ()


	# Function: close_spider
	# ----------------------
	# gets called when the spider is closed (basically a destructor)
	def close_spider (self, spider):

		print "---> Pipelie: close_spider"

		### Step 1: finalize exporters ###
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

		print "---> Pipeline: process_item"
		meme_type = item['meme_type']
		self.exporters[meme_type].export_item (item)
		return item


    	### Step 1: construct meme object, append to appropriate list ###
    	# new_meme = Meme (item['meme_type'], item['top_text'], item['bottom_text'])
    	# self.memes[item['meme_type']].append (item['top_text'])
