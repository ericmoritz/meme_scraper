# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#--- Standard ---
import os
import sys
import pickle
from collections import defaultdict

#--- My Files ---
sys.path.append (os.path.join(os.getcwd(), '../'))  #base-level directory
from Meme import meme

class MemeScraperPipeline(object):

	#--- Instance Variables ---
	data_directory = os.path.join (os.getcwd(), '../data')
	memes = defaultdict(lambda: [])


	####################################################################################################
	###############[ --- Pickling Data ---]#############################################################
	####################################################################################################		

    # Function: get_pickle_filename
    # -----------------------------
    # given a meme name, this returns the name (full filepath) of the file where
    # you should pickle the list of all instances of it.
    def get_pickle_filename (self, meme_type):

        return os.path.join (self.data_directory, meme_type + '_instances.pkl')

    # Function: pickle_meme_instances
    # -------------------------------
    # pickles the list of all meme objects
    def pickle_meme_instances (self, meme_type):

        pickle_filename = self.get_pickle_filename (meme_type)
        pickle.dump (self.memes[meme_type], open(pickle_filename, 'w'))
        print '---> Pickler: pickled ' + meme_type + 'instances at ' + pickle_filename



	####################################################################################################
	###############[ --- Processing Items ---]##########################################################
	####################################################################################################		

    def process_item(self, item, spider):

    	### Step 1: construct meme object, append to appropriate list ###
    	new_meme = Meme (item['meme_type'], item['top_text'], item['bottom_text'])
    	self.memes[item['meme_type']].append (item['top_text'])


        return item
