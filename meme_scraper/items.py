# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


# class: Meme_Item
# ----------------
# Item class to contain all information relevant to a single meme;
# this will get converted into a Meme object in due time.
class MemeItem (Item):

	meme_type = Field ()
	top_text = Field ()
	bottom_text = Field ()

	pass