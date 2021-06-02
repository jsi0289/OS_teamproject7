#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter

def get_tags(text, ntags=50):
    spliter = Okt()
    nouns = spliter.nouns(text)  
    nouns1 = [n for n in nouns if len(n) > 1]   
    count = Counter(nouns1)
    return_list = []

    for n, c in count.most_common(ntags):
        temp = {'tag': n, 'count': c}
        return_list.append(temp)

    return return_list

def replace(text):
    sym = ['[',',','.',']',':','/', '^','|','&','*','-','–','%','=', '(',')','"',"'"]
    text = re.sub('','',text,0).strip()

    for i in sym:
       text =  text.replace(i,'')

    print(text)

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

#Society

url_Society =  'https://news.daum.net/breakingnews/society'
res_Society = requests.get(url_Society, headers=headers).text
soup_Society = BeautifulSoup(res_Society, 'html.parser')
list_Society = []

title_Society = soup_Society.select('ul > li > div > strong > a')
print("Society News\n")   
for i in range(len(title_Society)):
     #replace(title_Society[i].text)
     list_Society.append(title_Society[i].text)

tags_Society = get_tags(' '.join(list_Society), 10)

for tag in tags_Society:
   noun = tag['tag']
   count = tag['count']
   print('{} {}'.format(noun, count))

#Politics

url_Politics =  'https://news.daum.net/breakingnews/politics'
res_Politics = requests.get(url_Politics, headers=headers).text
soup_Politics = BeautifulSoup(res_Politics, 'html.parser')
list_Politics = []

title_Politics = soup_Politics.select('ul > li > div > strong > a')
print("\nPolitics News\n")   
for i in range(len(title_Politics)):
     #replace(title_Politics[i].text)
     list_Politics.append(title_Politics[i].text)

tags_Politics = get_tags(' '.join(list_Politics), 10)

for tag in tags_Politics:
   noun = tag['tag']
   count = tag['count']
   print('{} {}'.format(noun, count))


#Economic

url_Economic =  'https://news.daum.net/breakingnews/economic'
res_Economic = requests.get(url_Economic, headers=headers).text
soup_Economic = BeautifulSoup(res_Economic, 'html.parser')
list_Economic = []
title_Economic = soup_Economic.select('ul > li > div > strong > a')
print("\nEconomic News\n")   
for i in range(len(title_Economic)):
     #replace(title_Economic[i].text)
     list_Economic.append(title_Economic[i].text)

tags_Economic = get_tags(' '.join(list_Economic), 10)

for tag in tags_Economic:
   noun = tag['tag']
   count = tag['count']
   print('{} {}'.format(noun, count))


#Foreign

url_Foreign =  'https://news.daum.net/breakingnews/foreign'
res_Foreign = requests.get(url_Foreign, headers=headers).text
soup_Foreign = BeautifulSoup(res_Foreign, 'html.parser')
list_Foreign = []

title_Foreign = soup_Foreign.select('ul > li > div > strong > a')
print("\nForeign News\n")   
for i in range(len(title_Foreign)):
     #replace(title_Foreign[i].text)
     list_Foreign.append(title_Foreign[i].text)

tags_Foreign = get_tags(' '.join(list_Foreign), 10)

for tag in tags_Foreign:
   noun = tag['tag']
   count = tag['count']
   print('{} {}'.format(noun, count))


#Culture

url_Culture =  'https://news.daum.net/breakingnews/culture'
res_Culture = requests.get(url_Culture, headers=headers).text
soup_Culture = BeautifulSoup(res_Culture, 'html.parser')
list_Culture = []

title_Culture = soup_Culture.select('ul > li > div > strong > a')
print("\nCulture News\n")   
for i in range(len(title_Culture)):
     #replace(title_Culture[i].text)
     list_Culture.append(title_Culture[i].text)

tags_Culture = get_tags(' '.join(list_Culture), 10)

for tag in tags_Culture:
   noun = tag['tag']
   count = tag['count']
   print('{} {}'.format(noun, count))


#Entertain

url_Entertain =  'https://news.daum.net/breakingnews/entertain'
res_Entertain = requests.get(url_Entertain, headers=headers).text
soup_Entertain = BeautifulSoup(res_Entertain, 'html.parser')
list_Entertain = []

title_Entertain = soup_Entertain.select('ul > li > div > strong > a')
print("\nEntertain News\n")   
for i in range(len(title_Entertain)):
     #replace(title_Entertain[i].text)
     list_Entertain.append(title_Entertain[i].text)

tags_Entertain = get_tags(' '.join(list_Entertain), 10)

for tag in tags_Entertain:
   noun = tag['tag']
   count = tag['count']
   print('{} {}'.format(noun, count))

  
#IT

url_IT =  'https://news.daum.net/breakingnews/digital'
res_IT = requests.get(url_IT, headers=headers).text
soup_IT = BeautifulSoup(res_IT, 'html.parser')
list_IT = []

title_IT = soup_IT.select('ul > li > div > strong > a')
print("\nIT News\n")   
for i in range(len(title_IT)):
     #replace(title_IT[i].text)
     list_IT.append(title_IT[i].text)

tags_IT = get_tags(' '.join(list_IT), 10)

for tag in tags_IT:
   noun = tag['tag']
   count = tag['count']
   print('{} {}'.format(noun, count))

