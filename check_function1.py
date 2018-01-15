from urllib.request import urlopen
import urllib.request
import urllib.error
import bs4 as bs
import re
from htmlparser import MLStripper
import pandas as pd
from read_html1 import htmlcon
from read_html1 import strip_tags
from re_find_data import percentage_numbers

class check_percentage_numbers():
	def __init__(self, html):
		self.html = html
	###function to check those percentage which is less than 5%###
	###make sure there is no need to add the percentage up###
	def check_find_data(self):
		percentage_check1 = percentage_numbers(self.html)		
		percentage_check = percentage_check1.check_function_find_data()
		###strip % out of numbers###		
		b = [str(percentage_check[p]).strip('%') for p in range(len(percentage_check))]
		###change the type in list###
		float_percentage = [float(b[p]) for p in range(len(b))]
		
		###check if all the percentage is larger than 0, only percentage larger than 0 is useful###
		###if the number of useful percentage is larger 3###
		###then need to be added up###
		percentage_check2 = [m for m in float_percentage if m != 0]	
		
		if len(percentage_check2) >= 3:
	
			###get rid of the percentage which is too big(bigger than 61% is abonormal)###	
			float_percentage1 = [x for x in percentage_check2 if x < 61]
			###sum the list###
			sum_percentage = [sum(float_percentage1)]
			###make the float type come back to string###
			sum_percentage1 = [str(sum_percentage[p]) for p in range(len(sum_percentage))]
			###add % back to each string###
			sum_percentage2 = [z + "%" for z in sum_percentage1]
		else:
			sum_percentage2 = "B"
			
		return sum_percentage2


