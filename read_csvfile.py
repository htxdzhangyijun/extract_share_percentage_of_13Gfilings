import csv
import re
import pandas as pd

class Index_Url:
	def __init__(self, csvfile1):
		self.csvfile1 = csvfile1
		
	def sort_indexurl(self):
		fields = ['EDGAR_LINK__']

		twoyear13GURL1 = pd.read_csv(self.csvfile1, skipinitialspace=True, usecols=fields,
			low_memory=False)
		
		twoyear13GURL = twoyear13GURL1.astype(str).values.tolist()

		urls = []
		for i in range(len(twoyear13GURL)):
			url = twoyear13GURL[i]
			url = ''.join(url)
			urls.append(url)
			
		return urls


	
	
	
	
	












