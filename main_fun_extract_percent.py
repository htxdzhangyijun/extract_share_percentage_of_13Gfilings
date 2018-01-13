from urllib.request import urlopen
import urllib.request
import urllib.error
import bs4 as bs
import re
from htmlparser import MLStripper
import pandas as pd
from read_csvfile import Index_Url
from read_html1 import htmlcon
from read_html1 import strip_tags
from re_find_data import percentage_numbers

csvfile1 = r'example3.csv'
csvfile2 = Index_Url(csvfile1)
csvfile = csvfile2.sort_indexurl()


sorted_url = []
for url in csvfile:
	if "nan" in url:
		url = "0" 
	sorted_url.append(url)

results = []

def search_all_percentage():
	for i in range(len(sorted_url)):
		html2 = sorted_url[i]
		if html2 == "0":
			results.append(['0.00%'])

		
		else:
			words1 = percentage_numbers(html2)
			words2 = words1.re_find_data()
			###judge if words2 is empty, if it is empty, means the file###
			###doesn't give us a pattern(not between item4 and (c))###
			###so we need to find all percentage results###
			###be careful, some files don't have seperate sign which means###
			###row 9 6.6% could turn out to be 96.6%, in order to avoid it###
			###need to give a space between each words(this can't work in###
			###pattern one, because we re.findall use the keywords without space### 
			if len(words2) == 0:
				words2 = words1.re_find_data_nopattern()
				if len(words2) == 0:
					words2 = "0.00%"
			results.append(words2)		
	return results

allpercent = search_all_percentage()


per_fin = []	
def main_function():
	for i in range(len(allpercent)):
		###judge if len(allpercent) is 1. if 1, means that is the only number we want,###
		###get rid of the percentage which is too big(bigger than 50% is abonormal)###	
		if len(allpercent[i]) == 1:
			a = "".join(line.strip() for line in allpercent[i])
			results_withoutpercent = float(a.strip('%'))
			
			if results_withoutpercent < 50:
				per_fin.append(allpercent[i])
			else:
				per_fin.append("0")
		###judge if len(allpercent) is between 2 to 4, means that the result could be the combination###
		###of adding up or unique of them###
		###get rid of the percentage which is too big(bigger than 50% is abonormal)###				
		if 2 <= len(allpercent[i]) <= 4:
			###get the unique number in list###
			c = []
			for t in range(len(allpercent[i])):
				if allpercent[i][t] not in c:
					c.append(allpercent[i][t])
			###strip % out of numbers###		
			b = [str(c[p]).strip('%') for p in range(len(c))]
			###change the type in list###
			float_percentage = [float(b[p]) for p in range(len(b))]
			###sum the list###
			sum_percentage = [sum(float_percentage)]
			###make the float type come back to string###
			sum_percentage1 = [str(sum_percentage[p]) for p in range(len(sum_percentage))]
			###add % back to each string###
			sum_percentage2 = [z + "%" for z in sum_percentage1]
			per_fin.append(sum_percentage2)
		###judge if len(allpercent) is larger than 5. It means this percentage could be###
		###made up by muliple percentages, take HTML = "https://www.sec.gov/Archives/edgar/data/1036325/0001036325-02-000021.txt"###
		###as example. So we need to choose the largest percentage of that###
		if len(allpercent[i]) >= 5:	
			###strip % out of numbers###		
			b = [str(allpercent[i][p]).strip('%') for p in range(len(allpercent[i]))]
			###change the type in list###
			float_percentage = [float(b[p]) for p in range(len(b))]
			###choose the max percentage of the list and put them back to str in list###
			###get rid of the percentage which is too big(bigger than 50% is abonormal)###
			max_percentage = max(float_percentage)
			if max_percentage < 50:
				max_percentage_str1 = [str(max(float_percentage))]
				max_percentage_str = [z + "%" for z in max_percentage_str1]
			else:
				max_percentage_str = ["0.00%"]
			per_fin.append(max_percentage_str)


	return per_fin

newlist = []
newlist1 = main_function()
for i in range(len(newlist1)):
	item1 = newlist1[i][0]
	newlist.append(item1)


dict1 = dict(Percentage1 = newlist)

fin_result1 = pd.DataFrame.from_dict(dict1, orient = 'index')
fin_result = fin_result1.T

print(fin_result)		



			
'''
fin_result.to_csv('percentage_of_shares_two_year.csv')
'''		
			
			
			
			
			
			
			
			
			
			
			
			
			
