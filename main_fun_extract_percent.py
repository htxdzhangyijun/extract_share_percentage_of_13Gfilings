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
from check_function1 import check_percentage_numbers
import math


csvfile1 = r'part1.csv'
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
			
			###extract logic: first, extract the percentage between item4 and (c)###
			###no matter is a number with % or without % or with "percentage"###
			###then extract the number after row9, because row 9 always represent###
			###shares so in this way can extract share percentage###
			###then, extract all the numbers with %. Through selection in main_fun###
			###choose the best way to calculate the percentage of shares###
			###at last check whether the percentage we have is too small(small than 5%)###
			###whether need to add up all the percentages###
			
			###reason why extract number after row9 first: always useful percentage###
			###is after row9, so it is more efficient to extract numbers after row9###
			###than simply extract percentage numbers###
			if len(words2) == 0:
				words2 = words1.re_find_data_with_percentage_character()
				if len(words2) == 0:		
					words2 = words1.re_find_data_nopattern()
					if len(words2) == 0:
						words2 = ["0.00%"]
			results.append(words2)

	return results

allpercent = search_all_percentage()


per_fin1 = []	
def main_function():
	for i in range(len(allpercent)):
		###judge if len(allpercent) is 1. if 1, means that is the only number we want,###
		###get rid of the percentage which is too big(bigger than 77.1% is abonormal)###	
		if len(allpercent[i]) == 1:
			a = "".join(line.strip() for line in allpercent[i])
			
			try:
				results_withoutpercent = float(a.strip('%'))
			
				if results_withoutpercent < 77.1:
					per_fin1.append(allpercent[i])
				else:
					per_fin1.append(["0.00%"])
			###if there is an error, give an specific percentage to make###
			###it can be identified and keep the program going###
			###i choose 77% to be the error code###
			except ValueError:
				per_fin1.append(["77.00%"])		
			
		###judge if len(allpercent) is between 2 to 4, means that the result could be the combination###
		###of adding up them###
		
		###The first alogrithm is not 100% accurate to identify when to###
		###sum all the percentage and when to choose the max percentage###
		###I use length of allpercent to distinguish between each other###
		###I divided them by 1, (2,4), (5, infi).###
		###This means that we only can extract correctly if there are only###
		###2, 3, 4 share holders. If the share holders are too much, we may###
		###wrongly see them as the part of the biggest share holders###
		###in this way, I would like to make another alogrithm to check if other parts###
		###added up together equal to the max one. If it eqauls, means we should extract the###
		###largest one###
		
		if 3 <= len(allpercent[i]) < 5:
			###get the unique number in list###
			c = []
			for t in range(len(allpercent[i])):
				if allpercent[i][t] not in c:
					c.append(allpercent[i][t])			
			###strip % out of numbers###		
			b = [str(c[p]).strip('%') for p in range(len(c))]
			
			###if there is an error, give an specific percentage to make###
			###it can be identified and keep the program going###
			###i choose 77% to be the error code###
			
			try: 
			
				###change the type in list###
				float_percentage = [float(b[p]) for p in range(len(b))]		
				###get rid of the percentage which is too big(bigger than 77.1% is abonormal)###	
				float_percentage1 = [x for x in float_percentage if x < 77.1]
				###sum the list###
				sum_percentage = [sum(float_percentage1)]
				###make the float type come back to string###
				sum_percentage1 = [str(sum_percentage[p]) for p in range(len(sum_percentage))]
				###add % back to each string###
				sum_percentage2 = [z + "%" for z in sum_percentage1]
				
			except ValueError:
				sum_percentage2 = ["77.00%"]
			per_fin1.append(sum_percentage2)
		
		
		###considering I can't make sure how to deal with the situation that###
		###if 3 or more people share the same shares, so I make length(2, 4) use the old alogrithm###
		###I don't think 3 or 4 different people will share the same shares and they represent###
		###different investors. So I use the old one to help distinguish###
		if len(allpercent[i]) == 2 or len(allpercent[i]) > 4:
			b = [str(allpercent[i][p]).strip('%') for p in range(len(allpercent[i]))]
			###if there is an error, give an specific percentage to make###
			###it can be identified and keep the program going###
			###i choose 77% to be the error code###
	
			try:
				float_percentage = [float(b[p]) for p in range(len(b))]
				###get rid of the percentage which is too big(bigger than 77.1% is abonormal)###
				for y in range(len(float_percentage)):
					if float_percentage[y] > 77.1:
						float_percentage[y] = 0.00

					else:
						float_percentage[y] = float_percentage[y]
				###calculate max and sum of the list###
				max_float_percentage = max(float_percentage)
				sum_float_percentage = sum(float_percentage)
				rest_float_percentage = sum_float_percentage - max_float_percentage
				###the absolute value of the difference between rest_float_percentage and###
				###max_float_percentage should less than 0.01
				
				###this method also avoid the situiation that sometimes###
				###the same company would seperate their company and their accuate holder###
				###they both own the same portion of the shares but they just share the shares###
				###so we only need to calculate that one time(this only works when they report two people)###
				
				###I am thinking when they report 3 or more people share the same shares, what should I do?###
				
				###This situation happens, example: https://www.sec.gov/Archives/edgar/data/49146/0000912057-00-006810.txt###
				###I added up a check if to see if the sum of the percentage is abnormally big, I set the alert line###
				###to be 35. when accross the line, it will check if the every unique one is equal to each other###
				###if equal to equal to each other, means it is a report mistake or over 3 people share ths same shares###
				###of a company, they both stand for one investor###
				
				###I am considering if the character "aggregate", "share vote power" appears, we can choose the###
				###unique percentage###
				
				###the reason difference I choose is 0.6 is sometimes, we have###
				###example:6.4 changed to 6.5###		
				if math.fabs(rest_float_percentage - max_float_percentage) < 0.6:
					act_percentage1 = [str(max_float_percentage)]
					act_percentage = [z + "%" for z in act_percentage1]
				else:
					###if the sum of all the percentage is larger than 35###
					###then we make sure all the percentage is not the same###
					###all the shareholders don't represent one investor###
					###if they represent one, their share must be the same###
					###we only extract one of them###
					###if they are not the same, it means they don't represent only one investor###
					###we extract the sum of the percentage###
					
					if sum_float_percentage > 35:
						count1 = 0
						for i in range(len(float_percentage)):
							if math.fabs(float_percentage[i] - max_float_percentage) < 0.1:
								count1 += 1
							
						if (count1 / len(float_percentage)) > 0.9:
							act_percentage1 = [str(max_float_percentage)]
							act_percentage = [z + "%" for z in act_percentage1]
						else:
							act_percentage1 = [str(sum_float_percentage)]
							act_percentage = [z + "%" for z in act_percentage1]	
					###else, we still make the sum of all percentages###				
					else:
						act_percentage1 = [str(sum_float_percentage)]
						act_percentage = [z + "%" for z in act_percentage1]
				
			except ValueError:
				act_percentage = ["77.00%"]
			
			per_fin1.append(act_percentage)
		'''
		
		if 2 <= len(allpercent[i]) < 5:
			###get the unique number in list###
			c = []
			for t in range(len(allpercent[i])):
				if allpercent[i][t] not in c:
					c.append(allpercent[i][t])			
			###strip % out of numbers###		
			b = [str(c[p]).strip('%') for p in range(len(c))]
			
			###if there is an error, give an specific percentage to make###
			###it can be identified and keep the program going###
			###i choose 77% to be the error code###
			
			try: 
			
				###change the type in list###
				float_percentage = [float(b[p]) for p in range(len(b))]		
				###get rid of the percentage which is too big(bigger than 77.1% is abonormal)###	
				float_percentage1 = [x for x in float_percentage if x < 77.1]
				###sum the list###
				sum_percentage = [sum(float_percentage1)]
				###make the float type come back to string###
				sum_percentage1 = [str(sum_percentage[p]) for p in range(len(sum_percentage))]
				###add % back to each string###
				sum_percentage2 = [z + "%" for z in sum_percentage1]
				
			except ValueError:
				sum_percentage2 = ["77.00%"]
			per_fin1.append(sum_percentage2)
		###judge if len(allpercent) is larger than 6. It means this percentage could be###
		###made up by muliple percentages, take HTML = "https://www.sec.gov/Archives/edgar/data/1036325/0001036325-02-000021.txt"###
		###as example. So we need to choose the largest percentage of that###
		if len(allpercent[i]) >= 5:	
			###strip % out of numbers###		
			b = [str(allpercent[i][p]).strip('%') for p in range(len(allpercent[i]))]
			###if there is an error, give an specific percentage to make###
			###it can be identified and keep the program going###
			###i choose 77% to be the error code###
			try:
				###change the type in list###
				float_percentage = [float(b[p]) for p in range(len(b))]
				
				###get rid of the percentage which is too big(bigger than 77.1% is abonormal)###
				for y in range(len(float_percentage)):
					if float_percentage[y] > 77.1:
						float_percentage[y] = 0.00

					else:
						float_percentage[y] = float_percentage[y]

				###choose the max percentage of the list and put them back to str in list###

				max_percentage = max(float_percentage)
				max_percentage_str1 = [str(max(float_percentage))]
				max_percentage_str = [z + "%" for z in max_percentage_str1]				
				per_fin1.append(max_percentage_str)
			except ValueError:
				max_percentage_str = ["77.00%"]
				per_fin1.append(max_percentage_str)
				
				
		'''
	###make the element in per_fin become a string instead of list###
	per_fin = []
	for i in range(len(per_fin1)):
		item1 = per_fin1[i][0]
		per_fin.append(item1)



	###check the percentage which is less than 5% is right or wrong because###
	###sometimes the percentages were not been added up###
	
	###strip % out of numbers###		
	per_fin_no_percentage = [str(per_fin[p]).strip('%') for p in range(len(per_fin))]
	###change the type in list###
	float_per_fin = [float(per_fin_no_percentage[p]) for p in range(len(per_fin_no_percentage))]
	for q in range(len(float_per_fin)):
	
		###skip 0 when check the percentage, as 0.00% always happens as###
		###there is the percentage of share is 0.00% in the filings, so###
		###there is no need to check### 
		###unfortunately, I need to check 0.00%(sad face)###
		###example: "https://www.sec.gov/Archives/edgar/data/1035917/0001035917-99-000011.txt"###

		if 0 <= float_per_fin[q] < 5:
			htmlcheck1 = sorted_url[q]
			if htmlcheck1 == "0":
				per_fin[q] = per_fin[q]
			else:
				small_percentage1 = check_percentage_numbers(htmlcheck1)
				small_percentage = small_percentage1.check_find_data()
				if small_percentage[0] == "B":
					per_fin[q] = per_fin[q]
				
				else:
					per_fin[q] = small_percentage[0]


	return per_fin

newlist1 = main_function()


dict1 = dict(Percentage1 = newlist1)

fin_result1 = pd.DataFrame.from_dict(dict1, orient = 'index')
fin_result = fin_result1.T

print(fin_result)		



'''
fin_result.to_csv('part1_percentage_of_shares_two_year.csv')
'''	
			
			
			
			
			
			
###there are some filing that I can't extract properly###
###take this one as an example: https://www.sec.gov/Archives/edgar/data/860749/0000935836-00-000298.txt###
###in this one, the company first filed the whole percentage of two shareholders: 11.4% and 10.7%###
###then inside of each shareholder, the share was divided by two groups, one hold 2% of 10.7% and the other hold 8.7% if 10.7%###
###meanwhile, there is another group hold the 11.4%###
###this situation is complicated, and I only saw 1 example until now, so I don't think it is necessary to add this part###
###in the alogrithm. But, for accuarcy, when time permits, I would add it in my function###
###I have checked the file, it seems hard to find the pattern in that###


###I come up an idea for this one: we can add another if when make this choice "if (count1 / len(float_percentage)) > 0.9:"###
###i can check if there are some percentages that added up equal to one percentage. if this happens, we can check the keywords###
###whether the holders have some connections




		
			
			
			
			
			
			
