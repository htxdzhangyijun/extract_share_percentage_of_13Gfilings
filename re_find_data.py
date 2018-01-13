from urllib.request import urlopen
import urllib.request
import urllib.error
import bs4 as bs
import re
from htmlparser import MLStripper
import pandas as pd
from read_html1 import htmlcon
from read_html1 import strip_tags

class percentage_numbers():
	def __init__(self, html):
		self.html = html
	###find percentage with patterns(between item4 and (c))###
	def re_find_data(self):
		
		content1 = htmlcon(self.html)
		Hold = content1.read_html2().decode('utf-8')
		###if there is no tag in html###	
		if re.search(r'\<html\>', Hold, re.IGNORECASE) is None:
			a = "".join(line.strip() for line in Hold)

		
			paragraphs2 = re.findall(r'Item4(.*?)\(c\)', a, re.IGNORECASE)
			b = "".join(line.strip() for line in paragraphs2)
			paragraphs = re.findall(r'\d+.\d+%|\d+%', b, re.IGNORECASE)

			return paragraphs
		###if there are tags in html###	
		else:
			content1 = htmlcon(self.html)
			Hold = content1.read_html2().decode('utf-8')
			Hold1 = strip_tags(Hold)
			a = "".join(line.strip() for line in Hold1)

		
			paragraphs2 = re.findall(r'Item4(.*?)\(c\)', a, re.IGNORECASE)
			b = "".join(line.strip() for line in paragraphs2)
			paragraphs = re.findall(r'\d+.\d+%|\d+%', b, re.IGNORECASE)

			return paragraphs
	
	###find percentage with no patterns###		
	def re_find_data_nopattern(self):
		content1 = htmlcon(self.html)
		Hold = content1.read_html2().decode('utf-8')

		if re.search(r'\<html\>', Hold, re.IGNORECASE) is None:
			Hold1 = Hold.split()
			a = " ".join(line.strip() for line in Hold1)

			paragraphs = re.findall(r'\d+.\d+%|\d+%', a, re.IGNORECASE)

			return paragraphs
		###if there are tags in html###	
		else:
			content1 = htmlcon(self.html)
			Hold = content1.read_html2().decode('utf-8')
			Hold1 = strip_tags(Hold)
			Hold2 = Hold1.split()
			a = " ".join(line.strip() for line in Hold2)


			paragraphs = re.findall(r'\d+.\d+%|\d+%', a, re.IGNORECASE)

			return paragraphs	
			
			
			
			
			

