#!/usr/bin/python3
#-*- coding: utf-8 -*-

#특수문자 제거 함
#명사 분리 함
#word frequency 확인 함

import re
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter
#twitter = Twitter()
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

def get_tags(text, num):
	splitter = Okt()
	nouns = splitter.nouns(text)
	nouns1 = [n for n in nouns if len(n) > 1]
	count = Counter(nouns1)
	return_list = []
	for n, c in count.most_common(num):
		temp = {'tag':n, 'count':c}
		return_list.append(temp)
	return return_list

list_politics = []
list_economy = []
list_society = []
list_culture = []
list_world = []
list_IT = []
list_science = []
ranking = 10

#politics
print("Politics News\n")
url_politics = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=100&sid2=269"
res_politics = requests.get(url_politics, headers=headers).text
soup_politics = BeautifulSoup(res_politics, "html.parser")

politics_title1 = soup_politics.select('.type06_headline > li > dl > dt > a')
for i in range(len(politics_title1)):
	list_politics.append(politics_title1[i].text)
politics_title2 = soup_politics.select('.type06 > li > dl > dt > a')
for i in range(len(politics_title2)):
	list_politics.append(politics_title2[i].text)

tags = get_tags(' '.join(list_politics), ranking)
for tag in tags:
	noun = tag['tag']
	count = tag['count']
	print('{} {}\n'.format(noun, count))


#economy
print("Economy News\n")
url_economy = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=263"
res_economy = requests.get(url_economy, headers=headers).text
soup_economy = BeautifulSoup(res_economy, "html.parser")

economy_title1 = soup_economy.select('.type06_headline > li > dl > dt > a')
for i in range(len(economy_title1)):
	list_economy.append(economy_title1[i].text)
economy_title2 = soup_economy.select('.type06 > li > dl > dt > a')
for i in range(len(economy_title2)):
	list_economy.append(economy_title2[i].text)

tags = get_tags(' '.join(list_economy), ranking)
for tag in tags:
	noun = tag['tag']
	count = tag['count']
	print('{} {}\n'.format(noun, count))


#society
print("Society News\n")
url_society = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=102&sid2=257"
res_society = requests.get(url_society, headers=headers).text
soup_society = BeautifulSoup(res_society, "html.parser")

society_title1 = soup_society.select('.type06_headline > li > dl > dt > a')
for i in range(len(society_title1)):
	list_society.append(society_title1[i].text)
society_title2 = soup_society.select('.type06 > li > dl > dt > a')
for i in range(len(society_title2)):
	list_society.append(society_title2[i].text)

tags = get_tags(' '.join(list_society), ranking)
for tag in tags:
	noun = tag['tag']
	count = tag['count']
	print('{} {}\n'.format(noun, count))

#culture
print("Culture News\n")
url_culture = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=103&sid2=245"
res_culture = requests.get(url_culture, headers=headers).text
soup_culture = BeautifulSoup(res_culture, "html.parser")

culture_title1 = soup_culture.select('.type06_headline > li > dl > dt > a')
for i in range(len(culture_title1)):
	list_culture.append(culture_title1[i].text)
culture_title2 = soup_culture.select('.type06 > li > dl > dt > a')
for i in range(len(culture_title2)):
	list_culture.append(culture_title2[i].text)

tags = get_tags(' '.join(list_culture), ranking)
for tag in tags:
	noun = tag['tag']
	count = tag['count']
	print('{} {}\n'.format(noun, count))


#world
print("World News\n")
url_world = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=104&sid2=322"
res_world = requests.get(url_world, headers=headers).text
soup_world = BeautifulSoup(res_world, "html.parser")

world_title1 = soup_world.select('.type06_headline > li > dl > dt > a')
for i in range(len(world_title1)):
	list_world.append(world_title1[i].text)
world_title2 = soup_world.select('.type06 > li > dl > dt > a')
for i in range(len(world_title2)):
	list_world.append(world_title2[i].text)

tags = get_tags(' '.join(list_world), ranking)
for tag in tags:
	noun = tag['tag']
	count = tag['count']
	print('{} {}\n'.format(noun, count))


#IT
print("IT News\n")
url_IT = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
res_IT = requests.get(url_IT, headers=headers).text
soup_IT = BeautifulSoup(res_IT, "html.parser")

IT_title1 = soup_IT.select('.type06_headline > li > dl > dt > a')
for i in range(len(IT_title1)):
	list_IT.append(IT_title1[i].text)
IT_title2 = soup_IT.select('.type06 > li > dl > dt > a')
for i in range(len(IT_title2)):
	list_IT.append(IT_title2[i].text)

tags = get_tags(' '.join(list_IT), ranking)
for tag in tags:
	noun = tag['tag']
	count = tag['count']
	print('{} {}\n'.format(noun, count))


#science
print("Science News\n")
url_science = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=228"
res_science = requests.get(url_science, headers=headers).text
soup_science = BeautifulSoup(res_science, "html.parser")

science_title1 = soup_science.select('.type06_headline > li > dl > dt > a')
for i in range(len(science_title1)):
	list_science.append(science_title1[i].text)
science_title2 = soup_science.select('.type06 > li > dl > dt > a')
for i in range(len(science_title2)):
	list_science.append(science_title2[i].text)

tags = get_tags(' '.join(list_science), ranking)
for tag in tags:
	noun = tag['tag']
	count = tag['count']
	print('{} {}\n'.format(noun, count))


#end
