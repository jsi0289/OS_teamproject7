#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import json
import pprint
import datetime
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Okt
from collections import Counter
from elasticsearch import Elasticsearch

def get_tags(text, ranking): #특수문자 및 한 글자 제거
	spliter = Okt()
	nouns = spliter.nouns(text)
	nounsException = [word for word in nouns if not word in exception]
	nouns_not1 = [n for n in nounsException if len(n) > 1]

	count = Counter(nouns_not1)
	return_list = []

	for n, c in count.most_common(ranking):
		temp = {'tag': n, 'count': c}
		return_list.append(temp)

	return return_list

def crawler_naver(category, sid2, sid1, date): #웹 크롤링 후 결과를 JSON에 저장
	list_n = []
	data = []
	text_check = ""
	text_check1 = ""
	page_num = 0
	count_news = 0
	page = 1

	while True:
		url = 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid2=' + str(sid2) + '&sid1=' + str(sid1) + '&date=' + str(date) + '&page=' + str(page)
		res = requests.get(url, headers=headers_naver).text
		soup = BeautifulSoup(res, 'html.parser')      
        	
		title = soup.select('.type06_headline > li > dl > dt > a')
		title1 = soup.select('.type06 > li > dl > dt > a')

		last_page = page_num
		page_num = soup.select('.paging > strong')
		
		if (last_page == page_num) or page > 15:
			break
		
		for i in range(len(title)):
			if len(title[i].text) < 3:
				continue

			url_content = title[i]['href']
			res_content = requests.get(url_content, headers=headers_naver).text
			soup_content = BeautifulSoup(res_content, 'html.parser')
			content = soup_content.select('div > ._article_body_contents')

			if(not content):
				content = title

			text_split = title[i].text
			text_split = text_split.split()
			text_split = " ".join(text_split)

			if(text_split == '동영상기사'):
				continue
			
			if(text_check == text_split):
				continue

			text_check = text_split

			content_split = content[0].text
			content_split = content_split.split()
			content_split = " ".join(content_split)

			if(content_split[0:6] == "동영상 뉴스"):
				content_split = content_split[70:]
			else:
				content_split = content_split[63:]

			count_news += 1
			list_n.append(title[i].text)
			data.append({
                '1.Platform': "네이버",
                '2.Category': category + '뉴스',
                '3.Title': text_split,               
                '4.Url': title[i]['href'],
                '5.Date': date,
                '6.Number': count_news,
				'7.Content': content_split
            })
		for i in range(len(title1)):
			if len(title1[i].text) < 3:
				continue
			
			url_content1 = title1[i]['href']
			res_content1 = requests.get(url_content1, headers=headers_naver).text
			soup_content1 = BeautifulSoup(res_content1, 'html.parser')
			content1 = soup_content1.select('div > ._article_body_contents')

			if(not content1):
				content1 = title1

			text_split1 = title1[i].text
			text_split1 = text_split1.split()
			text_split1 = " ".join(text_split1)

			if(text_split1 == '동영상기사'):
				continue

			if(text_check1 == text_split1):
				continue

			text_check1 = text_split1

			content_split1 = content1[0].text
			content_split1 = content_split1.split()
			content_split1 = " ".join(content_split1)

			if(content_split1[0:6] == "동영상 뉴스"):
				content_split1 = content_split1[70:]
			else:
				content_split1 = content_split1[63:]
			
			count_news += 1
			list_n.append(title1[i].text)
			data.append({
                '1.Platform': "네이버",
                '2.Category': category + '뉴스',
                '3.Title': text_split1,               
                '4.Url': title1[i]['href'],
                '5.Date': date,
                '6.Number': count_news,
				'7.Content': content_split1
            })   
		page += 1
	tags = get_tags(' '.join(list_n), ranking)

	for tag in tags:
		result_ranking.append(tag['tag'])
		result_ranking1.append(tag['count'])

	with open('Naver_news_Data[' + category + '].json', 'w', encoding='utf-8') as f:
		json.dump(data, f, indent='\t', ensure_ascii=False)

	return result_ranking, result_ranking1
 
def check_index(): #Index 조회
   return es.indices.get_alias("*")

def create_index(mapping_json):	#Index 생성
	if not es.indices.exists(index=index):
		with open(mapping_json, 'r', encoding='utf-8') as f:
			mapping = json.load(f)
		res = es.indices.create(index=index, body = mapping)
		
		return res

def delete_index(): #Index 삭제
	if es.indices.exists(index=index):
		return es.indices.delete(index=index)

def insert(doc_json): #DB에 JSON 내용을 저장
	with open(doc_json, 'r', encoding='utf-8') as f:
		json_data = json.load(f)
	
	for i in json_data:
		res = es.index(index=index, body=i)
	
	return res

def search(keyword=None): #DB에 저장된 기사를 제목으로 검색
	body = {
		"from" : 0,
		"size" : 15,
		"query": {
			"match": {
				"3.Title" : keyword				
				}
		}
	}
	res = es.search(index=index, body=body, request_timeout= 30)

	for doc in res['hits']['hits']:
		result_search.append(doc['_source']['3.Title'])
		result_search1.append(doc['_source']['7.Content'])

	return result_search, result_search1

headers_naver = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48"}
exception = "동영상 기사 포토 사진 \r \t \n"
url_elastic = '127.0.0.1'
port = '9200'
index = 'news'
mapping_json = 'mapping_nori.json'
naver_categories = ['society', 'politics', 'economic', 'culture', 'science', 'IT']
naver_sid1 = [102, 100, 101, 103, 105, 105]
naver_sid2 = [257, 269, 263, 245, 228 ,230]
result_ranking = []
result_ranking1 = []
result_search = []
result_search1 = []
ranking = 10
d_today = datetime.date.today()
date = '20' + d_today.strftime('%y%m%d')

es = Elasticsearch(f'{url_elastic}:{port}')

####### 1.네이버뉴스 크롤링 및 단어 빈도수 출력과 기사들 JSON에 저장
for i in range(0,6):
	crawler_naver(naver_categories[i], naver_sid2[i], naver_sid1[i], date)

###### 2.index 삭제 ( Index 초기화 할때 아니면 항상 주석 처리 )
delete_index()
###### Index 생성 
create_index(mapping_json)

###### 3.기사를 저장한 JSON 파일을 DB에 저장
for category in naver_categories:
	insert('Naver_news_Data[' + category + '].json')

# #END

# nori 플러그인 설치
# sudo bin/elasticsearch-plugin install analysis-nori
# konply 모듈 설치
# pip install konlpy
# elasticsearch 설치
# 홈페이지 참고
# Beautifulsoup 설치
# pip install beautifulsoup4 
# scikit-learn 설치
# pip install --upgrade scikit-learn
