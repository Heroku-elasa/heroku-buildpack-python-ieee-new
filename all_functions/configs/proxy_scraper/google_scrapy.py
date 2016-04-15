'''
Example of Scrapy spider used for scraping the google url.
Not actual running code.
'''
import re
import os
import sys
import json

from scrapy.spider import Spider
from scrapy.selector import Selector

class GoogleSearch(Spider):

 #set the search result here
 name = 'Google search'
 allowed_domains = ['www.google.com']
 start_urls = ['Insert the google url here']

 def parse(self, response):

 sel = Selector(response)
 google_search_links_list = sel.xpath('//h3/a/@href').extract()
 google_search_links_list = [re.search('q=(.*)&sa',n).group(1) for n in google_search_links_list]

## Dump the output to json file
 with open(output_j_fname, "w") as outfile:
 json.dump({'output_url':google_search_links_list}, outfile, indent=4)
