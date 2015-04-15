# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E5012_GLBC_gov"
url = "http://www.royalgreenwich.gov.uk/downloads/200110/council_budgets_and_spending"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
pageLinks = soup.findAll('a')

for pageLink in pageLinks:
  pageUrl = pageLink['href']
  if ('500_csv') in pageUrl:
  	# add the right prefix onto the url
  	title = pageLink.contents[0]
  	html2 = urllib2.urlopen(pageUrl)
	soup2 = BeautifulSoup(html2)
	fileLinks = soup2.find('h3',{'class':'downloadNow'})
	
	for fileLink in fileLinks:
		fileUrl = fileLink['href']
		title = title.upper().strip()
		csvMth = title.split(' ')[0][:3]
		csvMth = convert_mth_strings(csvMth);

		if ' TO ' in title: #  then we've got a quarterly file
			csvYr = title.split(' ')[3]
			filename = "Qfile_" + entity_id + "_" + csvYr + "_" + csvMth
		else:
			csvYr = title.split(' ')[1]
			if 'PAYMENTS' in csvYr:
				csvYr = '2013' # adjust for April 2013 file which doesn't have a year.
			filename = entity_id + "_" + csvYr + "_" + csvMth
		
		
		todays_date = str(datetime.now())
		scraperwiki.sqlite.save(unique_keys=['l'], data={"l": fileUrl, "f": filename, "d": todays_date })
		print filename
		
