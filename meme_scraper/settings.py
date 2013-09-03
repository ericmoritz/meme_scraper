# Scrapy settings for meme_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'meme_scraper'

SPIDER_MODULES = ['meme_scraper.spiders']
NEWSPIDER_MODULE = 'meme_scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'meme_scraper (+http://www.yourdomain.com)'

#item pipeline
ITEM_PIPELINES = [
	'meme_scraper.pipelines.MemeScraperPipeline'
]