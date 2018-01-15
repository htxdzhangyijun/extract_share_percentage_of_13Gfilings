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
			paragraphs = re.findall(r'\d+\.\d+%|\d+%|\.\d+%', b, re.IGNORECASE)
			if len(paragraphs) == 0:
				paragraphs = re.findall(r'\d+\.\d+|\.\d+', b, re.IGNORECASE)
				paragraphs = [z + "%" for z in paragraphs]
			p = re.findall(r'inexcessof(\d+\.\d+%|\d+%|\.\d+%)oftheoutstanding', b, re.IGNORECASE)
			if len(p) == 1:
				paragraphs = [x for x in paragraphs if x != p[0]]
			return paragraphs
		###if there are tags in html###	
		else:
			content1 = htmlcon(self.html)
			Hold = content1.read_html2().decode('utf-8')
			Hold1 = strip_tags(Hold)
			a = "".join(line.strip() for line in Hold1)

		
			paragraphs2 = re.findall(r'Item4(.*?)\(c\)', a, re.IGNORECASE)
			b = "".join(line.strip() for line in paragraphs2)
			paragraphs = re.findall(r'\d+\.\d+%|\d+%|\.\d+%', b, re.IGNORECASE)
			if len(paragraphs) == 0:
				paragraphs = re.findall(r'\d+\.\d+|\.\d+', b, re.IGNORECASE)
				paragraphs = [z + "%" for z in paragraphs]
			p = re.findall(r'inexcessof(\d+\.\d+%|\d+%|\.\d+%)oftheoutstanding', b, re.IGNORECASE)
			if len(p) == 1:
				paragraphs = [x for x in paragraphs if x != p[0]]
			return paragraphs
	
	###find percentage with no patterns###		
	def re_find_data_nopattern(self):
		content1 = htmlcon(self.html)
		Hold = content1.read_html2().decode('utf-8')

		if re.search(r'\<html\>', Hold, re.IGNORECASE) is None:
			Hold1 = Hold.split()
			a = " ".join(line.strip() for line in Hold1)

			paragraphs = re.findall(r'\d+\.\d+%|\d+%|\.\d+%', a, re.IGNORECASE)
			p = re.findall(r'inexcessof(\d+\.\d+%|\d+%|\.\d+%)oftheoutstanding', a, re.IGNORECASE)
			if len(p) == 1:
				paragraphs = [x for x in paragraphs if x != p[0]]
			return paragraphs
		###if there are tags in html###	
		else:
			content1 = htmlcon(self.html)
			Hold = content1.read_html2().decode('utf-8')
			Hold1 = strip_tags(Hold)
			Hold2 = Hold1.split()
			a = " ".join(line.strip() for line in Hold2)


			paragraphs = re.findall(r'\d+\.\d+%|\d+%|\.\d+%', a, re.IGNORECASE)
			p = re.findall(r'inexcessof(\d+\.\d+%|\d+%|\.\d+%)oftheoutstanding', a, re.IGNORECASE)
			if len(p) == 1:
				paragraphs = [x for x in paragraphs if x != p[0]]
			return paragraphs	
			
			
	###find percentage without % signs but with percentage###
	###some percentage without % and also doesn't show in the pattern(between item 4 and (c))###
	###I extract them from the new pattern which comes from the whole article###
	###but with INROW9 in front###		
	def re_find_data_with_percentage_character(self):
		content1 = htmlcon(self.html)
		Hold = content1.read_html2().decode('utf-8')
		###if there is no tag in html###	
		if re.search(r'\<html\>', Hold, re.IGNORECASE) is None:
			a = "".join(line.strip() for line in Hold)
			paragraphs2 = re.findall(r'Item4(.*?)\(c\)', a, re.IGNORECASE)
			b = "".join(line.strip() for line in paragraphs2)
			paragraphs = re.findall(r'(\d+\.\d+|\d+|\.\d+)percent', b, re.IGNORECASE)
			###extract the number after INROW9###
			if len(paragraphs) == 0:
				paragraphs = re.findall(r'INROW9(\d+\.\d+|\d+|\.\d+)', a, re.IGNORECASE)
				if len(paragraphs) == 0:
					paragraphs = re.findall(r'INROW\(9\)(\d+\.\d+|\d+|\.\d+)', a, re.IGNORECASE)
					###check as below###

					if len(paragraphs) != 0:
						for u in range(len(paragraphs)):
							if len(paragraphs[u]) >= 2:
								if paragraphs[u][-1] == "2" and paragraphs[u][-2] == "1": 
									paragraphs = []
									break	

				###check whether the first number of each element is 0###
				###if the last two numbers are 1 and 2###
				###it means the number after row9(without %) could be linked with the following numbers###
				###which can make the number not eccuate###
				else:
					for o in range(len(paragraphs)):
						if len(paragraphs[o]) >= 2:
							if paragraphs[o].strip()[-1] == "2" and paragraphs[o].strip()[-2] == "1":
								paragraphs = []
								break

			paragraphs = [z + "%" for z in paragraphs]
			p = re.findall(r'inexcessof(\d+\.\d+%|\d+%|\.\d+%)oftheoutstanding', b, re.IGNORECASE)
			if len(p) == 1:
				paragraphs = [x for x in paragraphs if x != p[0]]
			return paragraphs
		###if there are tags in html###	
		else:
			content1 = htmlcon(self.html)
			Hold = content1.read_html2().decode('utf-8')
			Hold1 = strip_tags(Hold)
			a = "".join(line.strip() for line in Hold1)

		
			paragraphs2 = re.findall(r'Item4(.*?)\(c\)', a, re.IGNORECASE)
			b = "".join(line.strip() for line in paragraphs2)
			paragraphs = re.findall(r'(\d+\.\d+|\d+|\.\d+)percent', b, re.IGNORECASE)
			###extract the number after INROW9###
			if len(paragraphs) == 0:
				paragraphs = re.findall(r'INROW9(\d+\.\d+|\d+|\.\d+)', a, re.IGNORECASE)
				if len(paragraphs) == 0:
					paragraphs = re.findall(r'INROW\(9\)(\d+\.\d+|\d+|\.\d+)', a, re.IGNORECASE)
					###check as below###

					if len(paragraphs) != 0:
						for u in range(len(paragraphs)):
							if len(paragraphs[u]) >= 2:
								if paragraphs[u][-1] == "2" and paragraphs[u][-2] == "1": 
									paragraphs = []
									break	

				###check whether the first number of each element is 0###
				###if the last two numbers are 1 and 2###
				###it means the number after row9(without %) could be linked with the following numbers###
				###which can make the number not eccuate###
				else:
					for o in range(len(paragraphs)):
						if len(paragraphs[o]) >= 2:
							if paragraphs[o].strip()[-1] == "2" and paragraphs[o].strip()[-2] == "1":
								paragraphs = []
								break

			paragraphs = [z + "%" for z in paragraphs]
			p = re.findall(r'inexcessof(\d+\.\d+%|\d+%|\.\d+%)oftheoutstanding', b, re.IGNORECASE)
			if len(p) == 1:
				paragraphs = [x for x in paragraphs if x != p[0]]
			return paragraphs		
	
	###the find_data_function for check_function### 
	###expand the keywords range from "item4 to (c)" to "item4 to Item 5"###
	###than extract the percentage between the keywords###		
	def check_function_find_data(self):
		content1 = htmlcon(self.html)
		Hold1 = content1.read_html2().decode('utf-8')
		if re.search(r'\<html\>', Hold1, re.IGNORECASE) is None:
			a = "".join(line.strip() for line in Hold1)
			###expand the keywords range from "item4 to (c)" to "item4 to Item 5"###
			###than extract the percentage between the keywords###
			paragraphs2 = re.findall(r'Item4(.*?)Item5', a, re.IGNORECASE)
			b = "".join(line.strip() for line in paragraphs2)
			paragraphs = re.findall(r'\d+\.\d+%|\d+%|\.\d+%', b, re.IGNORECASE)
			p = re.findall(r'inexcessof(\d+\.\d+%|\d+%|\.\d+%)oftheoutstanding', b, re.IGNORECASE)
			if len(p) == 1:
				paragraphs = [x for x in paragraphs if x != p[0]]
			###check if there is some keywords between item4 and (c) that represent###
			###percentage is the sum of all the percentages###
			###the keword that I found is: in the aggregate###
			###example: https://www.sec.gov/Archives/edgar/data/101984/0000910643-00-000009.txt###
			
			aggregate_per1 = re.findall(r'Item4(.*?)\(c\)', a, re.IGNORECASE)
			c = "".join(line.strip() for line in aggregate_per1)	
			aggregate_per = re.findall(r'(intheaggregate)', c, re.IGNORECASE)
			if len(aggregate_per) != 0:
				###strip % out of numbers###		
				d = [str(paragraphs[p]).strip('%') for p in range(len(paragraphs))]
				###change the type in list###
				float_aggregate_per = [float(d[p]) for p in range(len(d))]
				paragraphs1 = [str(max(float_aggregate_per))]
				paragraphs = [z + "%" for z in paragraphs1]
			return paragraphs

		else:
			content1 = htmlcon(self.html)
			Hold = content1.read_html2().decode('utf-8')
			Hold1 = strip_tags(Hold)
			a = "".join(line.strip() for line in Hold1)

		
			paragraphs2 = re.findall(r'Item4(.*?)Item5', a, re.IGNORECASE)
			b = "".join(line.strip() for line in paragraphs2)
			paragraphs = re.findall(r'\d+\.\d+%|\d+%|\.\d+%', b, re.IGNORECASE)
			p = re.findall(r'inexcessof(\d+\.\d+%|\d+%|\.\d+%)oftheoutstanding', b, re.IGNORECASE)
			if len(p) == 1:
				paragraphs = [x for x in paragraphs if x != p[0]]
				
			aggregate_per1 = re.findall(r'Item4(.*?)\(c\)', a, re.IGNORECASE)
			c = "".join(line.strip() for line in aggregate_per1)	
			aggregate_per = re.findall(r'(intheaggregate)', c, re.IGNORECASE)
			if len(aggregate_per) != 0:
				###strip % out of numbers###		
				d = [str(paragraphs[p]).strip('%') for p in range(len(paragraphs))]
				###change the type in list###
				float_aggregate_per = [float(d[p]) for p in range(len(d))]
				paragraphs1 = [str(max(float_aggregate_per))]
				paragraphs = [z + "%" for z in paragraphs1]
			return paragraphs	

		

		
				

