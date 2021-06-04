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

def crawler(category):
    list = []
    page = 1  

    while True:
        url =  'https://news.daum.net/breakingnews/' + category +'?page=' + str(page)
        res = requests.get(url, headers=headers).text
        soup = BeautifulSoup(res, 'html.parser')      
        page += 1

        title = soup.select('ul > li > div > strong > a')
        lastpage_check = soup.select('p')

        if len(lastpage_check) == 1:
            break

        for i in range(len(title)):
            #replace(title[i].text)
            list.append(title[i].text)      

    tags = get_tags(' '.join(list), 10) 

    for tag in tags:
       noun = tag['tag']
       count = tag['count']
       print('{} {}'.format(noun, count))

    print('총 페이지 : ' + str(page))

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

#Society
print("\nSociety News") 
crawler('society')

#Politics
print("\nPolitics News") 
crawler('politics')

#Economic
print("\nEconomic News") 
crawler('economic')

#Foreign
print("\nForeign News") 
crawler('foreign')

#Culture
print("\nCulture News") 
crawler('culture')

#Entertain
print("\nEntertain News") 
crawler('entertain')

#IT
print("\nIT News") 
crawler('digital')