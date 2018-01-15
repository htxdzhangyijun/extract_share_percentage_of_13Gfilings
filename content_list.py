from urllib.request import urlopen
import urllib.request
import urllib.error
import bs4 as bs
import re
from htmlparser import MLStripper
import pandas as pd

from read_html1 import htmlcon
from read_html1 import strip_tags

class words:
	def __init__(self, html1):
		self.html1 = html1	
	def content_words(self):		
		content1 = htmlcon(self.html1)
		Hold = content1.read_html1().decode("utf-8")	
		Hnew1 = strip_tags(Hold)
		Hnew = re.split("\n+", Hnew1)

		words1 = []
		lines = [line.strip() for line in Hnew]
		for a in lines:
			for word in a.split(" "):
				words1.append(word)

		words1[:] = [word for word in words1 if word != '']

		return words1

