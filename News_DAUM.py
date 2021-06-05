#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import json
import pprint
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter
from elasticsearch import Elasticsearch

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


def crawler(category, date):
    list = []
    data = []
    page = 1
    count_news = 0   
    num = 0   

    while True:
        url = 'https://news.daum.net/breakingnews/' + category + \
            '?page=' + str(page) + '&regDate=' + str(date)
        res = requests.get(url, headers=headers).text
        soup = BeautifulSoup(res, 'html.parser')

        title = soup.select('ul > li > div > strong > a')
        lastpage_check = soup.select('p')

        if len(lastpage_check) == 1:
            break

        for i in range(len(title)):           
            count_news += 1
            data.append({
                '1.Platform': "다음",
                '2.Category': category + '뉴스',
                '3.Title': title[i].text,               
                '4.Url': title[i]['href'],
                '5.Date': date,
                '6.Number': count_news
            })
            list.append(title[i].text)

        page += 1

    tags = get_tags(' '.join(list), 10)

    for tag in tags:
        num += 1
        noun = tag['tag']
        count = tag['count']
        print(f'{num}.' + '{} {}'.format(noun, count))

    with open('Data[' + category + '].json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent='\t', ensure_ascii=False)

    print('총 페이지 : ' + str(page - 1))

def check_index():
   return es.indices.get_alias("*")

def create_index(mapping_json):	
	if not es.indices.exists(index=index):
		with open(mapping_json, 'r', encoding='utf-8') as f:
			mapping = json.load(f)
		res = es.indices.create(index=index, body = mapping)
		
		return res

def delete_index():
	if es.indices.exists(index=index):
		return es.indices.delete(index=index)

def insert(doc_json):
	with open(doc_json, 'r', encoding='utf-8') as f:
		json_data = json.load(f)
	
	for i in json_data:
		res = es.index(index=index, body=i)
	
	return res

def search(keyword=None):
	body = {
		"query": {
			"match": {
				"3.Title" : keyword				
				}
		}
	}
	res = es.search(index=index, body=body, request_timeout= 30)

	return res

if __name__ == '__main__':
   headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
   url_elastic = '127.0.0.1'
   port = '9200'
   index = 'news'
   mapping_json = 'mapping_nori.json'
   categories = ['society', 'politics', 'economic', 'foreign', 'culture', 'entertain', 'digital']
   date = 20210605
   
   es = Elasticsearch(f'{url_elastic}:{port}')

   #for category in categories:
      #print('\n'+ category + ' 뉴스')
      #crawler(category, date)
        
   #delete_index()
   #create_index(mapping_json)

   #for category in categories:
      #insert('Data[' + category + '].json')

   r = search("코로나")
   pprint.pprint(r)





