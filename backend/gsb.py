import requests
import simplejson
import json 
import ast
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def func(url):
	API_KEY = "AIzaSyBYeZ1AhJxa0ztkbszupUIWQRgMviyr-Mw"
	url2="https://safebrowsing.googleapis.com/v4/threatLists?key="+API_KEY
	url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key="+API_KEY

	body =   {
	    "client": {
	      "clientId":      "sravs",
	      "clientVersion": "1.5.2"
	    },
	    "threatInfo": {
	      "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING","UNWANTED_SOFTWARE"],
	      "platformTypes":    ["ANY_PLATFORM"],
	      "threatEntryTypes": ["URL","IP_RANGE"],
	      "threatEntries": [
		{"url": url},
	      ]
	    }
	  }
	data_json = json.dumps(body)
	resp = requests.post(url,data=data_json)
	resp = (resp.content).strip("\n")
	resp = ast.literal_eval(resp)
	return resp

def netcraft2(url):
	print("here")
	s = requests.Session()
	netcraft_url = "https://toolbar.netcraft.com/site_report?url="+url
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


	#cookies = {'__utma':'126155282.1249371075.1552141998.1552211266.1556451393.3','__utma':'207282326.844698358.1552142103.1556503637.1556862580.10','__utmb':'207282326.6.10.1556862580','__utmc':'207282326','__utmt':'	1','netcraft_js_verification_challenge':'djF8bDUxMXZLRkErMytCTXNLQjc2N2dDZ21UdjBLeUVuOHQxaS9DYUtDTnJpNnZadlEzU21penNP%0AOXl1RWYwaGZ0a20zOUxNMGU3WXo4Mgp0VytvNWs3bEVRPT0KfDE1NTY4NjMxMTA%3D%0A%7C46fb59e1a43f699a91a6fba4389792039e55116c','netcraft_js_verification_response':'43bfc69c5d3d8a1803262a0be5a250f760ea5ab3'}
	
	page = s.get(netcraft_url,headers=headers)

	cookies = page.cookies
	print(cookies)
	page = s.get(netcraft_url,headers=headers,cookies=cookies)
	print(page.text)

	# soup = BeautifulSoup(page.text,'html.parser')
	resp = "Netcraft Risk Rating: 0/10 \n IP Address: 	103.210.73.254\n Domain Registar: godaddy.com	\n Date first seen: October 2015\n DNS Admin: dns@jomax.net\n Name server: ns55.domaincontrol.com"
	return resp


def netcraft_scan(url):
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome('/home/sravani/Web-Application-Security-Framework/backend/chromedriver',chrome_options=chrome_options)
	driver.get('https://toolbar.netcraft.com/site_report?url='+url)

	information = dict()
	soup = BeautifulSoup(driver.page_source,'html.parser')
	all_tables = soup.find_all("table",class_="TBtable")
	table_information = all_tables[0]
	background_details_1 = table_information.find_all("tr",class_=["TBtr","TBtr2"])
	information["Date first seen"] = background_details_1[0].find_all("td")[1].get_text()

	for tag in background_details_1:
		tag_headline = tag.find("th").get_text()
		if not tag.find("span"):
			continue
		information[tag_headline] = tag.find("span").get_text()

	background_details_2 = table_information.find_all("tr",class_="TBtr")
	print(background_details_2)
	site_rank = background_details_2[0].find_all("a")[0].get_text().strip("\n")
	primary_language = background_details_2[0].find_all("td")[1].get_text().strip("\n")
	information["Site rank"] = site_rank
	information["Primary language"] = primary_language
	
	network_table = all_tables[1]
	network_table_1 = network_table.find_all("tr",class_=["TBtr","TBtr2"])	

	for tag in network_table_1:
		tag_headline = tag.find("th").get_text()
		tag_info = tag.find("td").get_text()
		if tag.find("a"):
			tag_info = tag.find("a").get_text()
		if 'IP' in tag_headline:
			tag_info = tag.find("td").get_text()

		information[tag_headline] = tag_info

	hosting_history_table = all_tables[2]
	hosting_history_titles = hosting_history_table.find_all("tr",class_="TBtrtitle")
	hh_title_tags = hosting_history_titles[0].find_all("th")
	hosting_history_details = hosting_history_table.find_all("tr",class_=["TBtr","TBtr2"])
	hh_titles = []
	hh_details = ''

	for tag in hh_title_tags:
		hh_titles.append(tag.get_text())
	hh_details = ",".join(hh_titles)+"\n"
	
	for tr_tag in hosting_history_details:
		hh_information = []
		td_tags = tr_tag.find_all("td")
		for td in td_tags:
			a = td.find("a")
			if a:
				hh_information.append(a.get_text())
				continue
			hh_information.append(td.get_text())
		hh_details+=",".join(hh_information)+"\n"

	information["Hosting history"]=hh_details
	table_information = ''

	for key,value in information.items():
		key = key.replace("[FAQ]","")
		value = value.replace("(VirusTotal)","")
		table_information+=key
		table_information+="\n"
		table_information+=value
		table_information+="\n"
		table_information+="\n"
	table_information = table_information.encode('utf-8')
	print(table_information)
	return table_information