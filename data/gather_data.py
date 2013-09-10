#!/usr/bin/python
# ---------------------------------------------------------- #
# Script: gather_data.py
# ---------------------
# used for getting in memes of all types and combining into a 
# single directory
# ---------------------------------------------------------- #

#--- Standard ---
import os
import sys
import json

#--- Equivalent Meme Types ---
meme_types = {

	'matrix-morpheus':['matrix-morpheus'],
	'condescending-wonka':['willy-wonka-sarcasm-meme', 'condescending-wonka', 'creepy-willy-wonka', 'creepy-wonka'],
	'condescending-fox':['condescending-fox', 'condescending-wife'],
	'scumbag-stacy':['scumbag-girl'],
	'scumbag-steve':['scumbag-steve'],
	'seth-from-superbad':['seth-from-superbad', 'fuck-me-right-alternative-seth-from-superbad-meme'],
	'socially-awkward-awesome-penguin':['socially-awkward-awesome-penguin', 'socially-awksome-penguin', 'socially-awesome-awkward-penguin'],
	'socially-awkward-penguin':['socially-awkward-penguin'],
	'socially-awesome-penguin':['socially-awesome-penguin'],
	'forever-alone':['forever-alone', 'forever-alone-20'],
	'today-was-a-good-day':['today-was-a-good-day'],
	'xbox-one':['xbox-one'],
	'misunderstood-douchebag':['misunderstood-douchebag'],
	'successful-black-man':['successful-black-man'],
	'too-damn-high':['too-damn-high'],
	'game-of-thrones':['game-of-thrones', 'winter-is-coming', 'game-of-thrones-meme'],
	'serial-killer-george':['serial-killer-george'],
	'sheltered-suburban-kid':['sheltered-suburban-kid'],
	'captain-hindsight':['captain-hindsight', 'captian-hindsight'],
	'megyn-kelly':['megyn-kelly'],
	'good-guy-greg':['good-guy-greg', 'good-guy-greg-', 'good-guy-greg--9'],
	'challenge-accepted':['challenge-accepted'],
	'overly-manly-man':['overly-manly-man'],
	'am-i-the-only-one':['am-i-the-only-one'],
	'stoner-dog':['stoner-dog'],
	'gordon-ramsay':['gordon-ramsay'],
	'butthurt-dweller':['butthurt-dweller'],
	'angry-samuel-l-jackson':['angry-samuel-l-jackson'],
	'bill-o-reilly':['bill-oreilly', 'bill-o-reilly'], 
	'drunk-baby':['drunk-baby'],
	'courage-wolf':['courage-wolf'],
	'push-it-patrick':['push-it-patrick', 'push-it-somewhere-else-patrick'],
	'downvoting-roman':['downvoting-roman', 'downvoting-robot'],
	'pawn-star':['pawn-star'], 
	'business-cat':['business-cat', 'business-cat-needs'],
	'american-pride-eagle':['american-pride-eagle'],
	'10-guy':['guy', '10-guy'],
	'advice-god':['advice-god'],
	'bill-lumbergh':['that-would-be-great-office-space-bill-lumbergh'],
	'bad-luck-brian':['bad-luck-brian'],
	'the-most-interesting-man-in-the-world':['the-most-interesting-man-in-the-world'],
	'oblivious-suburban-mom':['oblivious-suburban-mom'],
	'skeptical-third-world-kid':['skeptical-third-world-kid'],
	'third-world-success':['dancing-black-kids', 'third-world-success', 'third-world-success-kid'],
	'boromir':['one-does-not-simply', 'boromir'],
	'dwight-schrute':['schrute-facts-dwight-schrute-from-the-office', 'dwight-schrute', 'schrute'],
	'sheltered-college-freshman':['sheltered-college-freshman'],
	'engineering-professor':['engineering-professor'],
	'redditors-wife':['redditors-wife'],
	'foul-bachelorette-frog':['foul-bachelorette-frog'],
	'foul-bachelor-frog':['foul-bachelor-frog'],
	'annoyed-picard':['annoyed-picard', 'picard-wtf'],
	'browser-troll-face':['browser-troll-face'],
	'college-freshman':['college-freshman'],
	'sudden-clarity-clarence':['sudden-clarity-clarence'],
	'scumbag-brain':['scumbag-brain'],
	'almost-politically-correct-redneck':['almost-politically-correct-redneck'],
	'tech-impaired-duck':['tech-impaired-duck', 'technologically-impaired-duck'],
	'what-grinds-my-gears':['what-grinds-my-gears', 'what-grinds-my-gears-family-guy'],
	'things-are-getting-pretty-serious':['things-are-getting-pretty-serious'],
	'slowpoke':['slowpoke'],
	'actual-advice-mallard':['actual-advice-mallard'],
	'malicious-advice-mallard':['malicious-advice-mallard'],
	'annoying-facebook-girl':['annoying-facebook-girl'],
	'ptsd-clarinet-boy':['ptsd-clarinet-boy'],
	'science-cat':['science-cat', 'chemistry-cat'],
	'scumbag-teacher':['scumbag-teacher', 'unhelpful-high-school-teacher'],
	'y-u-no':['y-u-no'],
	'pickup-line-panda':['pickup-line-panda'],
	'hawkward':['hawkward'],
	'sexually-oblivious-rhino':['sexually-oblivious-rhino'],
	'web-developer-walrus':['web-developer-walrus'],
	'internet-grandma':['internet-grandma', 'grandma-finds-the-internet'],
	'futurama-fry':['futurama-fry'],
	'ordinary-muslim-man':['ordinary-muslim-man'],
	'pepperidge-farm-remembers':['pepperidge-farm-remembers'],
	'first-world-problems':['first-world-problems'],
	'reddit-alien':['reddit-alien'],
	'tough-spongebob':['tough-spongebob-i-ll-have-you-know'],
	'scumbag-steve':['scumbag-steve'],
	'godfather-baby':['godfather-baby', 'baby-godfather'],
	'musically-oblivious-8th-grader':['musically-oblivious-8th-grader'],
	'joker':['everyone-loses-their-minds'],
	'philosoraptor':['philosoraptor'],
	'first-day-on-the-internet-kid':['first-day-on-the-internet-kid'],
	'hipster-barista':['hipster-barista', 'hipster-kitty', 'hipster-ariel'],
	'evil-plotting-raccoon':['evil-plotting-raccoon'],
	'sheltering-suburban-mom':['sheltering-suburban-mom'],
	'sad-keanu':['sad-keanu'],
	'buzz-and-woody':['buzz-and-woody-toy-story-meme', 'buzz-and-woody'],
	'fuck-this-shit':['fuck-this-shit-bill-murray'],
	'high-expectations-asian-father':['high-expectations-asian-father'],
	'bear-grylls':['bear-grylls', 'bear-grylls-survival-tactics'],
	'joseph-ducreux':['joseph-ducreux'],
	'paranoid-parrot':['paranoid-parrot'],
	'ancient-alens-guy':['ancient-alens-guy'],
	'overly-attached-girlfriend':['overly-attached-girlfriend', 'oag-s-overly-attached-girlfriend-s'],
	'insanity-wolf':['insanity-wolf'],
	'success-kid':['success-kid'],
	'milton-from-office-space':['milton-from-office-space'],
	'confession-bear':['confession-bear'],
	'conspiracy-keanu':['conspiracy-keanu'],
	'redneck-randal':['redneck-randal', 'redneck-randall'],
	'x-all-the-things':['x-all-the-things'],
	'confucius-says':['confucious-says', 'confucius-says'],
	'super-cool-ski-instructor':['super-cool-ski-instructor', 'bad-time'], 
	'rasta-science-teacher':['rasta-science-teacher'],
	'lazy-college-senior':['lazy-college-senior'],
	'ok-guy':['ok-guy'],
	'pedobear':['pedobear'],
	'aaand-its-gone':['aaand-its-gone'],
	'karate-kyle':['karate-kyle']
}



# Function: get_data_directories
# ------------------------------
# gets filepaths for all directories containing json files for the 
# respective sites
def get_data_directories ():
	
	return [d for d in os.listdir (os.getcwd ()) if os.path.isdir (d)]

# Function: get_meme_types 
# ------------------------
# returns list of all meme_types in a given data directory
def get_memes (data_directory):
	
	json_files =  [f for f in os.listdir (data_directory) if f[-4:] == 'json']

	memes = []
	for j in json_files:
		full_filename = os.path.join (data_directory, j)
		memes += json.loads (open(full_filename, 'r').read())
	return memes

# Function: get_all_meme_types
# ----------------------------
# returns a list of all of the meme types from all data directories
def get_all_memes (data_directories):

	memes = []
	for d in data_directories:

		memes += get_memes (d)
	return memes

# Function: mark_actual_type
# ------------------------
# given a meme, this marks its actual type
def mark_actual_type (meme, meme_types):

	marked_type = meme['meme_type']
	for actual_type, equivalents in meme_types.items():
		if marked_type in equivalents:
			meme['meme_type'] = actual_type

# Function: write_out_memes
# -------------------------
# writes out all memes to a json file
def write_out_memes (memes):

	outfile = open('all_memes.json', 'w')
	outfile.write (json.dumps(memes))
	outfile.close ()


if __name__ == "__main__":

	### Step 1: get all of the directories (non-py files) ###
	data_directories = get_data_directories ()

	### Step 2: get all memes ###
	memes = get_all_memes (data_directories)

	### Step 3: re-mark them ###
	for meme in memes:
		mark_actual_type (meme, meme_types)

	### Step 4: write them out to json files ###
	write_out_memes (memes)






