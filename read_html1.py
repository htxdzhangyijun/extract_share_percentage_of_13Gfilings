from urllib.request import urlopen
import urllib.request
import urllib.error
import bs4 as bs
import re
from htmlparser import MLStripper

class htmlcon:
	def __init__(self, html1):
		self.html1 = html1
	def read_html2(self):
		hdr = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
				"X-Requested-With": "XMLHttpRequest",
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Referer': 'https://cssspritegenerator.com',
				'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
				'Accept-Encoding': 'none',
				'Accept-Language': 'en-US,en;q=0.8',
				'Connection': 'keep-alive'}
		

		
		req = urllib.request.Request(self.html1, headers=hdr)
		
		try:
			page = urlopen(req)
		except urllib.error.HTTPError as e:
			print (e.code)	
		contents_file = page.read()
		return contents_file

		
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
	

	
