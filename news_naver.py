#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter

headers = { "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
ranking = 10
date = 20210604

def get_tags(text, ranking):
	spliter = Okt()
	nouns = spliter.nouns(text)
	nounsnot1 = [n for n in nouns if len(n) > 1]
	count = Counter(nounsnot1)
	return_list = []

	for n, c in count.most_common(ranking):
		temp = {'tag': n, 'count': c}
		return_list.append(temp)

	return return_list

def replace(text):
	sym = ['[',',','.',']',':','/', '^','|','&','*','-','–','%','=', '(',')','"',"'"]
	text = re.sub('','',text,0).strip()

	for i in sym:
		text =  text.replace(i,'')

	print(text)

def crawler(sid2, sid1, date):
	list = []
	page = 1
	num = 0
	page_num = 0

	while True:
		url = 'https://news.naver.com/main/list.nhn?mode=LS2D&sid2=' + str(sid2) + '&sid1=' + str(sid1) + '&mid=shm&date=' + str(date) + '&page=' + str(page)
		res = requests.get(url, headers=headers).text
		soup = BeautifulSoup(res, 'html.parser')      
        	
		title = soup.select('.type06_headline > li > dl > dt > a')
		title1 = soup.select('.type06 > li > dl > dt > a')

		last_page = page_num
		page_num = soup.select('.paging > strong')
		
		if last_page == page_num:
			break
		
		for i in range(len(title)):
			#replace(title[i].text)
			list.append(title[i].text)   
		for i in range(len(title1)):
		#replace(title[i].text)
			list.append(title1[i].text)
		page += 1
	
	tags = get_tags(' '.join(list), ranking)

	for tag in tags:
		num += 1
		noun = tag['tag']
		count = tag['count']
		print(f'{num}. ' + '{} {}'.format(noun, count))
	      
	print('총 페이지 : ' + str(page - 1))


#Politics(269, 100)
sid2_politics = 269
sid1_politics = 100
print("\nPolitics News") 
crawler(sid2_politics, sid1_politics, date)

#Economy(263, 101)
sid2_economy = 263
sid1_economy = 101
print("\nEconomy News") 
crawler(sid2_economy, sid1_economy, date)

#Society(257, 102)
sid2_society = 257
sid1_society = 102
print("\nSociety News") 
crawler(sid2_society, sid1_society, date)

#Culture(245, 103)
sid2_culture = 245
sid1_culture = 103
print("\nCulture News") 
crawler(sid2_culture, sid1_culture, date)

#World(322, 104)
sid2_world = 322
sid1_world = 104
print("\nWorld News") 
crawler(sid2_world, sid1_world, date)

#IT(230, 105)
sid2_IT = 230
sid1_IT = 105
print("\nIT News") 
crawler(sid2_IT, sid1_IT, date)

#Science(228, 105)
sid2_science = 228
sid1_science = 105
print("\nScience News") 
crawler(sid2_science, sid1_science, date)


#end
